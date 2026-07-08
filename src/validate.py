"""
validate.py — the structural guarantee that a brief invents no numbers.

Every numeric token in a brief must trace to a value the tools actually returned.
This is enforced by CODE, not by prompt: the agent's brief is rejected and
regenerated if any figure isn't tool-backed. The same function is meant to double
as an eval assertion — run validate_brief() on every brief, every seed, and a
fabricated number is a hard failure.

How it works:
  - Build the ALLOWED sets from the exact tool outputs the agent received (the
    compute_position result dicts): every money Decimal, every ratio rendered as a
    percentage, every integer, and every digit group that appears inside a string
    the tool returned (dates, filenames, quarter labels).
  - Extract every currency token ($…), percentage token (…%), and bare number
    from the brief, and check each against the allowed sets.
  - Anything not found is a violation.

Money is compared as Decimal, so "$240,000", "$240,000.00", and 240000 all match
the same tool value; ratios are matched at their standard 0- and 1-decimal
percentage renderings (127%, 126.7%, 30%).
"""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import List

# Currency may carry a K/M/B suffix ("$50K"). The (?![A-Za-z]) guard keeps the
# suffix from eating a following word (so "$50 million" or "3M Company" don't turn
# a stray letter into a multiplier). The suffix is allowed on $-amounts only —
# bare numbers stay literal so "2 months" is never read as "2 million".
_CURRENCY_RE = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?(?:\s?[KkMmBb](?![A-Za-z]))?")
_PERCENT_RE = re.compile(r"\d[\d,]*(?:\.\d+)?\s?%")
_NUMBER_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")
_DIGITS_RE = re.compile(r"\d+")

_SUFFIX = {"K": Decimal(1000), "M": Decimal(1_000_000), "B": Decimal(1_000_000_000)}


def _to_decimal(raw: str) -> Decimal:
    s = raw.replace("$", "").replace("%", "").replace(",", "").replace(" ", "")
    mult = Decimal(1)
    if s and s[-1] in "KkMmBb":
        mult = _SUFFIX[s[-1].upper()]
        s = s[:-1]
    return Decimal(s) * mult


class BriefValidation:
    """Result of validating one brief. Truthy iff no fabricated numbers."""

    def __init__(self, ok: bool, violations: list, allowed: dict):
        self.ok = ok
        self.violations = violations  # [{"token": str, "kind": str}]
        self.allowed = allowed

    def __bool__(self) -> bool:
        return self.ok

    def message(self) -> str:
        """Feedback handed back to the model to drive a regeneration."""
        lines = [
            "Your brief contains numbers that did NOT come from any tool and are "
            "therefore not allowed. Every figure in the brief must be a value a "
            "tool returned verbatim (a compute_position field, including its "
            "per-source subtotals). Remove or replace each of these, then rewrite "
            "the brief. Do not add or combine numbers yourself:",
        ]
        for v in self.violations:
            lines.append(f'  - "{v["token"]}" ({v["kind"]}) is not a tool value')
        return "\n".join(lines)


def _collect(positions: List[dict]):
    """Walk the tool-output dicts and build the allowed sets."""
    money: set = set()      # Decimal money values
    percents: set = set()   # Decimal, e.g. 127, 126.7, 30, 100
    ints: set = set()       # int — bare-number whitelist

    def walk(value):
        if value is None or isinstance(value, bool):
            return
        if isinstance(value, Decimal):
            # Allow the magnitude too: over_under is stored negative when under
            # plan (-6000), but an honest brief cites it as "under by $6,000".
            # abs() is a no-op for the (positive) money values, so this only
            # newly-permits |over_under| — exactly the legitimate rendering.
            for m in (value, abs(value)):
                money.add(m)
                if m == m.to_integral_value():
                    ints.add(int(m))
        elif isinstance(value, float):
            # a ratio (pct_of_plan, surface_pct, confidence) -> percent renderings
            for p in (round(value * 100), round(value * 100, 1)):
                percents.add(Decimal(str(p)))
                if float(p).is_integer():
                    ints.add(int(p))
        elif isinstance(value, int):
            ints.add(value)
            # an int amount from a data tool (e.g. a $30,000 charge) is money too,
            # so a currency token like "$30,000" matches it, not just aggregates
            money.add(Decimal(value))
        elif isinstance(value, str):
            for grp in _DIGITS_RE.findall(value):
                ints.add(int(grp))
        elif isinstance(value, dict):
            for v in value.values():
                walk(v)
        elif isinstance(value, (list, tuple)):
            for v in value:
                walk(v)

    for pos in positions:
        walk(pos)
    return money, percents, ints


def validate_brief(brief: str, tool_outputs: List[dict]) -> BriefValidation:
    """Assert every numeric token in `brief` traces to a value the tools returned
    (across ALL data tools the agent called, not just compute_position)."""
    # An empty / contentless brief is not a clean verdict — never bless it.
    if not brief or not brief.strip():
        return BriefValidation(
            ok=False,
            violations=[{"token": "(empty brief)", "kind": "empty"}],
            allowed={},
        )
    money, percents, ints = _collect(tool_outputs)
    violations: list = []
    covered_spans: list = []  # currency/percent spans, to skip in the bare-number pass

    for m in _CURRENCY_RE.finditer(brief):
        covered_spans.append(m.span())
        try:
            val = _to_decimal(m.group())
        except InvalidOperation:
            violations.append({"token": m.group().strip(), "kind": "currency"})
            continue
        if val not in money:
            violations.append({"token": m.group().strip(), "kind": "currency"})

    for m in _PERCENT_RE.finditer(brief):
        covered_spans.append(m.span())
        try:
            val = _to_decimal(m.group())
        except InvalidOperation:
            violations.append({"token": m.group().strip(), "kind": "percent"})
            continue
        if val not in percents:
            violations.append({"token": m.group().strip(), "kind": "percent"})

    for m in _NUMBER_RE.finditer(brief):
        start, end = m.span()
        if any(start >= cs and end <= ce for cs, ce in covered_spans):
            continue  # part of a currency/percent token already checked
        before = brief[start - 1] if start > 0 else ""
        after = brief[end] if end < len(brief) else ""
        if before == "$" or after == "%":
            continue  # currency/percent handled above
        if before in ("Q", "q"):
            continue  # quarter label (Q3, Q4), not a financial magnitude
        try:
            val = _to_decimal(m.group())
        except InvalidOperation:
            continue
        if val == val.to_integral_value() and int(val) in ints:
            continue
        if val in money or val in percents:
            continue
        violations.append({"token": m.group().strip(), "kind": "number"})

    return BriefValidation(
        ok=not violations,
        violations=violations,
        allowed={"money": money, "percents": percents, "ints": ints},
    )
