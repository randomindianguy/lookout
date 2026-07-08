# Lookout — Data foundation (Seed 1, Northwind)

The synthetic-first data layer for **Lookout** (the committed-spend agent): the
five entities as schemas and Seed 1 expressed in them. This is the foundation
the tools (`tools.py`) and the reasoning agent (`agent.py`) read from.

## Files

| File | What it is |
|------|-----------|
| `schemas.py` | The five entities as Pydantic models + shared `Origin`, `Amount`, and enums. Shared across all seeds. |
| `seeds/seed01_northwind/budgets.json` | The Contractors & Professional Services budget ($300K plan). |
| `seeds/seed01_northwind/commitments.json` | The three commitments (design agency, dev shop, recruiter). |
| `seeds/seed01_northwind/transactions.json` | The $90K of actuals (the billed portions of two commitments). |
| `seeds/seed01_northwind/sources.json` | Where each commitment's evidence lives (contract / contract / email). |
| `seeds/seed01_northwind/readings.json` | One computed-position snapshot (single-snapshot per Seed 1). |
| `load_seed.py` | Loads the data, computes the true position live, prints the brief, cross-checks the reading. |

## Run it

```bash
python3 load_seed.py            # defaults to Seed 1
```

Prints the true-position brief and shows **$380K / $300K = 127%** computed from
the primitives — not hard-coded anywhere.

## The five entities (PRD §14)

- **Budget** — name, owner, plan amount, period. Stores the plan only; actuals
  are always computed, never stored.
- **Commitment** — a single promise to spend: amount (range-capable), budget,
  status (promised / partly-billed / paid / cancelled / uncertain), source
  pointer, confidence, `recurring` flag, `lifecycle` (active / closed). Stores
  the total signed amount only; the billed portion is derived.
- **Transaction** — money that moved: amount, date, vendor, budget, and a link
  to the commitment it settles.
- **Source** — type (ledger / contract / email / slack) + a specific reference,
  so the agent can cite its evidence.
- **Reading** — a budget's computed position at a timestamp. A series enables
  watching over time (Seed 8).

Every record carries an **`origin`** field (real-api vs synthetic-file + which
source) for lineage — added from the start, not retrofit.

## Two design rules encoded

1. **Never store a total that can go stale — compute it.** Budget has no
   amount-spent; Commitment has no billed/remaining. Both are derived.
2. **Two-bucket model (no double-count).** A charge is a *transfer* from the
   promised bucket to the paid bucket, not new money. `committed_remaining` for
   each commitment = signed amount − billed (billed = sum of linked
   transactions). The loader verifies actuals == sum of billed portions, so no
   dollar is counted twice.

## How 127% is built (every number traceable)

```
paid (actuals)        = $60K (design) + $30K (dev) + $0 (recruiter) = $90K
promised (remaining)  = ($180K−$60K) + ($150K−$30K) + ($50K−$0)     = $290K
true position         = $90K + $290K                                = $380K
% of plan             = $380K / $300K                               = 127%
```

The recruiter's $50K exists only as an email, never logged in the finance tool —
the "pile 3" edge a normal dashboard never sees.

## Deliberate simplifications (from the Seed 1 spec)

Round numbers, single snapshot, one transaction per billed commitment, clean
source separation. The mechanism works identically on messy real numbers.

## Scope note

Seed 1 names six budgets but only assigns figures to Contractors, so only that
budget is modeled here (guarding against inventing numbers the PRD doesn't
specify). The other seeds' budgets slot into the same `seeds/<seed>/` shape.
