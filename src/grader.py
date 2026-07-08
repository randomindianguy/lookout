"""
grader.py — Part 1 of the eval harness: score ONE brief as PASS / PARTIAL / FAIL.

The code-vs-LLM split (neurosymbolic):
  - CODE checks the deterministic parts — no fabricated numbers (reuse
    validate.py), fired on the right budget, expected vendors/figures present.
    Fabrication and wrong-budget are HARD GATES: they auto-FAIL, overriding the
    judge. Vendor/figure presence is advisory evidence handed to the judge.
  - The OPUS judge reads intent — was the verdict correct, was silence the right
    call, is the reasoning sound, did the brief overreach beyond its data. It
    returns PASS / PARTIAL / FAIL plus its reasoning — never a 1-10 score.

The rubric per seed is the real work; each comes from that seed's PRD pass bar
(and the findings we locked while building it).
"""

from __future__ import annotations

import json
import re
from decimal import Decimal

import anthropic

from agent import load_dotenv
from tools import SyntheticFileDataSource, run_tool
from validate import validate_brief

JUDGE_MODEL = "claude-opus-4-8"   # the judge must be the most sophisticated model


# --------------------------------------------------------------------------- #
# Rubrics — one per seed, straight from the PRD's per-seed "what counts as
# correct". These ARE the test cases.
# --------------------------------------------------------------------------- #

RUBRICS = {
    "seed01_northwind": {
        "budget": "Contractors & Professional Services", "budget_key": "Contractors",
        "budget_id": "bud-contractors",
        "correct_verdict": "FLAG (early)",
        "scenario": "Surface: $90K paid of $300K plan (30%, looks healthy). Hidden: three signed, largely-unbilled commitments (~$290K owed) — design agency $120K, dev shop $120K, recruiter $50K (email-only, never logged in the finance tool). True position $380K = 127% of plan, $80K over, ~1 month runway, none of it charged yet.",
        "pass": "Breaks silence; states the true position is over 100% (127% / $380K) once commitments are counted; lists the commitments as proof including the email-only recruiter; frames it as PREVENTABLE / act now, not a post-mortem.",
        "partial": "Flags but frames it as hopeless / already-happened / a post-mortem (misreads the timing — nothing is charged yet, it is still preventable).",
        "fail": "Stays silent (misses the killer), OR fails to state a >100% true position, OR omits the hidden commitments.",
        "expected_vendors": ["Meridian", "Lumen", "Apex"],
        "expected_figures": ["127", "380,000", "290,000"],
    },
    "seed02_software": {
        "budget": "Software & Tools", "budget_key": "Software",
        "budget_id": "bud-software",
        "correct_verdict": "FLAG (late / brace)",
        "scenario": "Plan $150K. A cluster of annual subscriptions AUTO-RENEWED and ALREADY CHARGED (+$60K), taking paid actuals to $170K = 113% of plan, $20K over. committed_remaining is $0 — the money is already gone, nothing left unbilled to prevent.",
        "pass": "Flags (does not stay silent); recognizes the overspend ALREADY HAPPENED / already charged (no runway to prevent); frames it as brace-and-plan-around-it / prevent-recurrence-next-time — NOT 'act now to prevent' something already paid.",
        "partial": "Flags but is muddled on timing (half prevent / half brace).",
        "fail": "Stays silent (leaves them blindsided), OR tells the controller to 'act now to prevent' the $60K that already charged.",
        "expected_vendors": ["SentinelSec", "Lumina", "Vellum"],
        "expected_figures": ["113", "170,000", "20,000"],
    },
    "seed03_facilities": {
        "budget": "Facilities", "budget_key": "Facilities",
        "budget_id": "bud-facilities",
        "correct_verdict": "STAY SILENT",
        "scenario": "Plan $60K, $38K spent (63%, on pace). NO commitments at all, no traps, no twist. Genuinely, boringly fine.",
        "pass": "Stays silent — a brief, calm 'all clear' (63%, under plan, nothing coming). No flag.",
        "partial": "Stays silent but pads heavily / invents a mild hypothetical concern without flagging.",
        "fail": "Flags anything, OR manufactures a worry that isn't in the data (crying wolf in clean air).",
        "expected_vendors": [],
        "expected_figures": ["38,000", "60,000"],
    },
    "seed04_marketing": {
        "budget": "Marketing", "budget_key": "Marketing",
        "budget_id": "bud-marketing",
        "correct_verdict": "STAY SILENT",
        "scenario": "Plan $200K, $190K spent (95% — looks scary). But the big spend is a CLOSED annual campaign: $180K signed, only $150K billed, engagement finished — the remaining $30K will NEVER be spent (correctly excluded). Only a tiny $4K active SOW forward. True position $194K = 97%, under plan.",
        "pass": "Stays silent; looks past the scary 95%; recognizes the campaign is closed/finished so its $30K unbilled remainder won't be spent (correctly excluded); confirms it stays under plan. Ideally names the $30K and explains why it's set aside.",
        "partial": "Stays silent but never engages the scary $30K / doesn't explain why it's safe (silence without reasoning).",
        "fail": "FLAGS it (cries wolf) — treats the 95% or the closed $30K as a live overrun threat.",
        "expected_vendors": ["Brightline"],
        "expected_figures": ["97", "194,000", "30,000"],
    },
    "seed05_software": {
        "budget": "Software & Tools", "budget_key": "Software",
        "budget_id": "bud-software",
        "correct_verdict": "STAY SILENT",
        "scenario": "Plan $90K, only $20K paid (22% surface). A signed-but-UNBILLED $60K Helix annual renewal (recurring=annual, on a signed contract) makes the true position $80K = 89%. It is the expected, planned, recurring annual renewal, and it stays UNDER plan.",
        "pass": "Stays silent; recognizes the $60K is the expected/planned recurring annual renewal (not a surprise), on a signed contract, and that it keeps the budget under plan. Engages the scary 22%->89% jump and explains why it's routine.",
        "partial": "Stays silent but doesn't engage the renewal / doesn't explain why the 89% is fine.",
        "fail": "FLAGS the renewal as an overrun or hidden pile (cries wolf on an expected, under-plan recurring renewal).",
        "expected_vendors": ["Helix"],
        "expected_figures": ["89", "80,000", "60,000"],
    },
    "seed06_travel": {
        "budget": "Travel", "budget_key": "Travel",
        "budget_id": "bud-travel",
        "correct_verdict": "FLAG (early)",
        "scenario": "Plan $80K, $55K actuals (69%, looks fine). But ~8 small PRE-LEDGER commitments (conf regs approved on Slack, trips booked-not-charged, unsubmitted expenses) total $30K -> true position $85K = 106%, $5K over. Reconciliation wrinkle: one earlier booked-trip promise ($5K) has since been CHARGED — it must be counted ONCE (as the paid charge, remaining $0), NOT double-counted (which would give $90K).",
        "pass": "Flags early; the reason is the SUM of many small scattered pre-ledger items (~$30K), not one big thing; aggregates them to the correct total (true $85K); does NOT double-count the reconciled booked trip (true position is $85K, not $90K); frames as preventable.",
        "partial": "Flags but under-represents the aggregation, or is shaky on the reconciled item without actually double-counting the number.",
        "fail": "Stays silent, OR materially under-counts the small items, OR double-counts the reconciled trip (states true position ~$90K).",
        "expected_vendors": ["SaaStr", "re:Invent", "Offsite"],
        "expected_figures": ["85,000", "30,000"],
    },
    "seed07_recruiting": {
        "budget": "Contractors & Professional Services", "budget_key": "Contractors",
        "budget_id": "bud-contractors",
        "correct_verdict": "FLAG (uncertain) — calibrated, defer to human",
        "scenario": "Plan $100K, $55K actuals, a clear $10K commitment, PLUS a recruiting commitment whose amount is genuinely UNRESOLVED: an email thread that started at $50K (two roles), then 'pause the second role' (~$25K), then 'we might still want both — let me check with finance', trailing off. Amount is a real range $25K-$50K. The true position straddles the plan: $90K (90%, under) at one role to $115K (115%, over) at two.",
        "pass": "Flags it as UNCERTAIN; surfaces the $25K-$50K range and the unresolved thread; does NOT assert a settled figure; hands the judgment to a human to confirm; the headline reflects genuine indeterminacy (can't call over-or-under yet — $90K to $115K).",
        "partial": "Surfaces the uncertainty and defers, but leads the headline with a false-precise single number / midpoint (e.g. '$102.5K, $2,500 over') as if settled.",
        "fail": "Confidently asserts a single settled figure ($25K OR $50K OR the $37.5K midpoint) as the amount, as if the thread were resolved (false confidence / bluffing).",
        "expected_vendors": ["Talent", "Keystone"],
        "expected_figures": ["25,000", "50,000"],
    },
    "seed08_sales": {
        "budget": "Sales", "budget_key": "Sales",
        "budget_id": "bud-sales",
        "correct_verdict": "FLAG (early) — trajectory / rate of climb",
        "scenario": "Plan $120K. Four WEEKLY readings: $20K -> $45K -> $72K -> $95K. Every single reading is UNDER plan (latest 79%). No hidden commitments. But the rate of climb (~$25K/week) means the next reading lands at ~$120K — a breach in about one week, with two months of quarter left.",
        "pass": "Flags EARLY on the TREND/rate (not silent); the reason is the rate of climb, explicitly NOT 'you're over plan' (it isn't) and NOT 'a hidden pile' (there is none); walks the week-by-week climb ($20K->$45K->$72K->$95K); gives a forward forecast grounded in the readings (~1 week to breach / next reading ~$120K).",
        "partial": "Flags but only from the latest snapshot / doesn't reason about the rate, or gives no forward forecast.",
        "fail": "Stays SILENT because every individual reading is under plan (the snapshot-agent failure).",
        "expected_vendors": [],
        "expected_figures": ["20,000", "45,000", "72,000", "95,000", "120,000"],
    },
}

# All budget keywords, to detect a brief that fired on the WRONG budget.
ALL_BUDGET_KEYS = {r["budget_key"] for r in RUBRICS.values()}


# --------------------------------------------------------------------------- #
# Ground truth for a seed (what the agent legitimately had)
# --------------------------------------------------------------------------- #

def gather_tool_outputs(seed_dir: str, budget_id: str) -> list:
    """Every data-tool output for the seed's budget — the allowed set for the
    no-fabrication check, and the ground truth for the judge."""
    ds = SyntheticFileDataSource(seed_dir)
    outs = []
    for name, inp in [
        ("get_budget", {}),
        ("compute_position", {"budget_id": budget_id}),
        ("get_commitments", {"budget_id": budget_id}),
        ("get_transactions", {"budget_id": budget_id}),
        ("get_readings", {"budget_id": budget_id}),
        ("get_trajectory", {"budget_id": budget_id}),
    ]:
        r = run_tool(ds, name, inp)
        if not (isinstance(r, dict) and "error" in r):
            outs.append(r)
    return outs


def ground_truth_json(tool_outputs: list) -> str:
    return json.dumps(tool_outputs, default=str, indent=2)


# --------------------------------------------------------------------------- #
# Verdict-aware rubric for MUTATIONS. A mutation's correct verdict is its own
# LABEL (a flip has the OPPOSITE verdict of its parent seed), so it must be graded
# against verdict-appropriate criteria — NOT the parent seed's fixed pass/fail,
# which assumes the seed's original verdict. The parent seed supplies the SKILL
# context; the mutation's label supplies the verdict.
# --------------------------------------------------------------------------- #

SKILL = {
    "seed01_northwind": "catching hidden signed-but-unbilled commitments that push a calm-looking budget over plan",
    "seed02_software": "an already-charged overrun (too late to prevent — brace / plan around it, not 'act now to prevent')",
    "seed03_facilities": "a healthy control — don't manufacture problems in clean air",
    "seed04_marketing": "restraint — a scary-looking but closed/finished spend that won't be spent; stay calm",
    "seed05_software": "restraint — an expected, planned recurring renewal that keeps the budget under plan; stay calm",
    "seed06_travel": "aggregating many small pre-ledger commitments (and NOT double-counting a reconciled one)",
    "seed07_recruiting": "calibrated uncertainty — an unresolved range; flag-as-uncertain and defer, don't bluff a number",
    "seed08_sales": "reading the trajectory/rate — flag a still-climbing breach, stay calm on one that has flattened",
}

_GENERIC = {
    "FLAG": {
        "pass": "The agent FLAGS the budget (raises it as needing attention — states the true position is at/over plan, or clearly heading there — and does NOT stay silent). Reasoning is sound and grounded in the data.",
        "partial": "Flags, but with a real flaw: wrong framing/timing (calls a preventable overrun hopeless, or a too-late one preventable), or a shaky/ungrounded rationale.",
        "fail": "Stays SILENT (misses the overrun), OR asserts a position the data doesn't support.",
    },
    "SILENT": {
        "pass": "The agent STAYS SILENT ('watched, nothing to act on') — correctly judging the budget genuinely fine (under plan; any scary-looking amount is closed/cancelled/expected-recurring/small/already-past). Raises no alarm.",
        "partial": "Silent, but manufactures a hypothetical worry, or never engages the scary-looking element at all.",
        "fail": "FLAGS the budget (cries wolf on a genuinely-fine, under-plan budget).",
    },
    "UNCERTAIN": {
        "pass": "The agent flags the budget as UNCERTAIN and defers to a human — surfaces the amount as a range, does NOT assert a single settled figure, and the headline reflects genuine indeterminacy (can't call over/under).",
        "partial": "Surfaces the uncertainty and defers, but leads with a false-precise single number/midpoint as if settled.",
        "fail": "Asserts a confident single settled figure as the amount, OR stays silent (ignores the commitment).",
    },
}


def _verdict_class(verdict: str) -> str:
    u = verdict.upper()
    if "SILENT" in u:
        return "SILENT"
    if "UNCERTAIN" in u:
        return "UNCERTAIN"
    return "FLAG"


def mutation_rubric(parent_seed: str, label: str, budget_key: str) -> dict:
    """Rubric for a mutation: verdict-appropriate criteria for its OWN label,
    with the parent seed's skill as context."""
    v = _verdict_class(label)
    g = _GENERIC[v]
    return {
        "budget": budget_key, "budget_key": budget_key, "budget_id": "bud-x",
        "correct_verdict": v,
        "scenario": (f"A mutation in the '{parent_seed}' family. Skill under test: "
                     f"{SKILL.get(parent_seed, parent_seed)}. The correct verdict for THIS "
                     f"case is {v} — judge against that and the ground-truth data below."),
        "pass": g["pass"], "partial": g["partial"], "fail": g["fail"],
        "expected_vendors": [], "expected_figures": [],
    }


# --------------------------------------------------------------------------- #
# Code checks (deterministic)
# --------------------------------------------------------------------------- #

def code_checks(brief: str, tool_outputs: list, rubric: dict,
                budget_key: str = None, check_wrong_budget: bool = True) -> dict:
    # budget_key/check_wrong_budget let a MUTATION use its OWN budget name (the
    # rubric still comes from the parent seed) — the routing the manifest enables.
    low = brief.lower()
    bkey = budget_key or rubric["budget_key"]

    # HARD GATE 1 — no fabricated numbers (reuse validate.py).
    v = validate_brief(brief, tool_outputs)
    fabricated = [x["token"] for x in v.violations] if not v.ok else []

    # HARD GATE 2 — fired on the right budget. Fail only if the expected budget
    # is absent AND a *different* budget is clearly the subject. Disabled for
    # mutations (varied budget names make the cross-check unreliable).
    right_budget = bkey.lower() in low
    other_keys = ([k for k in ALL_BUDGET_KEYS if k.lower() != bkey.lower()
                   and k.lower() in low] if check_wrong_budget else [])
    wrong_budget = check_wrong_budget and (not right_budget) and bool(other_keys)

    hard_gate_fail = (not v.ok) or wrong_budget
    reasons = []
    if not v.ok:
        reasons.append(f"fabricated/untraceable numbers: {fabricated}")
    if wrong_budget:
        reasons.append(f"fired on the wrong budget (found {other_keys}, expected "
                       f"{bkey})")

    # ADVISORY — expected vendors / figures present (evidence for the judge).
    vendors_found = [x for x in rubric["expected_vendors"] if x.lower() in low]
    vendors_missing = [x for x in rubric["expected_vendors"] if x.lower() not in low]
    figs_found = [f for f in rubric["expected_figures"]
                  if f.replace(",", "") in low.replace(",", "")]
    figs_missing = [f for f in rubric["expected_figures"]
                    if f.replace(",", "") not in low.replace(",", "")]

    return {
        "no_fabrication_ok": v.ok,
        "fabricated_tokens": fabricated,
        "right_budget": right_budget,
        "wrong_budget": wrong_budget,
        "vendors_found": vendors_found,
        "vendors_missing": vendors_missing,
        "figures_found": figs_found,
        "figures_missing": figs_missing,
        "hard_gate_fail": hard_gate_fail,
        "hard_gate_reason": "; ".join(reasons) if reasons else None,
    }


# --------------------------------------------------------------------------- #
# The Opus judge (intent)
# --------------------------------------------------------------------------- #

JUDGE_SYSTEM = """\
You are a rigorous, senior evaluator (a grader) for Lookout, a committed-spend \
finance agent. You judge whether ONE agent output — a "brief", which is either a \
FLAG or a deliberate SILENCE — is CORRECT for its scenario, strictly against a \
rubric. You are the skeptical reviewer; do not be generous.

You judge INTENT and reasoning, not surface wording. Consider: did the brief \
reach the correct call (flag / stay silent / flag-late / flag-uncertain)? If it \
stayed silent, was silence genuinely the right call? Is the reasoning sound and \
grounded? Did it overreach beyond the data it actually had (the ground truth is \
given)? Deterministic checks (no fabricated numbers, right budget) have already \
been run in code and passed — do not re-litigate those; focus on judgment.

Return ONLY a JSON object, nothing else:
{"verdict": "PASS" | "PARTIAL" | "FAIL", "reasoning": "<2-4 sentences: what the \
brief did, measured against the rubric's pass/partial/fail lines, and why that \
verdict>"}

Never output a numeric score. PARTIAL is for the rubric's explicit partial case \
(right direction, a real flaw). Reserve PASS for meeting the pass bar; FAIL for \
the wrong call or a missing essential."""


def _build_judge_user(rubric: dict, ground_truth: str, code: dict, brief: str) -> str:
    return f"""\
SCENARIO (ground-truth facts):
{rubric['scenario']}

CORRECT VERDICT: {rubric['correct_verdict']}

RUBRIC — what counts as correct for this scenario:
- PASS if: {rubric['pass']}
- PARTIAL if: {rubric['partial']}
- FAIL if: {rubric['fail']}

DETERMINISTIC CODE CHECKS (already run; evidence for you):
- no fabricated numbers: {code['no_fabrication_ok']}
- expected vendors present: {code['vendors_found']}  | missing: {code['vendors_missing']}
- key figures present: {code['figures_found']}  | missing: {code['figures_missing']}

FULL GROUND-TRUTH DATA the agent had (the only numbers/facts it could legitimately use):
{ground_truth}

=== AGENT OUTPUT TO GRADE (the brief) ===
{brief}
=== END AGENT OUTPUT ===

Grade it. Return only the JSON object."""


def _parse_verdict(text: str) -> dict:
    # pull the first JSON object out of the response
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            obj = json.loads(m.group(0))
            v = str(obj.get("verdict", "")).strip().upper()
            if v in ("PASS", "PARTIAL", "FAIL"):
                return {"verdict": v, "reasoning": str(obj.get("reasoning", "")).strip()}
        except json.JSONDecodeError:
            pass
    # fallback: keyword scan
    up = text.upper()
    for v in ("PARTIAL", "FAIL", "PASS"):
        if v in up:
            return {"verdict": v, "reasoning": text.strip()[:600]}
    return {"verdict": "ERROR", "reasoning": text.strip()[:600]}


def judge_brief(brief: str, rubric: dict, ground_truth: str, code: dict,
                model: str = JUDGE_MODEL) -> dict:
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=model,
        max_tokens=1000,
        system=JUDGE_SYSTEM,
        messages=[{"role": "user",
                   "content": _build_judge_user(rubric, ground_truth, code, brief)}],
    )
    text = "".join(b.text for b in resp.content if b.type == "text")
    return _parse_verdict(text)


# --------------------------------------------------------------------------- #
# Batch-friendly split: code gate locally, judge via the Batch API (50% cheaper).
# The JUDGE_SYSTEM prompt is identical across every grade, so cache it.
# --------------------------------------------------------------------------- #

_JUDGE_SYSTEM_CACHED = [{"type": "text", "text": JUDGE_SYSTEM,
                        "cache_control": {"type": "ephemeral"}}]


def prepare_grade(brief, seed_id, seed_dir, budget_id=None, budget_key=None,
                  check_wrong_budget=True, mutation_label=None):
    """Run the local code gate. Returns either a finished FAIL (hard gate tripped —
    no judge needed) under 'short_circuit', or the params for a batched judge call
    under 'judge_params' plus the 'code' facts to finalize with."""
    load_dotenv()
    rubric = (mutation_rubric(seed_id, mutation_label, budget_key or seed_id)
              if mutation_label else RUBRICS[seed_id])
    tool_outputs = gather_tool_outputs(seed_dir, budget_id or rubric["budget_id"])
    code = code_checks(brief, tool_outputs, rubric,
                       budget_key=budget_key, check_wrong_budget=check_wrong_budget)
    if code["hard_gate_fail"]:
        return {"short_circuit": {"verdict": "FAIL", "decided_by": "code (hard gate)",
                                  "reasoning": f"Hard gate: {code['hard_gate_reason']}",
                                  "code": code, "judge": None}}
    return {"code": code,
            "judge_params": {"model": JUDGE_MODEL, "max_tokens": 1000,
                             "system": _JUDGE_SYSTEM_CACHED,
                             "messages": [{"role": "user", "content": _build_judge_user(
                                 rubric, ground_truth_json(tool_outputs), code, brief)}]}}


def finalize_grade(judge_text, code):
    """Turn a judge's raw response text + the code facts into a grade dict."""
    jr = _parse_verdict(judge_text)
    return {"verdict": jr["verdict"], "decided_by": "judge (Opus)",
            "reasoning": jr["reasoning"], "code": code, "judge": jr}


# --------------------------------------------------------------------------- #
# The grader: combine code hard-gates + judge
# --------------------------------------------------------------------------- #

def grade(brief: str, seed_id: str, seed_dir: str, model: str = JUDGE_MODEL,
          budget_id: str = None, budget_key: str = None,
          check_wrong_budget: bool = True, mutation_label: str = None) -> dict:
    """Grade one brief. For the 8 SEEDS, uses the seed's own (validated) rubric.
    For a MUTATION, pass mutation_label (its ground-truth label) + its own
    budget_id/budget_key: it is graded against verdict-appropriate criteria for
    THAT label, with the parent seed's skill as context (a flip has the opposite
    verdict of its parent, so the parent's fixed pass/fail cannot be reused)."""
    load_dotenv()
    if mutation_label:
        rubric = mutation_rubric(seed_id, mutation_label, budget_key or seed_id)
    else:
        rubric = RUBRICS[seed_id]
    tool_outputs = gather_tool_outputs(seed_dir, budget_id or rubric["budget_id"])
    code = code_checks(brief, tool_outputs, rubric,
                       budget_key=budget_key, check_wrong_budget=check_wrong_budget)

    if code["hard_gate_fail"]:
        return {
            "verdict": "FAIL",
            "decided_by": "code (hard gate)",
            "reasoning": f"Hard gate: {code['hard_gate_reason']}",
            "code": code,
            "judge": None,
        }

    jr = judge_brief(brief, rubric, ground_truth_json(tool_outputs), code, model)
    return {
        "verdict": jr["verdict"],
        "decided_by": "judge (Opus)",
        "reasoning": jr["reasoning"],
        "code": code,
        "judge": jr,
    }
