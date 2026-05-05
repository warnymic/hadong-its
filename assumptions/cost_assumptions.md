# Cost Assumptions (TCO structure)

This document provides the cost structure used for marginal cost-effectiveness (MCI) evaluation.
Absolute unit costs may vary by site; therefore the paper interprets results primarily through
the stability of the MCI boundary (rather than absolute cost levels).

## 1) Cost structure (TCO = CAPEX + OPEX)
### CAPEX (installation / build)
- RSU / smart intersection equipment and installation
- Backhaul/network integration (where applicable)
- Control/monitoring system integration (software + setup)
- HD map production (core corridor coverage)

### OPEX (annual operations)
- Network subscription / connectivity
- Maintenance and repair
- HD map refresh / update operations
- Monitoring/remote support operations (if accounted)

## 2) Marginal cost definition
For level transition k→k+1:
- MC_{k→k+1} = C_{k+1} - C_k
- MCI_{k→k+1} = MA_{k→k+1} / MC_{k→k+1}

## 3) How the paper reports L3→L4 cost ratio
The paper reports that L4 incurs 3.2× higher cost than L3 while providing only +4.1% incremental accessibility gain.
This ratio is treated as an empirical summary of the level transition cost expansion.

- Cost ratio (reported): C_L4 / C_L3 = 3.2
- Incremental gain (reported): ΔA_L4 - ΔA_L3 = +4.1%
- MCI (reported for L3→L4): 0.43

## 4) Interpretation rule (boundary)
- A boundary is identified when MCI < 1.0 for a level transition.
- The paper concludes the minimum infrastructure package (MIP) is L1–L3 based on the boundary at L3→L4.

## 5) Source transparency (non-numeric)
If numeric unit costs cannot be publicly disclosed, provide at minimum:
- itemized CAPEX/OPEX categories (above)
- site-specific assumptions (corridor length, #junctions, RSU coverage scope)
- the reported relative ratio for L3→L4 (3.2×) and the MCI boundary logic