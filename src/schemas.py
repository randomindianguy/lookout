"""
Committed-Spend Agent — data model (PRD §14).

Five entities: Budget, Commitment, Transaction, Source, Reading.
Every record carries an `origin` field for lineage (real-API vs synthetic-file,
and which source) — PRD's lineage rule, added from the start rather than retrofit.

Two design rules from the PRD, encoded here:
  1. "Never store a total that can go stale — compute it."
     - Budget stores the PLAN only; actuals/spent are computed from transactions.
     - Commitment stores its total SIGNED amount only; the billed portion is
       derived from the transactions linked to it (the two-bucket model, §8c).
  2. A promise and its later charge are the SAME dollar at two life stages.
     status walks promised -> partly-billed -> paid; a charge is a TRANSFER
     between buckets (linked via Transaction.commitment_id), never new money.

Written for Pydantic (v1 or v2): models are constructed with `Model(**data)`
and read via attribute access, so both major versions work unchanged.
"""

from __future__ import annotations

from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

# Money is represented as Decimal, never float. Floats carry binary rounding
# error (0.1 + 0.2 != 0.3), which is unacceptable for a product whose whole
# credibility is exact numbers. Decimal is exact and reads as clean whole
# dollars. JSON is parsed with parse_float=Decimal (see the loaders) so no money
# value ever passes through a float on the way in. All future seeds and the eval
# inherit this by using these types.
Money = Decimal


# --------------------------------------------------------------------------- #
# Shared value objects / enums
# --------------------------------------------------------------------------- #

class OriginMode(str, Enum):
    """Where a record physically came from. Synthetic-first today; flip to
    real-api one source at a time as the real APIs get wired in."""
    real_api = "real-api"
    synthetic_file = "synthetic-file"


class Origin(BaseModel):
    """Lineage stamp on every record (PRD §14 lineage rule).

    `source` names the system/tool this record emulates (get_contracts,
    get_emails, get_transactions, ...), so when the agent misbehaves you can
    trace the behavior straight back to the data that produced it — and so the
    swap from synthetic-file to real-api is a one-field change per source.
    """
    mode: OriginMode
    source: str                     # e.g. "get_contracts", "get_emails", "get_transactions"
    detail: Optional[str] = None    # optional specific pointer (file path, ledger id, thread id)


class CommitmentStatus(str, Enum):
    """The two-bucket model as data (PRD §8c / §14).

    promised  -> money in bucket 1 (promised-but-not-paid), $0 billed
    partly-billed -> the commitment straddles both buckets
    paid      -> fully transferred into bucket 2 (already-paid)
    cancelled -> the promise was withdrawn; contributes nothing
    uncertain -> we're not sure this obligation is real / its size (Seed 7)
    """
    promised = "promised"
    partly_billed = "partly-billed"
    paid = "paid"
    cancelled = "cancelled"
    uncertain = "uncertain"


class SourceType(str, Enum):
    """Where a commitment's evidence lives."""
    ledger = "ledger"
    contract = "contract"
    email = "email"
    slack = "slack"


class Recurrence(str, Enum):
    """How often a commitment repeats. Needed by Seeds 2 & 5 to reason about
    renewals; 'none' for one-time engagements (all of Seed 1)."""
    none = "none"
    monthly = "monthly"
    quarterly = "quarterly"
    annual = "annual"


class Lifecycle(str, Enum):
    """Whether more spend is expected against this commitment.
    Seed 4 hinges on 'closed' (finished, no future spend) vs 'active'."""
    active = "active"
    closed = "closed"


class Amount(BaseModel):
    """An amount that may be a single figure OR a range.

    Seed 1 uses exact figures (low == high). Seed 7's ground truth is a RANGE
    ("$25K-$50K, unresolved"), which is why amount is modeled as [low, high]
    from the start rather than a bare number.
    """
    low: Money
    high: Money
    currency: str = "USD"

    @property
    def midpoint(self) -> Money:
        # `/ 2` (int), never `/ 2.0` — dividing a Decimal by a float raises;
        # Decimal / int stays exact Decimal.
        return (self.low + self.high) / 2

    @property
    def is_range(self) -> bool:
        return self.low != self.high

    @classmethod
    def exact(cls, value: Money, currency: str = "USD") -> "Amount":
        return cls(low=value, high=value, currency=currency)


# --------------------------------------------------------------------------- #
# The five entities
# --------------------------------------------------------------------------- #

class Period(BaseModel):
    """Which quarter a budget covers and how far into it we are.
    `as_of` is the snapshot 'now' — the moment the position is read."""
    label: str                  # human label, e.g. "Q3 2026"
    quarter: str                # machine key, e.g. "2026-Q3"
    start_date: str             # ISO date, quarter start
    months_total: int           # length of the period in months
    months_elapsed: int         # how many have passed at `as_of`
    as_of: str                  # ISO datetime — the snapshot moment


class Budget(BaseModel):
    """A plan to spend, owned by a department head.

    Deliberately does NOT carry an amount-spent field — that is always computed
    from transactions (paid) + open commitments (promised). Storing it would let
    it go stale against the underlying records.
    """
    id: str
    name: str
    owner: str                  # the department head who spends against it
    plan_amount: Money          # the planned budget for the period
    currency: str = "USD"
    period: Period
    origin: Origin
    # NOTE: no `amount_spent` / `actuals` — computed, never stored.


class Source(BaseModel):
    """Where a commitment's evidence physically lives, specific enough to cite.

    The agent uses this to SHOW the receipts ("get_contracts, file:
    DevShop_SOW_Q3_FINAL.pdf"), which is what makes the diagnosis verifiable.
    """
    id: str
    type: SourceType
    reference: str              # the specific document / thread, not just a category
    origin: Origin


class Commitment(BaseModel):
    """A single promise to spend — the heart of the product.

    Stores the total SIGNED amount only. How much has been billed so far is
    DERIVED from the transactions linked to this commitment (see the loader),
    so the promised-vs-paid split can never drift from the actual ledger.
    """
    id: str
    budget_id: str              # which budget it belongs to
    vendor: str
    amount: Amount              # total signed amount (range-capable)
    status: CommitmentStatus    # the two-bucket stage
    source_id: str              # pointer to the Source that evidences it
    # confidence = how sure the agent is this commitment is REAL and for THIS
    # amount. It does NOT reflect how messy/hard-to-find the source is (that's
    # tracked separately via `source_id`/Source). A firm $50K deal that lives
    # only in email is still confidence 1.0. Confidence only meaningfully drops
    # when the amount is a genuine range / the obligation is unresolved (Seed 7).
    confidence: float = Field(ge=0.0, le=1.0)
    recurring: Recurrence = Recurrence.none
    lifecycle: Lifecycle = Lifecycle.active
    description: Optional[str] = None
    origin: Origin
    # NOTE: no `billed` / `remaining` — derived from linked transactions.


class Transaction(BaseModel):
    """Money that actually moved (an actual / paid item).

    `commitment_id` links a charge to the promise it settles. That link is what
    lets the agent RELIEVE a promise (transfer between buckets) instead of
    double-counting it. Matching a messy real charge to a promise is the hard
    sub-skill; here the links are clean (a stated Seed 1 simplification).
    """
    id: str
    budget_id: str
    amount: Money
    currency: str = "USD"
    date: str                   # ISO date the charge posted
    vendor: str
    commitment_id: Optional[str] = None   # the commitment this settles, if any
    origin: Origin


class ComputedPosition(BaseModel):
    """A budget's position at a point in time — the two buckets plus totals.
    This is a computed snapshot captured into a Reading (legitimate history),
    NOT a live total stored on the Budget."""
    plan_amount: Money
    actuals_paid: Money         # bucket 2: already-paid (sum of transactions)
    committed_remaining: Money  # bucket 1: promised-but-not-paid (unbilled commitments)
    true_position: Money        # both buckets added together
    pct_of_plan: float          # true_position / plan — a ratio, not money
    surface_pct: float          # actuals_paid / plan — a ratio, not money
    over_under: Money           # true_position - plan (positive = over)


class Reading(BaseModel):
    """A budget's computed position captured at a timestamp.

    A SERIES of these = history = the ability to compute a rate of change.
    Required for Seed 8 (watching over time); without this entity the agent is
    structurally a snapshot analyzer. Seed 1 has a single reading.
    """
    id: str
    budget_id: str
    timestamp: str              # ISO datetime
    position: ComputedPosition
    origin: Origin


# --------------------------------------------------------------------------- #
# Convenience container (one seed's full dataset)
# --------------------------------------------------------------------------- #

class SeedDataset(BaseModel):
    """Everything one seed needs, loaded and validated together."""
    budgets: List[Budget]
    commitments: List[Commitment]
    transactions: List[Transaction]
    sources: List[Source]
    readings: List[Reading]
