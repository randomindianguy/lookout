"""
tools.py — the tools the agent calls to reach data.

Part 1 of the build. The agent talks to data ONLY through these tools:
    get_budget, get_transactions, get_commitments, get_readings, compute_position

Forward-compatibility is the whole design goal. Each tool reads through a
`DataSource` interface. Today the only implementation is
`SyntheticFileDataSource` (reads Seed 1's JSON). Later, `QuickBooksDataSource`,
`GmailDataSource`, `DriveDataSource`, or messy-document extractors implement the
SAME interface and return the SAME shapes — so the tools and the agent never
change when the backing is swapped for real APIs.

`compute_position` is the one tool that does arithmetic; it delegates to
position.py (the single source of truth) so the LLM never computes numbers.
"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import List, Optional

from position import compute_position as _compute_position
from position import compute_trajectory as _compute_trajectory
from schemas import Budget, Commitment, Reading, Source, Transaction

DEFAULT_SEED = Path(__file__).parent / "seeds" / "seed01_northwind"


# --------------------------------------------------------------------------- #
# Serialization helper (works on Pydantic v1 and v2, enums -> their values)
# --------------------------------------------------------------------------- #

def _dump(model) -> dict:
    if hasattr(model, "model_dump"):          # Pydantic v2
        return model.model_dump(mode="json")
    return json.loads(model.json())           # Pydantic v1


# --------------------------------------------------------------------------- #
# The data-source interface (this is the seam the real APIs slot into)
# --------------------------------------------------------------------------- #

class DataSource:
    """Interface every tool reads through. Swap the implementation to change the
    backing (synthetic file -> QuickBooks/Gmail/Drive/messy-doc extractor)
    without touching the tools or the agent."""

    def budgets(self) -> List[Budget]:
        raise NotImplementedError

    def commitments(self, budget_id: Optional[str] = None) -> List[Commitment]:
        raise NotImplementedError

    def transactions(self, budget_id: Optional[str] = None) -> List[Transaction]:
        raise NotImplementedError

    def readings(self, budget_id: Optional[str] = None) -> List[Reading]:
        raise NotImplementedError

    def sources(self) -> List[Source]:
        raise NotImplementedError


class SyntheticFileDataSource(DataSource):
    """Reads a seed's JSON files. The clean-data-first backing: no auth, no APIs,
    no messy-document parsing yet — just the structured Seed 1 data."""

    def __init__(self, seed_dir=DEFAULT_SEED):
        self.seed_dir = Path(seed_dir)
        self._budgets = self._load("budgets.json", Budget)
        self._commitments = self._load("commitments.json", Commitment)
        self._transactions = self._load("transactions.json", Transaction)
        self._readings = self._load("readings.json", Reading)
        self._sources = self._load("sources.json", Source)

    def _load(self, filename: str, model):
        with (self.seed_dir / filename).open() as f:
            # parse_float=Decimal so money never passes through a float
            raw = json.load(f, parse_float=Decimal)
        return [model(**item) for item in raw]

    def budgets(self) -> List[Budget]:
        return list(self._budgets)

    def commitments(self, budget_id: Optional[str] = None) -> List[Commitment]:
        if budget_id is None:
            return list(self._commitments)
        return [c for c in self._commitments if c.budget_id == budget_id]

    def transactions(self, budget_id: Optional[str] = None) -> List[Transaction]:
        if budget_id is None:
            return list(self._transactions)
        return [t for t in self._transactions if t.budget_id == budget_id]

    def readings(self, budget_id: Optional[str] = None) -> List[Reading]:
        if budget_id is None:
            return list(self._readings)
        return [r for r in self._readings if r.budget_id == budget_id]

    def sources(self) -> List[Source]:
        return list(self._sources)


# --------------------------------------------------------------------------- #
# The tools (agent-facing). Each returns JSON-serializable data.
# --------------------------------------------------------------------------- #

def get_budget(ds: DataSource, budget_id: Optional[str] = None) -> list:
    """List budgets (all, or the one matching budget_id). Returns plan/owner/
    period — never a stored amount-spent (that's computed)."""
    budgets = ds.budgets()
    if budget_id is not None:
        budgets = [b for b in budgets if b.id == budget_id]
    return [_dump(b) for b in budgets]


def get_transactions(ds: DataSource, budget_id: str) -> list:
    """Actuals (money that has actually moved) for a budget, each with a link to
    the commitment it settles, if any."""
    return [_dump(t) for t in ds.transactions(budget_id)]


def get_commitments(ds: DataSource, budget_id: str) -> list:
    """Commitments (promises to spend) for a budget — the signed amount, status,
    confidence, and a pointer to the source that evidences each."""
    return [_dump(c) for c in ds.commitments(budget_id)]


def get_readings(ds: DataSource, budget_id: str) -> list:
    """Historical computed-position snapshots for a budget (a series enables
    watching over time). Seed 1 has a single reading."""
    return [_dump(r) for r in ds.readings(budget_id)]


def compute_position(ds: DataSource, budget_id: str) -> dict:
    """Authoritative two-bucket math for a budget: paid, committed-remaining,
    true position, percentage, and a per-commitment breakdown. This is where ALL
    arithmetic happens — the agent must use these numbers rather than computing
    its own. Delegates to position.py (single source of truth)."""
    budget = next((b for b in ds.budgets() if b.id == budget_id), None)
    if budget is None:
        return {"error": f"no budget with id {budget_id!r}"}
    return _compute_position(
        budget, ds.commitments(), ds.transactions(), ds.sources()
    )


def get_trajectory(ds: DataSource, budget_id: str) -> dict:
    """Read the SEQUENCE of a budget's readings over time and surface the trend:
    the actual per-reading numbers (the weekly climb), the reading-over-reading
    deltas, an average rate, and a forward forecast (projected next reading, whole
    periods until it reaches plan). Use this when a budget has more than one
    reading — a budget can be UNDER plan at every single snapshot yet be climbing
    toward a breach; the danger is in the rate, not any one frame. Reason over the
    sequence yourself; the numbers here are the reliable, code-computed math."""
    budget = next((b for b in ds.budgets() if b.id == budget_id), None)
    if budget is None:
        return {"error": f"no budget with id {budget_id!r}"}
    return _compute_trajectory(budget, ds.readings())


# --------------------------------------------------------------------------- #
# Tool registry — names, Anthropic input schemas, and dispatch. The agent reads
# this so tools can be added/swapped in one place.
# --------------------------------------------------------------------------- #

TOOL_SPECS = [
    {
        "name": "get_budget",
        "description": (
            "List budgets and their plan, owner, and period (which quarter and "
            "how far into it). Does not include amount-spent — that is computed. "
            "Call with no budget_id to see all budgets, or pass one to fetch it."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "budget_id": {
                    "type": "string",
                    "description": "Optional budget id to filter to one budget.",
                }
            },
            "required": [],
        },
    },
    {
        "name": "get_commitments",
        "description": (
            "Get the commitments (promises to spend) for a budget: each vendor, "
            "signed amount, status (promised/partly-billed/paid/cancelled/"
            "uncertain), confidence, and the source that evidences it."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "budget_id": {"type": "string", "description": "Budget id."}
            },
            "required": ["budget_id"],
        },
    },
    {
        "name": "get_transactions",
        "description": (
            "Get the actuals (money that has actually moved) for a budget. Each "
            "transaction may link to the commitment it settles."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "budget_id": {"type": "string", "description": "Budget id."}
            },
            "required": ["budget_id"],
        },
    },
    {
        "name": "get_readings",
        "description": (
            "Get historical computed-position snapshots for a budget (a time "
            "series). Seed 1 has a single reading."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "budget_id": {"type": "string", "description": "Budget id."}
            },
            "required": ["budget_id"],
        },
    },
    {
        "name": "compute_position",
        "description": (
            "Compute a budget's AUTHORITATIVE true position with the two-bucket "
            "model: already-paid + committed-but-unpaid vs. plan, plus the "
            "percentage of plan, the surface percentage a dashboard shows, a "
            "per-commitment breakdown, and per-source subtotals "
            "(committed_remaining_by_source, e.g. all contracts combined vs. the "
            "email-only pile). It also returns excluded_commitments: closed or "
            "cancelled items whose signed-but-unbilled remainder is deliberately "
            "NOT in the true position (finished/won't be spent), each with its "
            "signed-vs-billed gap and the reason. Use these numbers directly — "
            "including the subtotals — and do not add, combine, or derive any "
            "number yourself."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "budget_id": {"type": "string", "description": "Budget id."}
            },
            "required": ["budget_id"],
        },
    },
    {
        "name": "get_trajectory",
        "description": (
            "For a budget with a TIME-SERIES of readings, surface the trend over "
            "time: the sequence of per-reading true positions, the reading-over-"
            "reading deltas (the climb), the RECENT rate (recent_rate, the latest "
            "interval's change — the current pace), the whole-window average "
            "(avg_rate_per_period, reference only), a trend label (steady / "
            "accelerating / flattening / flat_or_declining), and a forecast run "
            "off the RECENT pace: projected_next_period and periods_to_breach. "
            "A budget can be UNDER plan at every reading yet be climbing toward a "
            "breach (flag), OR it can have climbed steeply and then FLATTENED so "
            "it won't breach (silent). Judge from the recent rate / deltas / trend "
            "— NOT the average, which stays scary even after a budget levels off. "
            "Call this whenever get_readings shows more than one reading."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "budget_id": {"type": "string", "description": "Budget id."}
            },
            "required": ["budget_id"],
        },
    },
]

TOOL_DISPATCH = {
    "get_budget": get_budget,
    "get_commitments": get_commitments,
    "get_transactions": get_transactions,
    "get_readings": get_readings,
    "compute_position": compute_position,
    "get_trajectory": get_trajectory,
}


def run_tool(ds: DataSource, name: str, tool_input: dict):
    """Execute a tool by name against a data source."""
    fn = TOOL_DISPATCH.get(name)
    if fn is None:
        return {"error": f"unknown tool {name!r}"}
    return fn(ds, **(tool_input or {}))
