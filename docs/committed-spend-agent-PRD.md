# Lookout — Running PRD

**Status:** v1.5 (living document)
**Last updated:** July 7, 2026
**Owner:** Sid
**Purpose of this doc:** Capture every locked decision, open question, and reason-why for the project, so it can be defended cold and handed to a reviewer. Updated continuously as decisions are made or changed.

> **How to read this:** Structured on the AI Product Lifecycle framework (Act I strategy → Act II build/eval → Act III go-to-market). Plain English throughout; technical terms are defined on first use. The **Decision Log** at the bottom tracks what changed and when.

> **The name — Lookout:** a lookout stands watch, stays silent for hours, and calls out only when something real appears. It names the *differentiator* (watchful restraint), not just the problem (hidden spend). Interview line: *"I built Lookout because the hard part isn't catching the overspend — it's knowing when to stay quiet, like a lookout who doesn't cry wolf."*

---

## 0. What this project is (in one paragraph)

A "hire-me" artifact: a working AI agent that watches a company's budgets and catches money the company has already promised but not yet paid — the kind of overspend that looks fine on the surface and blindsides finance teams at month-end. It is aimed primarily at **Ramp** (dream company), and also fits **Warp**. Its job is **not** to be a novel idea nobody's had; its job is to **prove Sid can build the kind of trustworthy, human-approved finance agent these companies build — held to a higher standard of proof (evals) than they've shown publicly.** The product is the evidence; the real moat is the thinking behind it.

---

## 1. The core problem

**Two kinds of money:**
- **Actual spend** — money that has already left the account. Shows on statements. Easy to see.
- **Committed spend** — money already promised but not yet paid: signed contracts not yet billed, purchase orders (a purchase order = a formal "we're buying this" record), renewals about to auto-charge, invoices sitting unpaid, expenses not yet submitted.

**The trap:** most tools track only actual spend, so a budget that's paid $90K of $300K looks 30% spent and healthy — while secretly being 127% committed once you count what's promised. Finance finds out when the invoices land, too late to act.

**The real enemy is NOT another tool (Juicebox lens).** Run the JTBD honestly: the finance person's job isn't "see committed spend on a screen," it's **"not get blindsided."** And the highest-signal, lowest-effort way a competent finance person already avoids that is **to ask the budget owner directly** — Slack the eng manager "any big spend coming on Contractors I should know about?" That human reflex is the true competitor, the same way *referrals* (not another staffing tool) were Juicebox's real enemy. It wins on the exact axis your agent is weakest: **certainty of signal.** The owner *knows* they're signing a $150K contract; your agent *infers* a maybe-commitment from a messy thread.

- **Why naming this makes the agent stronger:** asking-around has a fatal weakness — **it doesn't scale.** It works at 5 budgets / 5 people you can Slack. At 30 budgets, where you don't know who to ask, or the owner forgot, or the commitment lives in a forgotten email, it collapses. **The agent's real job is to automate the "Slack-the-budget-owner" reflex and make it exhaustive** — no longer dependent on the finance person knowing who to ask or the owner remembering to speak up.
- **Honest limit (don't overclaim):** for big, known commitments a good team *will* still ask, and should. The agent is the **safety net under the human network** — it catches what asking-around misses (the commitments nobody thought to mention, the forgotten threads, the ones you didn't know to ask about). It eats the cases asking-around can't cover; it doesn't replace it.
- **Secondary framing (still true, now subordinate):** vs. dashboards specifically, the enemy is **attention, not visibility** — tools *display* committed spend; nobody caught it in time. But the *primary* competitor is the human workaround, not the tool.

> Analogy: a security system's real competitor isn't other alarm brands — it's **good neighbors** ("keep an eye on my place"). That human network works great on a small street where everyone knows everyone, and falls apart in a big building where you don't. The agent is the security system: it does what good neighbors do (watch your place) but scales to where neighbors no longer know each other.

---

## ACT I — Product Sense & Strategy

### 2. Differentiation — gauge vs. co-driver

Existing tools (Spendesk, Qonto, commitment-accounting software) already **show** committed-vs-actual. They are **gauges**: accurate numbers on a screen a human has to go read.

The agent is the **co-driver / doctor**, not another gauge. The difference is three things a dashboard does not do:
1. **Judgment across many** — watches all budgets, stays silent on the fine ones, and speaks on the *one* worth a human's attention right now.
2. **Timing** — judges whether there's still runway to act, and frames the message as *preventable* vs. *post-mortem*.
3. **Reach into messy places** — assembles promises even from places they were never formally logged (email, Slack, shared drives), not just what's in the finance tool.

> Analogy: a blood-test machine prints "cholesterol 240" and stops (the gauge). The doctor decides *this* number matters for *you*, catches it early, and tells you while there's still time (the agent). Nobody's blindsided because the machine broke — they're blindsided because a number sat on a screen and no doctor looked in time.

**What is NOT the differentiator (never claim it):** the committed-vs-actual arithmetic itself. That's commodity. The judgment *around* the number is the product.

**For the reviewer:** the point isn't the idea (Ramp likely ships something adjacent) — it's the *execution bar*. Everything below (the evals, the golden dataset, the disagreement-rate discipline) is deliberately auditable — don't take "senior-level" on faith; check the harness. *(Open kitchen, not a plated dish.)*

**Delta-4 check** (does the new experience beat the old by ≥4 on a 1–10 scale, or users won't switch): month-end catch ≈ 2, early catch with proof ≈ 8. Delta of 6. Passes.

### 3. Target user (segmentation)

- **Who:** the **controller / finance manager** at a **mid-market (201–1000 person), venture-backed Silicon Valley software company** — a stretched 2-person finance team.
- **Why this user:** it's Ramp's own core customer and the exact user Ramp's Policy Agent serves. The problem's severity scales with **budgets-per-person** — at 3 budgets you eyeball it; at 15–50 across departments you can't, so the trap is guaranteed.
- **Buyer vs. user:** the controller *does the task*; the CFO *feels the fear*. We build for the doer, the way Ramp does.
- **Why this user and not the neighbors (hypothesize, then check):** the mid-market controller — *not* the CFO (feels the fear, doesn't do the task), *not* the sub-10-person startup (few enough budgets to eyeball), *not* the large enterprise (has a full FP&A team and tooling to absorb it). The controller is the band where "asking around" stops scaling but there's no team to catch what falls through. That's the pick — unless the role you're hiring for skews to a different band.

### 4. Jobs to Be Done (FSE)

- **Functional:** across all my budgets, catch the one heading over *in time to act*, without me watching everything.
- **Emotional:** let me put down the constant, low dread that something's going wrong and I'll find out too late. Let me **trust the silence**.
- **Social:** let me be the person who flagged it early in the review, not the one explaining the overrun after.
- **Core human drive:** fear (of being caught not knowing). Lead with this, not "saves time."

---

## ACT II — Building & Evaluation

### 5. How the agent behaves

- **Proactive, not reactive.** It stands watch over live state; nobody has to ask it anything. (Reactive = waits for a request. Proactive = watches on its own.)
- **Silent by default.** Most of its job is correctly saying nothing.
- **Speaks only on what matters** — the one budget worth interrupting a human over.

### 6. The two-part output

1. **Diagnosis — the "true-position brief."** One page: "This looks 60% spent and healthy. It's not — it's at 127% once you count committed spend. Here's the exact pile that proves it. Here's the runway left." **Easy for a human to verify** (they can check the receipts), so the agent owns this outright.
2. **The fix — a staged action.** A reforecast / limit change / hold, prepared and held for the human's **one-click approval**. **Hard to verify + high stakes** (it moves money), so a human signs.

> Analogy: the doctor shows you the X-ray with the break circled (diagnosis — you trust it instantly) and *proposes* the surgery (the fix — you sign off before anyone cuts).

### 7. Where the human sits (the most important architectural line)

**The human sits on the FIX, not the diagnosis.** The agent is trusted to spot the problem alone; a person only approves the money move.
- This is **Sheridan Level 5** — "AI executes if human approves." Roadmappable toward Level 6 as trust builds. (Sheridan levels = a ladder of how much the agent may do alone.)
- This is also exactly Ramp's stated rule ("no money moves without human confirmation") and Warp's ("Approve" button before it acts). Sid reasoned to it independently from the frameworks.

### 8. Confidence-based calibration (Sheridan + human-in-the-loop)

The agent **moves up and down the autonomy ladder based on its own confidence:**
- **Clear case** → sits high, states the answer plainly.
- **Tangled case** → drops low, flags its uncertainty and asks the human ("I read a possible $25K–$50K commitment in a messy thread — please confirm").
- Human-in-the-loop fires **exactly when confidence is low** — where a human's judgment is most valuable.

> Analogy: a good junior employee pays the routine bill and tells you after, but stops and asks about the ambiguous $40K vendor claim. Same person, calibrated by how sure they are.

### 8b. Restraint lives in the reflection step

**Reflection** (from the agentic-design patterns) = the agent challenging its own first answer before committing to it (proofreading your essay before submitting). **Restraint is not a separate feature — it IS the reflection step.** The agent's fast first reaction to a 95%-spent budget is "alarm!"; reflection is the pause where it asks "wait — is this actually heading for trouble, or does it just look that way?" and overrides its own false alarm.

- **Tuning the reflection step = setting the precision/recall dial.** Too much reflection → it talks itself out of real alarms (kills recall, misses Seed 1's killer). Too little → it cries wolf (kills precision, fails Seed 4). Seeds 1 and 4 are the two guardrails for tuning it: reflect enough to stay quiet on Seed 4, not so much that you suppress Seed 1.
- Defensible line: *"restraint in my agent is implemented as a reflection step — it challenges its own first-pass alarm before speaking."*

> Analogy: reflection is a smoke alarm's sensitivity knob. Too high → screams at burnt toast (no reflection). Too low → sleeps through a real fire (over-reflection). Seeds 1 & 4 are the fire and the toast; tune until it's loud for one, quiet for the other.

### 8c. The two-bucket model (avoids double-counting)

A promise and its later charge are **the same dollar at two stages of its life**, not two separate things. Model spend as **two stocks (buckets):** *promised-but-not-paid* and *already-paid*. Events are flows:
- Booking a $4K trip → pours water into the **promised** bucket.
- The card actually charging $4K later → **transfers** that dollar from *promised* to *paid*. It is NOT new money entering the system.

**True position = both buckets added together.** Double-counting happens if the agent treats the charge as fresh water in the *paid* bucket without draining it from *promised* — total wrongly jumps by $4K when it should stay flat. **The fix ("relieve the promise when the charge lands") is one rule: a charge is a transfer between two stocks, not an inflow.**

- This is a property of the agent's **core world-model**, not a per-seed patch. Build the two-bucket model once → correct reconciliation falls out across *every* seed. (Design the whole, then let the parts verify it — systems-thinking.)
- The hard sub-skill is **matching**: recognizing a messy card charge ("UNITED AIR 0162, $4,037") is the same obligation as a promise seen in an email ("United, $4,000") when nothing formally links them. Too-eager matching → under-counts (hides overspend). Too-reluctant → over-counts (cries wolf). Same dial again. When a match is genuinely ambiguous → flag and ask the human.

> Analogy: moving money from savings to checking doesn't make you richer — it's a transfer. An accountant who counts the checking deposit as new income while still counting it in savings thinks you gained money. A charge landing is a transfer, not income.

### 9. How the agent finds the money (three places)

1. **Already spent** — in spending records. Easy. Any tool sees this.
2. **Promised and recorded** — signed contracts / POs logged in the finance tool. Existing tools see this too.
3. **Promised but hiding in messy places** — a deal that only exists in an email, a PDF in a drive, an approval in Slack. **This is the edge and the hard part.** A normal dashboard never sees pile 3.

Then: add all three, compare to plan, judge whether to speak.

> For the demo, these three places are **fake sources** built into the synthetic company (movie set). In the real world, the agent would need permission to connect to the spending system, contracts folder, and email/messaging — exactly how Ramp's and Warp's agents work.

### 10. The hard core (the real product spine)

Reading **scattered, evolving human conversations** and landing on the *current* truth — and being honest when unsure. A promise might live in email 2 of a 15-email thread, change in email 7, get cut in email 11. The real number is only knowable by reading the whole thread. This is the "archaeologist vs. metal detector" skill, and it's where evals earn their keep.

### 11. Build architecture (mimics how Ramp builds)

- Ingest **messy reality**, not just tidy rules.
- **Tool-calling** shape: `get_budget`, `get_commitments`, `get_actuals`, and `stage_reforecast` — the money move as the **one gated tool**.
- Confidence band, human on money, explainable brief as the audit trail, closed-loop evals.

---

## 12. Evaluation (the overshoot — Sid's strongest card)

**Evals are the differentiator vs. what Ramp/Warp showed publicly.** They ship the brief; they don't show how they *prove it's right*.

**Double duty:** these evals prove two things at once — that the *agent* is trustworthy, and that *I* operate at your team's bar. They're built to be audited by a skeptical senior reviewer, not just to produce a number. That's the point.

### 12a. Metrics
- **Precision** — when it flags, how often is it right? (Guards against crying wolf.)
- **Recall** — of the truly-blown budgets, how many did it catch?
- **Tuned toward precision over recall** (trust > catching everything), same call as Revue. Shown as a **PR curve** (performance across every dial setting) — the grown-up view Ramp didn't show.

### 12b. Timing counts
A "correct catch" = truly blown **AND** flagged **AND** with runway left to act. "Caught but too late" is a **different failure type** (tracked separately), not the same as a false alarm.

### 12c. The golden dataset (the spine — built BEFORE the agent)
The golden dataset = a set of fake budgets where **Sid already knows the right answer**. It's the answer key the agent is graded against.
- **Rubric:** binary pass / fail / partial. Sharpened until independent graders disagree **<10%** (disagreement rate). For the golden set specifically, disagreement must be **near zero**.
- **Ground truth is Sid's.** Sid authors every verdict (the human anchor). **Claude Code spawns adversarial finance-persona agents to *stress-test* the verdicts — never to set them.** Honest caveat to state openly: one author, stress-tested; a production setting would want more human labelers.
- **Calibration eval:** also test whether the agent **asked for help at the right moments** (knew when to be confident vs. ask), not just whether it got the number right.

### 12d. Seed-and-mutate
- **Seeds:** hand-written by Sid, airtight, defensible cold. Quality lives here. **Guard seed correctness above everything — the golden set is the answer key; if it's wrong, every number measured against it is garbage.**
- **Mutations:** machine produces ~15 variations per seed — **same answer, different surface**. Gives quantity + forces the agent to reason instead of memorize. **Use the right technique per data type:**
  - *Structured data (budgets, commitments-as-data):* **self-instruct / seed-instruction** — give the seed triplet (input + correct verdict), model generates more following the pattern.
  - *Messy documents (email threads, contracts):* **back-translation through a structurally-distant language** (Hindi / Japanese / Arabic, not French/Spanish — wider structural gap reshuffles phrasing more), so the fake docs don't all read like one author. Fixes the realism problem.
- **Engineer diversity DELIBERATELY — don't trust mutation to produce it.** 15 mutations of one seed can be 15 photocopies of the same quirks (all formal, all American-English) = *narrowness masquerading as coverage*. Mutation multiplies **quantity**; **diversity** must be designed in, by explicitly varying the axes (hiding mechanism, writing style, closeness-to-the-line), not just names/amounts.
- **Never delete high-disagreement cases** (the ambiguous/borderline ones, e.g. Seed 7) — they're the "storms" the agent most needs to face. Diagnose *why* they're ambiguous; remove genuine ambiguity, keep the hard case.
- **Three pillars:** quality = the seeds (human-owned), quantity = mutation (free), diversity = deliberate coverage. *Garbage seed in → 15× garbage out, so seeds come first.*

### 12e. Minimum Viable Performance
For AI, "MVP" = **Minimum Viable Performance**, not product. Launch bar is a number (e.g. "≥X% precision, ≥Y% recall on the golden set"). **[Number TBD.]**

### 12f. The build loop — how the agent is made to work across all seeds and mutations

The agent is **not** built once and then tested. It is built *against* the seeds, one failure at a time. This is the daily job.

**The loop:**
1. **Run & watch it fail.** First version will be bad (~20% right is normal). Run all seeds; the failures are the map of what to fix.
2. **Fix, cheapest lever first, then re-run.** Change the agent's instructions (the prompt) first — it's hours, not weeks. Re-run everything. Some pass; some may newly break.
3. **Repeat until it clears the bar** (Minimum Viable Performance). This grind — run, fail, fix — *is* the work of building an AI product.

> Analogy: training a new employee for a judgment job. You don't hand them the rulebook and send them to the client; you give them practice cases, watch each one, and coach the misses. Seeds = practice cases. The prompt = your coaching. The loop = the training.

**Two things that make it work across seeds AND mutations:**
- **Tune on seeds, TEST on mutations.** If you only tune against the 7 exact seeds, you coach the agent to memorize those 7 (like memorizing a practice test). The mutations — variations the agent was *not* tuned on — are the proof it learned the real skill and generalizes. Passing the fresh mutations is the only real proof.
- **Watch precision AND recall together — fixes fight each other.** Make it catch more aggressively → it starts crying wolf on the restraint cases (broke precision). Calm it down → it misses a real killer (broke recall). Seven seeds pull in different directions; the eval loop tells you the moment a fix in one place broke another. The goal is the setting that satisfies the whole table, not any one case.

> Analogy: adjusting a recipe for a dinner party. Spicier for the guests who want heat ruins it for those who don't. Seven seeds = seven guests. You tune for the whole table, and every change risks pleasing one while upsetting another.

**Honest bar:** "works across all seeds" does **not** mean a perfect answer on all seven. It means **gets the clear ones right and correctly raises its hand (asks the human) on the genuinely hard ones** (esp. Seed 7, the borderline thread). That calibration — knowing when it's unsure — is itself a tested, provable behavior, and more honest + impressive than claiming a perfect score.

### 12g. Honesty has TWO layers (only one is built)

Discovered while building Seeds 1 & 4 — a key insight about what "trustworthy" actually requires:
- **Layer 1 — provenance (BUILT, code):** every number in a brief traces to a real tool output; nothing fabricated. Enforced by `validate.py` (`validate_brief`), which runs on every brief and rejects+regenerates any brief citing a number that isn't a tool value. This is the code-enforced guarantee. *Key lesson banked: a prompt rule is probabilistic, not structural — "never invent a number" only became a real guarantee once it lived in **code**, not the prompt. (Prompts persuade; code enforces.)*
- **Layer 2 — semantic accuracy (LATER, rubric):** is each real number *described correctly*? A brief can cite a real, tool-sourced number and still attach it to the wrong concept (Seed 4 called the $6,000 under-plan margin the "surface-to-true gap" — right number, wrong label). The validator **cannot** catch this by design (it checks where a number came from, not whether the sentence about it is true). This is a job for the **eval rubric + LLM judge**. **→ Rubric criterion, now on the list: "every number is not just real but correctly labeled."**

> Analogy: Layer 1 is a fact-checker who verifies every statistic traces to a real source. Layer 2 is a fact-checker who reads whether the *sentence around* the statistic describes it correctly. "Unemployment is 4%, so the economy is shrinking" — the 4% is real (passes Layer 1) but the claim is false (only Layer 2 catches it). Two different kinds of lie; only the first is guarded so far.

### 12h. Which brain owns which decision (a recurring design call)

The system has two "brains" — **code** (reliable, identical every run) and the **LLM** (judgment, probabilistic). A recurring skill is deciding which owns which decision:
- **Code owns:** the math (`compute_position`), and the honesty *guarantee* (`validate.py`). Anything that must be true 100% of the time.
- **LLM owns:** the visible judgment — flag vs. silent, the framing, and *explaining* decisions the code made.
- **The trap (found in Seed 4):** if code silently pre-digests a judgment (excluding the closed $30K before the LLM sees it), the seed no longer tests the *agent's* judgment — the code's correctness is doing the work, invisibly. Fix = **surface** the excluded item so the LLM must *see it and explain why it's excluded*. Code still owns the number; the agent owns the explanation. Restraint reasoning becomes visible and gradeable — which is the whole differentiator, so it must not hide in code.

### 12i. Build progress (Seeds 1 & 4)

- **Seed 1 (flag) — BUILT & VERIFIED.** 127% falls out of the data (not hard-coded); no-double-count invariant holds. Brief iterated through the eval loop: correct-but-flat → forceful (lede-first, controller-addressed, vivid-but-true) → honest (validator added after two fabrication slips) → clean (money = `Decimal`, no tool-names, no provenance-narration). Voice locked.
- **Seed 4 (restraint) — BUILT & VERIFIED.** Sharpened so the `closed` flag is *decisive* (closed-but-under-billed $30K: naive reading 112% flag → correct reading 97% silent). Agent correctly stays silent AND now visibly reasons about the $30K (names the vendor, cites the signed-vs-billed gap, says it "would look alarming on paper," explains why the closed remainder won't be spent) via the hybrid surfacing (§12h). Both poles pass on the identical system prompt — no restraint-specific tuning.
- **Discipline reminder:** a single passing run is an **anecdote**, not proof. It confirms the agent *can* do the right thing and the seed is built right — a green light to keep building, not a victory. **Reliability** (each seed × ~15 mutations, run many times → pass rate) comes after the full seed set. Don't over-celebrate single runs.

---

## 13. The eight seeds (golden-dataset bedrock)

**Axes of variation:** verdict × hiding mechanism × closeness-to-the-line × **time (snapshot vs. trajectory)**. Each seed sits at a deliberate point so the agent can't pass by memorizing one pattern. **Note: three of the eight are "stay silent" cases (3, 4, 5) — restraint is the differentiator. Seed 8 tests watching over time, which the others (snapshots) cannot.**

| # | Verdict | Hiding mechanism / signal | Role in the set |
|---|---------|------------------|-----------------|
| 1 ⭐ | Flag early | Unpaid signed contracts (one email-only) | **FLAGSHIP** — the money shot |
| 2 | Flag late | Auto-renewing subscriptions, already fired | Tests: still speak + shift tone to "brace, not prevent" |
| 3 | Stay silent (healthy) | None — clean control | The genuinely-nothing-wrong case |
| 4 | Stay silent (scary-but-fine) | **Near the limit** — 95% spent, nothing more coming | **Restraint #1** — false alarm about *how much* |
| 5 | Stay silent (scary-but-fine) | **Abnormal-looking charge** — big spike that's a legit expected annual payment | **Restraint #2** — false alarm about *what it looks like* |
| 6 | Flag early | Informal Slack approvals + late expenses (pre-ledger) + reconciliation | Death-by-a-thousand-cuts; sum scattered small things; two-bucket test |
| 7 | Borderline | Messy multi-email thread where the promise **changes** | Capstone: calibrated uncertainty; tests false-confidence |
| 8 | Flag early | **Trajectory** — fine every week, but the *rate* predicts a breach | **The "watching over time" seed** — closes the snapshot hole |

**⭐ = flagship (wins the room emotionally). Seeds 4 & 5 = win the room intellectually (restraint). Seed 7 = the trust capstone. Seed 8 = proves it actually *watches*.** Build Seed 1 and Seed 4 back-to-back to lock both poles of judgment.

> Seed count is not fixed — if a genuinely new *kind* of judgment case surfaces later, add a seed. Serve the judgment being proven, not the number.

### Seed 1 — FLAGSHIP (FULLY LOCKED)

- **Company:** "Northwind" (placeholder name), ~300-person VC-backed SV software co, post Series B. Finance = 1 controller + 1 junior analyst. **6 budgets:** Marketing, Software & Tools, Sales, Travel, Contractors & Professional Services, Facilities. **Clock:** 2 months into a 3-month quarter.
- **Killer budget:** Contractors & Professional Services.
- **Surface (what a dashboard shows):** $300K planned, $90K paid → looks 30% spent, comfortable.
- **Hidden commitments (~$290K):**
  - Design agency: $180K signed, $60K billed → **$120K owed**
  - Contract dev shop: $150K signed, $30K billed → **$120K owed**
  - Recruiter: $50K signed, $0 billed (bills on placement, lands this month) → **$50K owed** — *exists only as an email, never logged in the finance tool* (most realistic detail + shows the pile-3 edge)
- **Truth:** $90K paid + $290K committed = **$380K vs. $300K plan = 127%**, over by $80K, none of it hit the account yet, ~1 month runway.
- **Verdict line (ground truth):**
  - **Call:** flag early.
  - **Reason:** committed to 127% of plan through three signed, largely un-invoiced contracts invisible in actual spend, with ~1 month runway.
  - **Pass bar:** must break silence; must state true position >100% once commitments counted; must frame as *preventable*, not a post-mortem. Silent = fail. Flags-but-calls-it-hopeless = partial fail (misread timing).
- **Simplifications (state openly if asked):** round numbers for mental math; single-snapshot timeline; clean source separation. Mechanism works identically with messy real numbers.

### Seed 4 — RESTRAINT #1, near the limit (FULLY LOCKED)

The **mirror of Seed 1.** Seed 1 looks safe (30%) but is dangerous (127%). Seed 4 looks dangerous (95%) but is safe (0% committed going forward). Together they prove the agent judges the *real* position, not the surface number.

- **Company / clock:** same Northwind, 6 budgets, 2 months into a 3-month quarter.
- **Budget in question:** Marketing.
- **Surface (what makes it scary):** $200K planned, $190K spent → **95% spent** with a third of the quarter left. Looks about to blow past plan; a dumb alarm fires instantly.
- **Hidden layer (what makes it safe):** the $190K was almost entirely **one completed annual brand campaign** (ran months 1–2, delivered, fully paid, closed out). No open contracts, no unpaid invoices, no renewals coming. Only ~a few $K of routine content work left in month 3, well inside the ~$10K headroom.
- **Truth:** 95% spent, but **finished, not accelerating.** Committed spend going forward ≈ zero. Nothing to act on.
- **Verdict line (ground truth):**
  - **Call:** stay silent.
  - **Reason:** at 95% of plan, but the spend is a completed, closed-out annual campaign with ~zero remaining commitments and enough headroom for the small routine work left. High spend, no danger.
  - **Pass bar:** must **not** flag. Must look past the 95%, verify remaining commitments ≈ zero and the big spend is closed, and stay quiet. Flagging = fail (crying wolf — the trust-killer).
- **Why it's harder to build than Seed 1:** the agent must reason about the *nature* of the spend (is it done, or still running?), not just the amount. It'll likely panic at 95% first — this seed is the best diagnostic for teaching restraint.

> Analogy: a marathon runner at mile 25 of 26 — drenched, gasping, looks about to collapse. The panicked bystander calls an ambulance; the smart observer sees they're almost done and fine. "Near the end" looks like "in trouble," but they're different things. Telling them apart is the whole test.

### Seed 2 — Too-late (auto-renewals already fired) — LOCKED

- **Budget:** Software & Tools. Plan $150K, calm at $110K, then a cluster of annual subscriptions **auto-renew within days** → +$60K → $170K, over by $20K.
- **Why "too late":** auto-renewals fired automatically and **already charged**. No runway — the event that needed preventing already happened on its own.
- **Verdict:** **flag, but as heads-up + prevent-next-time**, not prevention. Must still speak (person needs to know), but frame honestly as "this already happened, plan around it — and here's how to avoid it next year." Staying silent = fail (leaves them blindsided).
- **Role in set:** the single deliberate too-late case. Tests whether the agent shifts its behavior based on *timing* (fix-it vs. brace-and-prevent). **One is seasoning, not the meal** — keeps the set honest (proves Sid didn't cherry-pick only wins).

> Analogy: coming home to a basement already flooded from a burst pipe. You still need to know (insurance, cleanup, prevent next time), but nobody's handing you a mop to stop a flood that already happened.

### Seed 3 — Healthy control — LOCKED

- **Budget:** Facilities. Plan $60K, spent $38K (~63%, on pace), no hidden commitments, no twist.
- **Verdict:** **stay silent** — everything is genuinely, boringly fine.
- **Role:** the baseline. If the agent can't say nothing about a normal budget, it's hopelessly trigger-happy. The "does the smoke alarm stay quiet in a room with no smoke" test.

### Seed 5 — Restraint #2 (abnormal-looking but fine) — LOCKED

- **Budget:** Software & Tools. Two months of small steady charges, then a **$60K spike** — looks like an anomaly / error / fraud.
- **Truth:** it's the **expected annual renewal** of a core platform — legitimate, budgeted, only looks abnormal against a short 2-month window.
- **How the agent sees through it:** finds the **signed annual renewal contract** on file and *reads inside it* (despite a messy file name) to confirm the charge was expected. **Its silence must be earned by evidence, not luck** — so the synthetic company must contain that contract.
- **Verdict:** **stay silent.** Tests: can it tell a legitimate rare event from a genuine anomaly ("unusual ≠ wrong")?
- **Reads contents, not file names** — the "paralegal, not filing clerk" skill: opens a badly-named PDF and understands the meaning. (Evidence chosen = contract, over transaction history.)

> Analogy: your bank flags a $2K charge as possible fraud because it's abnormal — but it's your annual insurance premium, totally expected. A smart system recognizes the yearly pattern; a dumb one just screams "unusual."

### Seed 6 — Death by a thousand cuts + reconciliation — LOCKED

- **Budget:** Travel. Plan $80K, spent $55K (looks fine), but **~8 small scattered commitments** (trips booked-not-charged, conf regs approved over Slack, unsubmitted expenses) total ~$30K → true position $85K, over by $5K.
- **Verdict:** **flag early.** No villain — the overage exists only in the *sum* of many small things.
- **Skill tested = aggregation:** gather many small items from different messy places and total them, resisting "this $3K is nothing" ×8.
- **CRITICAL honesty rule (vs. Ramp Budgets / Fyle):** every item must be **pre-ledger** — NOT yet in any finance system. Ramp's real-time Budgets already sums recorded transactions (cards, reimbursements, bills, committed POs) beautifully. The *differentiated* skill is summing what **hasn't hit the ledger yet**. If any item is a recorded charge, it's cheating. Interview line: *"Budgets sums what's entered the system; my agent sums what hasn't — the trips booked-not-charged, the Slack approval nobody logged. Two different piles; the second is the one that blindsides you."*
- **Reconciliation wrinkle (the two-bucket test):** one earlier promise later becomes a real charge — the agent must **transfer it between buckets (keep total flat), not double-count**. Tests the core two-bucket world-model (see §8c).

> Analogy: vacation overspend — no single purchase blows it; a $15 lunch, $40 taxi, $30 souvenir, ×20, and you're way over, surprised, because nothing individually felt like a problem.

### Seed 7 — Borderline thread (the capstone) — LOCKED

- **Evidence:** a long (~15-message) **email thread** where a recruiting commitment **changes as it goes**: starts at $50K/two roles → "pause the second role" → "we might still want both, let me check" → trails off unresolved.
- **Truth (ground truth):** the correct answer is **NOT a dollar figure**. It's **"flag as uncertain, ask a human to confirm."** Real enough to matter, too unresolved to pin down.
- **Verdict:** must **not** confidently state $25K *or* $50K — false confidence is the failure. Correct behavior: surface it honestly ("a recruiting commitment, ~$25K–$50K depending on the last few messages, unresolved — confirm before I count it") and hand judgment to a person.
- **Why it's the capstone:** the only seed whose right answer is *calibrated uncertainty*, not a confident verdict. Tests a third failure mode beyond cry-wolf and miss: **false confidence** (bluffing a number). A finance agent that confidently invents numbers is *dangerous*. This is where every thread converges — reflection (doubts hard enough not to commit), Sheridan (drops a level), human-in-the-loop (fires here), precision-over-recall (flag uncertainty > assert a wrong number).
- **Hardest to author + grade:** the thread must be genuinely unresolvable; the rubric checks *appropriate* uncertainty (not overconfident, not uselessly wishy-washy).

> Analogy: a jury facing genuinely conflicting testimony with no tiebreaker. A bad juror picks a side on a coin-flip; a good one says "the evidence doesn't settle this beyond reasonable doubt." Knowing when evidence is insufficient is a higher skill than always producing an answer.

### Seed 8 — Drift over time (the "watching" seed) — LOCKED

**Different in shape from all others: a *sequence* of weekly snapshots, not one frozen moment.** This is the seed that closes the "everything is a snapshot" hole and realigns the set with the *proactive, watching* pitch.

- **Budget:** Sales, plan $120K. Four weekly readings: Wk1 $20K → Wk2 $45K → Wk3 $72K → Wk4 (now) $95K.
- **The trap:** at **no single week** does it cross any line — every frame is under the $120K plan. A snapshot agent says "79% spent, fine, stay quiet" on week 4. But the **rate** (~$25K/wk, slightly accelerating) means it breaches next week.
- **Verdict:** **flag early** — reason unlike any other seed: *not* "it's over" and *not* "hidden pile," but **"the rate of climb means it will breach soon — act now."** Produces a **forecast** ("~1 week to breach").
- **Why it's special:**
  - The **only seed a snapshot agent structurally cannot pass** — the danger exists only *between* frames, not in any one. Forces genuine watching-over-time.
  - Forces the **Memory** component + a repeating loop into the agent from day one (must remember prior weeks and compute the change). Can't be faked.
  - Produces the most **proactive-feeling** output — the forward forecast — which is the pitch made visible.
- **Stocks/flows framing (systems-thinking):** a snapshot reads the **stock** (level). Watching-over-time reads the **flow** (rate) — and a rate needs ≥2 points in time (freeze the clock and the rate vanishes). This seed tests reading the flow, not the stock.
- **Completes the "catch it early" picture with Seed 1:** Seed 1 = trouble *already committed but hidden*; Seed 8 = trouble *not committed yet but trending there*. Together = both ways a budget heads for a breach.
- **Build cost (honest):** needs time-series synthetic data (sequences of states) and rate-reasoning. "Over time" is really a *dimension* that could later be layered across all seeds (every seed has a slow vs. fast version) — but one dedicated drift seed proves the capability now; layering everywhere is a later enrichment.

> Analogy: blood pressure readings — 110, 120, 130. Any one is a shrug. The *climb* is the alarm. A good doctor treats the trend, not the single reading. Seeds 1–7 are single readings; Seed 8 is the chart.

---

## 14. Data model (build order: data model → synthetic data → agent → page)

Per the prototyping flow: **describe the data model up front** (it constrains the build and stops the AI going off the rails — "slow is smooth, smooth is fast"). Most of this was designed implicitly while building the seeds; here it's explicit. **Rule of thumb: never store a total that can go stale — compute it.**

**Lineage rule (applies to every entity):** every record carries an **`origin`** field — real-API vs. synthetic-file, and which source. Because the agent reasons over a *mix* of real (Gmail/Drive/QuickBooks) and synthetic data, when it behaves oddly you must be able to trace behavior back to its data. (Data-lineage confusion is a named synthetic-data risk.) *Add this to the schemas from the start — retrofitting it into every entity later is the exact rewrite the prototyping notes warn against.*

**Build-stack & modeling decisions (locked while building Seed 1's foundation):**
- **Stack: Python + Pydantic.** Schemas as Pydantic models (validation + free JSON-Schema export), data as plain language-agnostic JSON files (so the demo page can read them regardless of its own language), loader is a short Python script. Chosen because the heaviest work ahead — the agent + eval harness — lives most naturally in Python (the center of gravity), not the light demo page.
- **Billed portion = derived from linked transactions, never stored.** Commitment stores only its total signed amount; billed-so-far = sum of transactions linked to it; remaining = total − billed. (Bank-balance, not sticky-note — a stored total goes stale; a computed one can't. This is the two-bucket model made airtight.)
- **`confidence` means "how sure the agent is the commitment is real and for this amount" — nothing else.** It does NOT reflect how messy/hard-to-find the source was (that's the `source` field's job). Email-only but clear = 1.0. The only place confidence meaningfully drops is Seed 7 (genuine range, unresolved thread). Applied consistently across all seeds.

**Entity: Budget**
- name, owner, plan amount, period (which quarter + where we are in it)
- **does NOT store "amount spent"** — that's *derived* from transactions + commitments (two-bucket model). Store the plan; compute the actuals.

**Entity: Commitment** (the heart of the product — a single promise to spend)
- amount (see uncertainty note below), which budget it belongs to, **source** (where the evidence lives), **confidence** (how sure the agent is it read this correctly)
- **status** = the two-bucket model as data: `promised` (bucket 1) → `partly-billed` (split) → `paid` (bucket 2); plus `cancelled`, `uncertain`. **Reconciliation happens for free**: a promise becoming a charge is the *same* commitment changing status, not a new record → no double-count. (Analogy: one package moving ordered→shipped→delivered; you never count it twice.)

**Entity: Transaction** (money that actually moved)
- amount, date, vendor, which budget
- **links to the commitment it settles** (if any) — this link is what lets the agent "relieve" a promise instead of double-counting it. Matching a messy charge ("UNITED AIR 0162, $4,037") to a promise ("United, $4,000") is the hard sub-skill.

**Entity: Source** (where a commitment's evidence lives)
- type (ledger / contract-in-drive / email / Slack) + a **specific reference** (which document/thread), so the agent can *cite* what proved a commitment — not just a category.

**Entity: Reading / Snapshot** (a budget's state captured at a point in time)
- budget, timestamp, computed position. **A series of these = history = the ability to compute a rate.** Required for Seed 8 (watching over time). Without this entity, the agent is structurally a snapshot analyzer.

**Gap-fixes found by walking all 8 seeds against the model (explore-before-exploit):**
- **`recurring` flag** on commitments (how often it repeats) — Seeds 2 & 5 need "this renews annually" to reason/forecast.
- **`closed` vs. `active`** on a commitment/spend — Seed 4 needs "finished, no future spend" vs. "paid but ongoing."
- **amount as a possible range / with uncertainty** — Seed 7's answer is "$25K–$50K," not a single number.
- **Reading entity** (above) — Seed 8.
- **Transaction→Commitment link** (above) — Seed 6 reconciliation.

> These gaps were caught on paper *before* generating synthetic data — exactly the rewrite the prototyping notes warn about, avoided.

### 14a. Where the data lives (real systems) + the tool/MCP architecture

**A real 300-person VC-backed software company runs a *patchwork*, not one system** — and the patchwork IS the point:
- **Accounting / ERP** (actuals + general ledger): QuickBooks early, → NetSuite / an AI-native ERP (Campfire, Rillet) once funded.
- **Spend platform** (cards, expenses, bill pay — actuals + some open bills): Ramp / Brex / Bill.
- **Planning tool** (the plan; budget-vs-actual): Mosaic / Planful — or, very often, **Excel / Google Sheets**.
- **Contract storage** (commitments — badly): often **no real system** — a Google Drive folder, DocuSign, or email. (Contractbook exists; many don't use it.)
- **Procurement** (POs — maybe): Zip / Coupa at the larger end; a 300-person co. may just use **email + Slack**.

**The core insight the stack reveals — "commitments are the homeless entity."** Every other entity has one clean home (transactions → accounting/spend; budget/readings → planning). **Commitments have none** — they're scattered across contracts-in-a-drive, email, Slack, maybe a PO tool, and *partly in no system at all*. That's structural (tools track money that *moved* and *plans*; committed-but-unpaid falls between them), and it's *why the agent exists*: a human has to hunt across 5 systems, so they get blindsided. (Even new YC finance startups — Dimely, Dexter — are racing at exactly this: extracting commitments from Order Forms/MSAs/POs, finding off-contract spend.)

> Analogy: your *spending* is all on one bank statement (easy). Your future *obligations* are scattered — the lease PDF in email, the gym text, the verbally-okayed quote nowhere. The statement can't warn you; someone has to walk email + texts + documents and add them up. The agent is that someone, for a company.

**Architecture: the agent talks to everything through tools (MCP servers) — a uniform interface, exactly how Ramp's agents work.** Each entity has a "home tool":

| Tool | Feeds entity | Backed by |
|------|-------------|-----------|
| `get_transactions` | Transaction (actuals) | **Real** — QuickBooks free developer sandbox |
| `get_contracts` | Commitment (contracts) | **Real** — Google Drive API (messy, badly-named PDFs) |
| `get_emails` | Commitment (email deals) | **Real** — Gmail API (e.g. the Seed 7 thread) |
| `get_approvals` | Commitment (Slack approvals) | **Real** — Slack API (free workspace) |
| `get_budget`, `get_readings` | Budget, Reading | Synthetic file (or QuickBooks) |
| gatekept enterprise tools (NetSuite, Ramp API) | — | **Synthetic-backed** — don't fight vendor gatekeeping; these hold the *easy* clean actuals anyway |

- **The `Source` field becomes concrete:** it points at the tool + the specific document ("`get_contracts`, file: `PlatformCo_orderform_FINAL.pdf`") → this is how the agent *cites* its evidence.
- **Why this split works:** the gatekept tools (hard to get API access as an individual) hold the *commodity* actuals; the freely-accessible tools (Gmail/Drive/Slack) hold the *differentiating* messy commitments. The data you most need to be real is the data that's easiest to get real. 
- **This is NOT the risky BYOD:** these are *your own* mock accounts with *your own* fake data — zero customer, zero liability.

> Analogy: a detective walking a town of case files. Some buildings are real (you can walk in — Gmail, QuickBooks); some are cardboard movie-set fronts you built (the gatekept tools). The detective knocks and reads the same way at every door (the tool interface) and can't tell which is which.

**Build sequence — synthetic-first (de-risks the fiddly auth work):**
1. Build all tools as **synthetic-file readers first** (no auth) → get the whole agent working end-to-end on files you control → watch it produce a correct brief on Seed 1.
2. **Then** swap in the real APIs one at a time (Gmail → Drive → Slack → QuickBooks). The agent doesn't change — same tool interface, different backing. Auth (OAuth, tokens, rate limits) is real but bounded work; doing it *after* the logic is proven de-risks it.

---

## 14b. The demo & experience layer — what a visitor sees & the path to aha

**Shape:** a **landing page wrapped around a live demo** that runs on the synthetic company. Not a bare landing page (screenshots prove nothing — anyone can mock those). Not a full production product (no real integrations/customers needed). A **real engine on a test track**: the agent genuinely reads the fake contracts, does the two-bucket math, and produces the brief — but on movie-set data. *(This is why data model + synthetic data must come first: the live demo needs data to run on.)*

**Order by AHA, not by logic.** The logical order (problem → user → architecture → evals) buries the payoff behind setup and loses busy visitors. Invert it: punchline first, explanation below. (Trailer, not the movie.)

**The funnel (one scrolling page, each layer a satisfying exit point):**
- **Depth 0 — Hook (3 sec):** one headline + the *contrast image* — same budget shown as "30% spent, healthy (green)" vs. "127% committed (alarm), here's why." Book cover + blurb.
- **Depth 1 — THE AHA (30 sec):** the **live Seed 1 catch**. Northwind's budgets; Contractors looks fine at 30%; agent runs (auto or one obvious click) → brief appears → **the three contracts are listed so the visitor's own eyes verify it**. *Verification IS the aha.* **Minimize friction before this — no signup, no wall of text.** **Show it multi-budget (many, not one):** the agent stays quiet on the healthy ones and speaks on the one that isn't — that contrast is what proves *judgment* ("co-driver, not gauge"), not a threshold alarm.
- **Depth 2 — Judgment (2 min):** restraint. The 95% budget it ignores (Seed 4), the scary spike it clears (Seed 5), the messy thread where it says "I'm not sure — confirm" (Seed 7). Message: *"the hard part isn't catching problems, it's staying quiet on the scary-but-fine ones."*
- **Depth 3 — Rigor (5+ min):** the evals — precision/recall, the PR curve, the golden-dataset method. Few reach it on first visit; the serious evaluator does, and it's what closes the deal (nobody else shows this).
- **Close:** who you are, "how I built it," contact.

**Two entry doors (activation = supporting actions relative to the visitor's context):**
- **Portfolio browsers** land at the top and scroll the full funnel (they're in explore mode; light framing is welcome).
- **Resume / pitch links** drop **straight onto the live catch** with **one framing sentence** above it ("watch it catch an overspend three finance tools would miss") → near-zero supporting actions to the aha. Same page, different anchor.
- Keep the *one* framing line even for cold links — it "loads the gun" so the aha fires; cut the scroll-past-the-hero, not the sentence that makes 127% land.

**Sandbox** = optional "try it yourself" toy **low on the page**, after they're convinced. Story first, play second. Lead with it and a cold visitor pokes a random budget they can't interpret. **The guided scroll is the "pilot's exam" — it *proves correctness* on the golden set. The sandbox proves nothing** — it makes **no correctness claims** (only the golden set is "proven"). Good evals mean sensible inputs land in already-tested territory; **guardrails** (sliders/dials within sane ranges) fence off absurd inputs.

> The guided walkthrough IS the scroll (the tour guide); the live demos are the exhibits (the real product). Landing page = connective tissue between real demos.

---

## ACT III — GTM / Growth / Monetization (thin — noted, not built)

- **Minimum Viable Performance:** a precision/recall threshold. **[TBD.]**
- **Aha:** the brief. (Done.)
- **Monetization (one-liner to carry):** rides Ramp's model — more trust → more spend on the platform → interchange + software revenue.

---

## 15. Positioning / framing

- **The artifact's real claim (the one thesis under everything):** not "here's a novel product," but **"here's proof I build and evaluate at your team's senior bar — audit it."** Every section repeats this one confident move: concede what isn't the point (the idea), and reframe the rigor as the reviewer's audit kit.
- **To Ramp:** "I built the kind of spend-judgment agent your Policy Agent is, held to a higher eval bar."
- **To Warp:** "Your compliance agent watches tax jurisdictions and drafts a resolution for a human to approve. I built the same shape watching budget commitments — catching the overspend a stretched finance team would miss and staging the fix for approval. Same trust architecture, different stream."
- **Never claim novelty or "a gap they missed."** Cover-band framing: it proves musicianship, not authorship. Ramp shipping similar work (Q2 2026) *validates* the direction.
- **Category-read point:** two dream companies (Ramp, Warp) independently converged on watch → catch → draft → human-approves; Sid reasoned to it from frameworks. Shows he reads where the category is going.

---

## 16. Guardrails / recurring discipline

- **Honesty over phantom claims** (Sagan standard). Never overclaim what evals or the agent can do.
- **Every number traceable** (e.g. $380K = $90K + $290K). If a reviewer asks "where'd that come from," walk it down to the parts.
- **Movie set, not a real town** — build only what the demo's "camera" sees; everything else stays plywood.
- **Quality propagates** — a sloppy seed becomes 15 sloppy cases. Seeds are hand-built and airtight before mutation.
- **Build order:** golden dataset (seeds) FIRST, before the agent. Dataset + evals sit at the top of the priority order.

---

## 17. Open questions / TBD

- [x] ~~Which seed to build next~~ → **Seed 4 (restraint)** — decided.
- [x] ~~Seed 1 recruiter as email-only~~ → **LOCKED**.
- [x] ~~All seven seeds designed~~ → **DONE: eight seeds** (1–8 locked at the numbers/logic level; Seed 8 = drift-over-time).
- [ ] **Agent now requires a Memory component + repeating loop** (to watch over time / compute rates) — Seed 8 forces this. Build it in from the start, don't bolt on.
- [ ] **Next phase: build the synthetic data** — fake contracts, email threads, budget/transaction records, and **time-series sequences** (for Seed 8). Start with one hand-written seed contract for Seed 5, then mutate. Documents must be believably *messy*, not clean.
- [ ] Minimum Viable Performance numbers (precision/recall thresholds).
- [ ] Exact fix the agent stages — reforecast vs. freeze/tighten vs. flag-commitment. *(Lean: reforecast.)*
- [ ] Real company name (Northwind = placeholder).
- [ ] Seed mutation count (the "~15/seed" figure is a placeholder — set it by what makes precision/recall trustworthy).

---

## 18. Decision log

| Date | Decision | Note |
|------|----------|------|
| 2026-07-06 | Target = Generalist/AIPM-growth at Ramp; artifact is a capability demo, not a novel thesis | "Cook their signature dish better" |
| 2026-07-06 | Product = proactive committed-spend agent; silent by default | Co-driver, not gauge |
| 2026-07-06 | Human sits on the FIX (Sheridan 5), not the diagnosis | Matches Ramp/Warp |
| 2026-07-06 | Golden dataset is the spine; built before the agent | Seed-and-mutate |
| 2026-07-06 | Ground truth authored by Sid; agents stress-test only | Keeps evals honest |
| 2026-07-06 | Seed 1 (flagship) locked pending recruiter detail | Northwind, Contractors budget, 127% |
| 2026-07-06 | Seed 6 = messy evolving email thread (calibration test) | Turns the "hard part" fear into the best test |
| 2026-07-06 | Warp added as second target (same artifact, different framing) | Both converged on same agent shape |
| 2026-07-06 | Seed 1 recruiter FULLY LOCKED as email-only, never-logged commitment | Most realistic detail + demonstrates the pile-3 edge |
| 2026-07-06 | Build Seed 4 (restraint) next, not Seed 2 | Seed 4 defends the differentiator (proves it's not a dumb alarm); Seed 2 only refines timing/tone |
| 2026-07-06 | Expanded to **seven seeds**: split restraint into two (near-the-limit + abnormal-but-fine) | Two different false alarms test different reasoning; restraint is the differentiator, worth doubling down. Seed count stays flexible. |
| 2026-07-06 | Documented the build loop (§12f): run→fail→fix; tune on seeds, test on mutations; watch precision+recall together | The "how it's actually made to work + generalize" rigor a reviewer wants to see |
| 2026-07-06 | Seed 4 (restraint / near-the-limit) FULLY LOCKED | Mirror of Seed 1: Marketing at 95% but closed-out campaign, ~zero forward commitments → stay silent |
| 2026-07-06 | Restraint = the reflection step; tuning it = the precision/recall dial (§8b) | Names *where* in the agent restraint lives |
| 2026-07-06 | Seeds 3 & 5 LOCKED (healthy control; abnormal-but-fine renewal) | Seed 5 silence must be earned by a readable contract, not luck |
| 2026-07-06 | Seed 2 LOCKED as the single too-late case | One is seasoning — keeps the set honest, tests brace-vs-prevent |
| 2026-07-06 | Seed 6 LOCKED; all items must be **pre-ledger**; + two-bucket reconciliation wrinkle (§8c) | Keeps it honestly different from Ramp Budgets / Fyle (which sum *recorded* spend) |
| 2026-07-06 | Seed 7 LOCKED as the capstone: correct answer = *calibrated uncertainty*, not a number | Tests false-confidence — the third, most dangerous failure mode |
| 2026-07-06 | **All 7 seeds designed.** Next phase = synthetic data (docs/threads/records) | Seed-and-mutate extends to documents, not just numbers |
| 2026-07-06 | Added **Seed 8 (drift over time)** to close the snapshot hole | Only seed a snapshot agent can't pass; forces the **Memory** component + loop; produces the forecast. "Over time" is a dimension layerable across all seeds later. |
| 2026-07-06 | Made the **data model explicit** (§14); walked all 8 seeds against it and fixed gaps | Budgets compute (don't store) actuals; Commitment.status = two-bucket; added Reading entity, recurring flag, txn→commitment link, uncertain/range amount. Caught rewrites on paper. |
| 2026-07-06 | Locked the **demo & experience layer** (§14b): landing page wrapped around a live demo on synthetic data; aha-first funnel; two entry doors | Resume/pitch links drop straight onto the live catch w/ one framing line; portfolio browsers scroll the funnel. Sandbox = optional toy, low on page. Merged the old "two stations" note in here so the demo is described once. |
| 2026-07-06 | **Tool/MCP architecture + "commitments are the homeless entity"** (§14a); real accounts (Gmail/Drive/Slack/QuickBooks sandbox) behind MCP tools, synthetic-backed for gatekept enterprise tools | Uniform tool interface = Ramp-flavored; the freely-accessible tools hold the *differentiating* messy commitments. Not BYOD (own mock data, zero liability). |
| 2026-07-06 | **Build sequence = synthetic-first**, then swap in real APIs one at a time | Get the agent working end-to-end on files first; de-risks the fiddly OAuth work by doing it after the logic is proven. |
| 2026-07-06 | Folded in synthetic-data brief: **lineage `origin` field on every entity** (data-model rule); named mutation techniques (self-instruct for structured, back-translation via structurally-distant language for docs); **engineer diversity deliberately**; never delete high-disagreement cases | Guards against data-lineage confusion + "narrowness masquerading as coverage." Lineage touches the schema task NOW; the rest is synthetic-data-phase guidance. |
| 2026-07-06 | **Project named "Lookout"** | Names the differentiator (watchful restraint), not the problem. Sells the thesis in one word. |
| 2026-07-06 | Build decisions (Seed 1 foundation): **Python + Pydantic**; **billed derived from linked transactions** (not stored); **confidence = certainty of the commitment, not source-messiness** | Stack serves the agent+eval center of gravity; derive-don't-store keeps two-bucket airtight; clean confidence rule reserves the real drop for Seed 7. Seed 1 foundation built & verified — 127% falls out of the data, no-double-count invariant holds. |
| 2026-07-06 | Agent build decisions: **default model Sonnet 5** (configurable to Opus for the flagship demo run); **`compute_position` as a tool** (math in code, agent calls it) | Cheaper default proves the intelligence is in the *design* not the horsepower (marginal ROI); math-as-a-tool keeps everything through the uniform tool interface + keeps reasoning step-evaluable. |
| 2026-07-06 | **Seed 1 built & verified**; brief iterated to forceful + honest + clean; **`validate.py` = code-enforced honesty guarantee** | Prompt rules are probabilistic; the no-fabrication guarantee had to live in code (§12g). Money = `Decimal`. |
| 2026-07-06 | **Seed 4 built & verified**; sharpened so `closed` is decisive; **hybrid: code owns the number, agent explains the exclusion** | Found the "code silently pre-digests judgment" trap (§12h) — surfacing the excluded $30K makes restraint reasoning visible + gradeable. |
| 2026-07-06 | **Honesty has two layers** (§12g): provenance (built, code) + semantic accuracy (later, rubric). Added rubric criterion "numbers correctly labeled" | Seed 4's "$6,000 swing" mislabel — real number, wrong concept — passes the validator but is semantically wrong; only a rubric/LLM-judge catches it. |
| 2026-07-06 | Confirmed build order: **data model → synthetic data → agent → page** | The live demo needs data to run on; this is why the data model comes first |
| 2026-07-06 | **Reframed the "real enemy" (Juicebox lens):** the true competitor is the human reflex of *asking budget owners directly*, not another tool | Wins on certainty but doesn't scale; agent = automating that reflex + being the safety net under it. Sharper, more defensible, credits what finance teams actually do. |
| 2026-07-06 | **Sharpening pass (QBQ + FSE, senior posture):** reframed rigor as the reviewer's *audit kit*; added one thesis — "audit that I build at your bar, not that the idea is novel" | Deepak: "juniors ask, seniors hypothesize" + "do the mental math silently, then speak." Applied to differentiation, target-user, evals, positioning. |