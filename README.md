# Lookout

A committed-spend agent that watches a finance team's budgets and catches money that's **promised but not yet paid** — the signed contracts and email handshakes that make a healthy-looking budget secretly over plan. It stays silent on the budgets that are genuinely fine.

This is a capability demo, not a product pitch: a worked example of how I build and evaluate an AI agent, using a committed-spend finance agent as the case study. The question it answers isn't "is Lookout a business," it's "can I build and evaluate agents at a senior bar." Everything here is meant to be audited. It runs entirely on synthetic data, so it costs nothing to run and every number is verifiable against the data it reads.

## The demo

Open `index.html` in a browser. It is a self-contained page — no build, no server, no live API calls — that replays the agent's real, saved outputs:

- **The catch.** A budget that looks 30% spent is actually at 127%; the three commitments are listed so you can verify it yourself.
- **The judgment.** The scary-looking budgets it correctly stays silent on, and the uncertain case where it says "I can't call this, confirm it."
- **The eval.** Precision/recall, the confusion matrix, and the method — led by the honest caveat that the reported numbers are a single-pass *fallback*: the planned multi-pass stability run hit a hard budget ceiling and 334 agent runs died on a credit wall.

## Architecture — the decisions, and why

- **Sheridan Level 5 autonomy.** The agent diagnoses; a human approves the fix. The math can be automated, but the decision to cut a vendor or defer scope belongs to the controller.
- **Code owns the math and the honesty; the model owns judgment and language.** Prompts persuade, code enforces. Every figure in a brief comes from one two-bucket function (`position.py`), and `validate.py` rejects any number in a brief that does not trace to a tool output. The model is never allowed to do arithmetic.
- **Single loop, deliberately.** One agent, one environment. Multi-agent buys coordination failure modes this problem does not have.
- **Two-bucket money model.** Paid vs committed, tracked apart. A charge landing is a transfer between buckets, not new spend — which is what stops the double-counting that makes naive "sum the spend" tools quietly wrong.

The agent reaches data only through the tools in `tools.py`, behind a `DataSource` interface, so swapping the synthetic files for real APIs (QuickBooks, Gmail, Drive) later changes nothing in the agent.

## The golden dataset and the eval

The dataset is the spine, and it was built before the agent:

- **8 hand-authored seeds** (`src/seeds/`), each at a deliberate point — a hidden-commitment catch, restraint cases (scary-but-fine), a calibrated-uncertainty case, a drift-over-time case.
- **120 mutations** (`src/mutations/`), template-generated with machine-verified labels, including **boundary pairs**: near-identical cases with the opposite correct answer, differing in one decisive fact. That is the generalization test — a passing score cannot be memorization.
- **A neuro-symbolic grader** (`src/grader.py`): code hard-gates the objective failures (a fabricated number or the wrong budget is an automatic fail); an Opus judge decides intent. Verdicts are PASS / PARTIAL / FAIL with a written rationale, never a scalar. The grader was validated against my own hand-labels before it was trusted.

**Result (single-pass):** 94.5% precision, 100% recall across 128 cases (confusion matrix TP 69 / FP 4 / FN 0 / TN 55), over the launch floors of 0.70 / 0.60.

**Stated honestly:** these numbers are a single-pass *fallback*, not the run I planned. The plan was a tiered stability run — three passes on every case, four more on any case whose verdict or grade wobbled — because one pass tells you a score and three tell you whether the score is stable. It hit a hard budget ceiling mid-execution: 334 agent runs died on a credit wall. So each case was scored on the first pass that completed, which makes these point estimates with real error bars, not a settled statistical result. Fourteen cases did finish all three passes before the money ran out; thirteen were stable, and one stay-silent case (`seed03_facilities`, label SILENT) came back SILENT twice and UNCERTAIN once — a hint, not a measurement, that the agent is steadier when it catches than when it holds back. The four false positives are one coherent failure mode — crying wolf on an under-plan budget with a surprise commitment — which I flagged as an untested edge during the build and the eval then confirmed. Nothing was tuned to flatter the score, and the run scored for each case was chosen by code that never sees the label.

## The raw run artifacts (`eval/`)

The eval directory holds the unedited run records — credit errors and all — so every number above is auditable against the files it came from:

- **`agent_records.jsonl`** (496 lines) — every agent run that was *attempted*, three to four per case. Each line is one run: its case id, the agent's verdict, and either the brief it produced or the error that killed it. This is where the 334 credit-wall failures live, interleaved with the runs that completed. The three-to-four-per-case count is the residue of the tiered plan: a base of three passes each, plus extra passes on cases that wobbled, most of which never finished before the budget ran out.
- **`scoring_v3_results.jsonl`** (128 lines) — one line per case: the single run that was scored, with its grade. The reported precision/recall is computed from this file.
- **`scoring_results.jsonl`** (71 lines) — an earlier, partial scoring pass, kept as-is for the record.

**How the one scored run per case is picked.** For each case the harness takes the *first non-ERROR run in file order* — the first pass that did not crash — and when choosing it never looks at the ground-truth label, the agent's verdict value, or whether the run passed the code gate. The selection logic (from the scoring harness, `scoring_v3.py`, which produced these outputs but is **not** committed to this repo):

```python
banked = {}
for line in AGENT_JL.read_text().splitlines():
    if line.strip():
        r = json.loads(line)
        if r.get("agent_verdict") != "ERROR" and r["cid"] not in banked:
            banked[r["cid"]] = r          # keep the first surviving run per case
todo = [cid for cid in cases if cid not in banked]   # cases with no survivor: re-run once
```

The rule is label-blind by construction, and the output corroborates it. For all 128 cases, the scored record reproduces the first non-ERROR record for that case in `agent_records.jsonl` on both fields the agent produces — the same `agent_verdict` and a byte-identical complete `brief` (not just the head) — with zero exceptions. For the 14 cases that have three or more non-ERROR runs, the selected run was the first record in file order in every case, including `seed03_facilities`, where a SILENT first run was taken over a later UNCERTAIN. This is reproducible directly from the two JSONL files in this repo, without trusting the missing harness.

## Repository layout

```
.
├── index.html             # the self-contained demo page
├── docs/                  # PRD + the AI-product-lifecycle framework it is built on
└── src/
    ├── agent.py           # the Anthropic tool-use loop (LLM judgment, code math)
    ├── tools.py           # the tools the agent reaches data through (DataSource seam)
    ├── position.py        # two-bucket math, the single source of truth for every figure
    ├── schemas.py         # Pydantic entities (money as Decimal, never float)
    ├── validate.py        # rejects any brief number not traceable to a tool
    ├── grader.py          # neuro-symbolic eval grader (code gates + Opus judge)
    ├── load_seed.py       # loads a seed and cross-checks the recomputed position
    ├── seeds/             # 8 hand-authored golden scenarios
    └── mutations/         # 120 machine-verified mutations (boundary pairs)
```

## Running it

```bash
pip install -r requirements.txt
cp src/.env.example src/.env      # then add your ANTHROPIC_API_KEY

python src/load_seed.py           # offline: load Seed 1, verify the two-bucket math
python src/agent.py               # run the agent on Seed 1 (uses the API)
python src/agent.py seeds/seed04_marketing   # or another seed (path is relative to src/)
```
