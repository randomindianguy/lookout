"""
load_seed.py — load a seed's synthetic data and print its true position.

The whole point: watch 127% FALL OUT of the data (plan + transactions +
commitments), not be hard-coded anywhere. The math comes from position.py — the
same function the agent's compute_position tool and the future eval harness use,
so there is a single source of truth for every number.

Usage:
    python load_seed.py                       # defaults to Seed 1 (Northwind)
    python load_seed.py seeds/seed01_northwind
"""

from __future__ import annotations

import json
import sys
from decimal import Decimal
from pathlib import Path

from position import compute_position
from schemas import (
    Budget,
    Commitment,
    Reading,
    SeedDataset,
    Source,
    Transaction,
)

DEFAULT_SEED = str(Path(__file__).parent / "seeds" / "seed01_northwind")


def _load_list(path: Path, model):
    with path.open() as f:
        # parse_float=Decimal so money never passes through a float
        raw = json.load(f, parse_float=Decimal)
    return [model(**item) for item in raw]


def load_seed(seed_dir: Path) -> SeedDataset:
    """Load and validate all five entity files for one seed."""
    return SeedDataset(
        budgets=_load_list(seed_dir / "budgets.json", Budget),
        commitments=_load_list(seed_dir / "commitments.json", Commitment),
        transactions=_load_list(seed_dir / "transactions.json", Transaction),
        sources=_load_list(seed_dir / "sources.json", Source),
        readings=_load_list(seed_dir / "readings.json", Reading),
    )


def usd(x) -> str:  # x is a Decimal (money) or float (ratio); both format fine
    return f"${x:,.0f}"


def print_brief(dataset: SeedDataset) -> None:
    budget = dataset.budgets[0]
    pos = compute_position(
        budget, dataset.commitments, dataset.transactions, dataset.sources
    )
    plan = pos["plan_amount"]

    print("=" * 68)
    print(f"TRUE-POSITION BRIEF  —  {budget.name}")
    print(f"Owner: {budget.owner}")
    print(f"Period: {budget.period.label}  ({pos['months_elapsed']} of "
          f"{pos['months_total']} months in, as of {pos['as_of']})")
    print("=" * 68)

    print()
    print(f"  Plan:               {usd(plan)}")
    print(f"  SURFACE (paid):     {usd(pos['actuals_paid'])}   -> looks "
          f"{pos['surface_pct']:.0%} spent, comfortable")
    print()
    print("  The hidden pile (committed but not yet paid):")
    for ln in pos["commitment_lines"]:
        cite = f"{ln['source_type']}:{ln['source_reference']}"
        print(f"    - {ln['vendor']:<20} signed {usd(ln['signed'])}, "
              f"billed {usd(ln['billed'])}  ->  {usd(ln['remaining'])} owed")
        print(f"        status={ln['status']}  confidence={ln['confidence']:.0%}  "
              f"source=[{cite}]")
    print(f"    {'':<20} committed remaining total:      "
          f"{usd(pos['committed_remaining'])}")

    print()
    print("  Two buckets:")
    print(f"    already-paid          {usd(pos['actuals_paid'])}")
    print(f"    promised-not-paid   + {usd(pos['committed_remaining'])}")
    print(f"    {'-' * 34}")
    print(f"    TRUE POSITION       = {usd(pos['true_position'])}   "
          f"vs {usd(plan)} plan  =  {pos['pct_of_plan']:.0%}")
    print()
    verdict = "OVER" if pos["over_under"] > 0 else "under"
    print(f"  >>> {verdict} plan by {usd(abs(pos['over_under']))}  "
          f"({pos['pct_of_plan']:.1%} of plan), none of it hit the account yet.")
    print()

    # --- lineage / no-double-count checks ---------------------------------- #
    total_billed = sum(ln["billed"] for ln in pos["commitment_lines"])
    print("  Checks:")
    print(f"    - actuals ({usd(pos['actuals_paid'])}) == sum of billed portions "
          f"({usd(total_billed)}): {pos['actuals_paid'] == total_billed}  "
          f"(no dollar counted twice)")

    # use the LATEST reading (a budget may have a time-series of them)
    budget_readings = [r for r in dataset.readings if r.budget_id == budget.id]
    reading = max(budget_readings, key=lambda r: r.timestamp) if budget_readings else None
    if reading is not None:
        rp = reading.position
        tp_match = abs(rp.true_position - pos["true_position"]) < 0.01
        pct_match = abs(rp.pct_of_plan - pos["pct_of_plan"]) < 0.001
        print(f"    - recomputed true position ({usd(pos['true_position'])}) matches "
              f"stored reading ({usd(rp.true_position)}): {tp_match}")
        print(f"    - recomputed pct ({pos['pct_of_plan']:.4f}) matches stored reading "
              f"({rp.pct_of_plan:.4f}): {pct_match}")
    print("=" * 68)


def main() -> None:
    seed_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(DEFAULT_SEED)
    if not seed_dir.is_absolute():
        seed_dir = Path(__file__).parent / seed_dir
    dataset = load_seed(seed_dir)
    print_brief(dataset)


if __name__ == "__main__":
    main()
