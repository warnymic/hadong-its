# Level Toggles (L0–L4)

This file defines the infrastructure/ODD maturity toggles used to construct scenarios and evaluate the MCI boundary.

## ODD axes (4)
- Communication
- HD mapping (HD map)
- Traffic control (control/monitoring)
- Intersection cooperation (smart intersection / SPaT/MAP)

## Levels
### L0 — Baseline
- Communication: minimal / not evaluated
- HD map: none (or conventional map)
- Control: basic operations only
- Intersection cooperation: none
- Intended use: baseline for Δ comparisons (S0)

### L1 — Operations MVP (minimum controllable service)
- Communication: stable cellular connectivity for monitoring/remote support
- HD map: none (or limited)
- Control: basic monitoring + event logging (OTP/Waiting/Cancel/MTTR computable)
- Intersection cooperation: none
- Output focus: operational KPI availability (OTP, waiting distribution, cancellation, MTTR)

### L2 — Core HD mapping (ODD stabilization)
- Communication: L1 +
- HD map: core HD mapping for the operating corridor (core segment coverage)
- Control: procedures for updates (construction/closures reflected operationally)
- Intersection cooperation: none
- Reported outcome (paper): +18.3% accessibility improvement vs S0

### L3 — Smart intersections at key junctions
- Communication: L2 +
- HD map: L2 +
- Control: L2 +
- Intersection cooperation: enabled at five key junctions (smart intersections; SPaT/MAP-type support)
- Reported outcome (paper): +22.7% accessibility improvement vs S0
- Robustness (paper): P(ΔA>0)=97.3% with N=1,000

### L4 — Full RSU deployment
- Communication: L3 +
- HD map: L3 +
- Control: L3 +
- Intersection cooperation: expanded (full RSU deployment across corridor/network)
- Reported outcome (paper): +4.1% additional gain over L3 (total +26.8% vs S0)
- Cost-effectiveness boundary (paper): cost is 3.2× L3 while MCI drops to 0.43 (boundary at L3→L4)

## Scenario mapping
- S0 → L0
- S1 → L1
- S2 → L2
- S3 → L3
- S4 → L4