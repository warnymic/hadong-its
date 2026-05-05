#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Recompute core paper claims from outputs/scenario_summary.csv.

What this script does:
- Reads scenario_summary.csv
- Computes:
  - total ΔA_cum vs S0 for each scenario
  - incremental gains between consecutive levels (when possible)
  - identifies boundary transitions where MCI < threshold (default 1.0)
  - prints the minimum infrastructure package (MIP): highest level before boundary
- Writes a clean summary CSV to outputs/recomputed_summary.csv

Run:
  python scripts/recompute_mci.py
Optional:
  python scripts/recompute_mci.py --threshold 1.0
"""

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class Row:
    scenario: str
    level: str
    deltaA_cum_pct_vs_S0: Optional[float]
    incremental_gain_pct_vs_prev: Optional[float]
    cost_ratio_vs_prev: Optional[float]
    mci: Optional[float]
    mc_n: Optional[int]
    p_deltaA_gt_0: Optional[float]
    notes: str


def _to_float(x: str) -> Optional[float]:
    x = (x or "").strip()
    if x == "" or x.lower() in {"n/a", "na", "none", "null"}:
        return None
    # allow values like "0.973" or "97.3%" or "3.2×"
    x = x.replace("×", "").replace("x", "").replace("%", "")
    try:
        return float(x)
    except ValueError:
        return None


def _to_int(x: str) -> Optional[int]:
    x = (x or "").strip()
    if x == "" or x.lower() in {"n/a", "na", "none", "null"}:
        return None
    try:
        return int(float(x))
    except ValueError:
        return None


def load_csv(path: Path) -> List[Row]:
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows: List[Row] = []
        for r in reader:
            rows.append(
                Row(
                    scenario=r.get("Scenario", "").strip(),
                    level=r.get("Level", "").strip(),
                    deltaA_cum_pct_vs_S0=_to_float(r.get("DeltaA_cum_percent_vs_S0", "")),
                    incremental_gain_pct_vs_prev=_to_float(r.get("Incremental_gain_percent_vs_prev", "")),
                    cost_ratio_vs_prev=_to_float(r.get("Cost_ratio_vs_prev", "")),
                    mci=_to_float(r.get("MCI", "")),
                    mc_n=_to_int(r.get("MonteCarlo_N", "")),
                    p_deltaA_gt_0=_to_float(r.get("P_DeltaA_gt_0", "")),
                    notes=(r.get("Notes", "") or "").strip(),
                )
            )
    return rows


def sort_key(row: Row) -> Tuple[int, str]:
    # Sort by level number if possible (L0..L4), else keep as string.
    lvl = row.level.strip().upper()
    if lvl.startswith("L") and lvl[1:].isdigit():
        return (int(lvl[1:]), row.scenario)
    return (999, row.scenario)


def compute_incremental_from_totals(rows_sorted: List[Row]) -> Dict[str, Optional[float]]:
    """
    If incremental gains are missing, compute them from total ΔA_cum vs S0 when available.
    Returns mapping scenario -> incremental gain vs previous scenario in sorted order.
    """
    inc: Dict[str, Optional[float]] = {}
    prev_total: Optional[float] = None
    prev_row: Optional[Row] = None
    for row in rows_sorted:
        total = row.deltaA_cum_pct_vs_S0
        if prev_total is not None and total is not None:
            inc[row.scenario] = total - prev_total
        else:
            inc[row.scenario] = row.incremental_gain_pct_vs_prev  # maybe already set
        prev_total = total if total is not None else prev_total
        prev_row = row
    return inc


def boundary_and_mip(rows_sorted: List[Row], threshold: float) -> Tuple[List[Tuple[str, float]], str]:
    """
    Identify boundary transitions where MCI < threshold.
    Return list of (transition_label, mci) and MIP label.
    MIP = highest level before first boundary (based on sorted order).
    """
    boundaries: List[Tuple[str, float]] = []

    # Determine first boundary in order
    first_boundary_idx: Optional[int] = None
    for i, row in enumerate(rows_sorted):
        if row.mci is None:
            continue
        if row.mci < threshold:
            # transition is previous level -> this level, if possible
            if i > 0:
                prev = rows_sorted[i - 1]
                transition = f"{prev.level}→{row.level}"
            else:
                transition = f"UNKNOWN→{row.level}"
            boundaries.append((transition, row.mci))
            if first_boundary_idx is None:
                first_boundary_idx = i

    # MIP determination
    if first_boundary_idx is None:
        mip = f"L0–{rows_sorted[-1].level}" if rows_sorted else "UNKNOWN"
    else:
        # highest level before first boundary
        if first_boundary_idx == 0:
            mip = "L0"
        else:
            mip = f"L0–{rows_sorted[first_boundary_idx - 1].level}"

    return boundaries, mip


def write_summary(path: Path, rows_sorted: List[Row], inc_map: Dict[str, Optional[float]], mip: str, boundaries: List[Tuple[str, float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Scenario", "Level", "DeltaA_cum_%_vs_S0", "Incremental_%_vs_prev", "Cost_ratio_vs_prev", "MCI", "MonteCarlo_N", "P(ΔA>0)", "Notes"])
        for row in rows_sorted:
            w.writerow([
                row.scenario,
                row.level,
                "" if row.deltaA_cum_pct_vs_S0 is None else f"{row.deltaA_cum_pct_vs_S0:.3f}",
                "" if inc_map.get(row.scenario) is None else f"{inc_map[row.scenario]:.3f}",
                "" if row.cost_ratio_vs_prev is None else f"{row.cost_ratio_vs_prev:.3f}",
                "" if row.mci is None else f"{row.mci:.3f}",
                "" if row.mc_n is None else str(row.mc_n),
                "" if row.p_deltaA_gt_0 is None else f"{row.p_deltaA_gt_0:.3f}",
                row.notes,
            ])
        w.writerow([])
        w.writerow(["MIP", mip])
        if boundaries:
            w.writerow(["Boundaries (MCI<threshold)", "; ".join([f"{t}:{mci:.3f}" for t, mci in boundaries])])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="outputs/scenario_summary.csv", help="Path to scenario_summary.csv")
    ap.add_argument("--output", default="outputs/recomputed_summary.csv", help="Output CSV path")
    ap.add_argument("--threshold", type=float, default=1.0, help="Boundary threshold for MCI (default 1.0)")
    args = ap.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f"[ERROR] Input file not found: {in_path}")
        return 1

    rows = load_csv(in_path)
    rows_sorted = sorted(rows, key=sort_key)

    inc_map = compute_incremental_from_totals(rows_sorted)
    boundaries, mip = boundary_and_mip(rows_sorted, threshold=args.threshold)

    print("\n=== Recomputed Core Results ===")
    print(f"- MCI threshold: {args.threshold:.2f}")
    print(f"- Minimum Infrastructure Package (MIP): {mip}")
    if boundaries:
        print("- Boundary transitions (MCI<threshold):")
        for t, mci in boundaries:
            print(f"  * {t}: MCI={mci:.3f}")
    else:
        print("- No boundary detected (no MCI values below threshold).")

    # Report key paper numbers if present
    print("\n=== Scenario Totals (ΔA_cum vs S0) ===")
    for row in rows_sorted:
        if row.deltaA_cum_pct_vs_S0 is not None:
            print(f"  {row.scenario} ({row.level}): {row.deltaA_cum_pct_vs_S0:.1f}%")

    print("\n=== Incremental Gains (computed when possible) ===")
    for row in rows_sorted:
        inc = inc_map.get(row.scenario)
        if inc is not None:
            print(f"  {row.scenario}: +{inc:.2f}% vs prev")

    out_path = Path(args.output)
    write_summary(out_path, rows_sorted, inc_map, mip, boundaries)
    print(f"\n[OK] Wrote: {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
