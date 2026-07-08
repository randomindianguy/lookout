"""
position.py — the two-bucket math, in ONE place.

Every number the agent and the evals depend on comes from here: the loader
script, the agent's `compute_position` tool, and the future eval harness all
call this same function, so there is a single source of truth for the
arithmetic. The LLM never computes these figures itself.

Two-bucket model (PRD §8c):
  actuals_paid        (bucket 2) = every transaction posted to the budget
  committed_remaining (bucket 1) = for each OPEN commitment, its signed amount
                                   minus what's already been billed against it
  true_position                  = both buckets added together

Subtracting `billed` (the sum of transactions linked to a commitment) is what
prevents double-counting: a charge is a TRANSFER from the promised bucket to the
paid bucket, not new money.
"""

from __future__ import annotations

import math
from typing import List, Optional

from schemas import (
    Budget,
    Commitment,
    CommitmentStatus,
    Lifecycle,
    Money,
    Reading,
    Source,
    Transaction,
)


def billed_against(commitment: Commitment, transactions: List[Transaction]) -> Money:
    """How much of a commitment has actually been paid = the sum of the
    transactions linked to it. Derived, never stored."""
    return sum(
        (t.amount for t in transactions if t.commitment_id == commitment.id),
        Money(0),
    )


def compute_position(
    budget: Budget,
    commitments: List[Commitment],
    transactions: List[Transaction],
    sources: Optional[List[Source]] = None,
) -> dict:
    """Compute a budget's true position. Returns a JSON-serializable dict with
    the two buckets, the totals, the surface number a dashboard would show, and
    a per-commitment breakdown (with source citation) the brief uses as proof.
    """
    sources_by_id = {s.id: s for s in (sources or [])}

    budget_txns = [t for t in transactions if t.budget_id == budget.id]
    actuals_paid = sum((t.amount for t in budget_txns), Money(0))

    committed_remaining = Money(0)
    # Low/high bounds track the two ends of any uncertain (range) amounts, so the
    # true position can be surfaced as a RANGE rather than averaged to a false-
    # precise midpoint.
    committed_remaining_low = Money(0)
    committed_remaining_high = Money(0)
    any_uncertain = False
    lines: List[dict] = []
    excluded: List[dict] = []
    for c in commitments:
        if c.budget_id != budget.id:
            continue
        billed = billed_against(c, transactions)
        remaining_on_paper = max(c.amount.midpoint - billed, Money(0))
        remaining_low = max(c.amount.low - billed, Money(0))
        remaining_high = max(c.amount.high - billed, Money(0))
        src = sources_by_id.get(c.source_id)
        entry = {
            "commitment_id": c.id,
            "vendor": c.vendor,
            "signed": c.amount.midpoint,
            "signed_is_range": c.amount.is_range,
            "signed_low": c.amount.low,
            "signed_high": c.amount.high,
            "billed": billed,
            "remaining": remaining_on_paper,
            "status": c.status.value,
            "lifecycle": c.lifecycle.value,
            "recurring": c.recurring.value,   # 'annual' etc. — flags expected renewals
            "confidence": c.confidence,
            "source_id": c.source_id,
            "source_type": src.type.value if src else None,
            "source_reference": src.reference if src else None,
        }
        # Only a genuine range gets low/high fields — an exact amount stays a
        # single number, so the range only appears where there's real uncertainty.
        if c.amount.is_range:
            entry["remaining_low"] = remaining_low
            entry["remaining_high"] = remaining_high
        # Closed engagements and cancelled promises bring no future spend. The
        # code still EXCLUDES their remainder from the true position (the number
        # stays reliable) — but instead of silently dropping them, it surfaces
        # them with the reason, so the agent can SEE the scary-looking
        # signed-vs-billed gap and explain in the brief why it isn't counted.
        if c.lifecycle == Lifecycle.closed or c.status == CommitmentStatus.cancelled:
            entry["excluded_reason"] = (
                "closed — engagement finished; the unbilled remainder will not be spent"
                if c.lifecycle == Lifecycle.closed
                else "cancelled — will not be spent"
            )
            excluded.append(entry)
            continue
        committed_remaining += remaining_on_paper
        committed_remaining_low += remaining_low
        committed_remaining_high += remaining_high
        if c.amount.is_range:
            any_uncertain = True
        lines.append(entry)

    # Per-source subtotals, so the brief can cite "the contracts combined" or
    # "the email-only pile" as a REAL tool value instead of adding line items in
    # prose. Keyed by source type (contract / email / slack / ledger).
    by_source: dict = {}
    for ln in lines:
        st = ln["source_type"] or "unknown"
        bucket = by_source.setdefault(
            st, {"signed": Money(0), "billed": Money(0), "remaining": Money(0), "count": 0}
        )
        bucket["signed"] += ln["signed"]
        bucket["billed"] += ln["billed"]
        bucket["remaining"] += ln["remaining"]
        bucket["count"] += 1

    # Total signed-but-unbilled sitting on excluded (closed/cancelled) items —
    # the "on paper but not counted" amount, so the agent can cite it exactly.
    excluded_committed_remaining = sum((e["remaining"] for e in excluded), Money(0))

    plan = budget.plan_amount
    true_position = actuals_paid + committed_remaining
    true_position_low = actuals_paid + committed_remaining_low
    true_position_high = actuals_paid + committed_remaining_high

    result = {
        "budget_id": budget.id,
        "budget_name": budget.name,
        "plan_amount": plan,
        "actuals_paid": actuals_paid,               # bucket 2
        "committed_remaining": committed_remaining,  # bucket 1
        "committed_remaining_by_source": by_source,  # subtotals to cite, never add
        "excluded_commitments": excluded,            # closed/cancelled — surfaced, not counted
        "excluded_committed_remaining": excluded_committed_remaining,
        "true_position": true_position,              # both buckets (midpoint if any range)
        "position_is_uncertain": any_uncertain,      # true iff a counted amount is a range
        # ratios, not money -> float is fine and display rounds them anyway
        "pct_of_plan": float(true_position / plan) if plan else None,
        "surface_pct": float(actuals_paid / plan) if plan else None,  # what a dashboard shows
        "over_under": true_position - plan,          # positive = over plan
        "months_total": budget.period.months_total,
        "months_elapsed": budget.period.months_elapsed,
        "months_remaining": budget.period.months_total - budget.period.months_elapsed,
        "as_of": budget.period.as_of,
        "commitment_lines": lines,
    }
    # When a counted commitment amount is a genuine range, DON'T hide the
    # uncertainty behind the midpoint — surface the true position as a RANGE so
    # the agent can calibrate ("$90K under to $115K over") instead of asserting a
    # false-precise single number. These fields appear ONLY when there's real
    # uncertainty; certain budgets get a normal single-number position.
    if any_uncertain:
        result["committed_remaining_low"] = committed_remaining_low
        result["committed_remaining_high"] = committed_remaining_high
        result["true_position_low"] = true_position_low
        result["true_position_high"] = true_position_high
        result["pct_of_plan_low"] = float(true_position_low / plan) if plan else None
        result["pct_of_plan_high"] = float(true_position_high / plan) if plan else None
        # straddles_plan: the range spans the plan line, so over-vs-under is
        # genuinely undecidable until the amount is confirmed.
        result["straddles_plan"] = bool(
            plan and true_position_low < plan < true_position_high
        )
    return result


def compute_trajectory(budget: Budget, readings: List[Reading]) -> dict:
    """Read a SEQUENCE of readings and surface the trend + a forward forecast.

    §12h-bis: the code does the math reliably, but it SURFACES THE SEQUENCE (the
    actual per-reading numbers and the week-over-week climb) rather than handing
    the agent only a single pre-computed 'rate'. A budget can be UNDER plan at
    every single reading and still be heading for a breach — the danger lives
    BETWEEN the frames, in the rate of climb, not in any one snapshot. The agent
    reasons over the sequence and explains the climb; the code just makes the
    arithmetic exact.
    """
    budget_readings = [r for r in readings if r.budget_id == budget.id]
    # oldest -> newest (ISO timestamps sort chronologically)
    budget_readings.sort(key=lambda r: r.timestamp)
    seq = [
        {
            "timestamp": r.timestamp,
            "true_position": r.position.true_position,
            "pct_of_plan": r.position.pct_of_plan,
        }
        for r in budget_readings
    ]
    plan = budget.plan_amount

    if len(seq) < 2:
        # No trend without at least two points in time — a single snapshot has
        # no rate (freeze the clock and the rate vanishes).
        return {
            "budget_id": budget.id,
            "budget_name": budget.name,
            "plan_amount": plan,
            "has_trajectory": False,
            "sequence": seq,
        }

    # The visible climb: week-over-week change in true position.
    deltas = [
        seq[i]["true_position"] - seq[i - 1]["true_position"]
        for i in range(1, len(seq))
    ]
    latest = seq[-1]["true_position"]
    first = seq[0]["true_position"]
    intervals = len(seq) - 1
    avg_rate = (latest - first) / intervals        # average over the WHOLE window
    headroom = plan - latest                        # room left before plan
    already_over = latest >= plan

    # The RECENT pace is what predicts the near future — NOT the whole-window
    # average. A budget that climbed steeply then flattened has a high average
    # but a near-zero recent rate; averaging hides the flattening (the very
    # signal that tells you it WON'T breach). So the forecast runs off the recent
    # rate, with the average kept only for reference.
    recent_rate = deltas[-1]                         # the latest reading-over-reading change
    earlier = deltas[:-1]
    earlier_avg = (sum(earlier, Money(0)) / len(earlier)) if earlier else recent_rate

    if recent_rate <= 0:
        trend = "flat_or_declining"
    elif earlier_avg > 0 and recent_rate < earlier_avg / 2:
        trend = "flattening"                         # recent pace well below the earlier climb
    elif earlier_avg > 0 and recent_rate > earlier_avg * Money("1.3"):
        trend = "accelerating"
    else:
        trend = "steady"

    def _periods(rate):
        if already_over:
            return 0
        if rate <= 0:
            return None                              # not climbing -> won't breach
        return int(math.ceil(float(headroom) / float(rate)))

    return {
        "budget_id": budget.id,
        "budget_name": budget.name,
        "plan_amount": plan,
        "has_trajectory": True,
        "sequence": seq,                     # the actual per-reading numbers — reason over THESE
        "weekly_deltas": deltas,             # the climb, reading over reading
        "recent_rate": recent_rate,          # the CURRENT pace (latest interval) — use this to forecast
        "avg_rate_per_period": avg_rate,     # whole-window average (reference only; hides flattening)
        "earlier_avg_rate": earlier_avg,     # average of the earlier intervals, to compare against recent
        "trend": trend,                      # steady | accelerating | flattening | flat_or_declining
        "latest_true_position": latest,
        "headroom_to_plan": headroom,        # plan - latest
        "projected_next_period": latest + recent_rate,   # forecast at the RECENT pace
        "periods_to_breach": _periods(recent_rate),      # periods to breach at the RECENT pace
        "periods_to_breach_if_avg": _periods(avg_rate),  # same at the (misleading) average pace, for reference
        "already_over": already_over,
    }
