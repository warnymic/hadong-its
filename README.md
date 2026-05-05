## Notation (Variables & Parameters)

> Units are shown in brackets. If your implementation uses different units (e.g., seconds), convert consistently.

### Indices
- $i$: origin zone/grid (residential area)
- $j$: destination opportunity/POI
- $k$: infrastructure maturity level ($k \in \{0,1,2,3,4\}$)
- $n$: Monte Carlo trial index ($n=1,\dots,N$)

### Travel time and reliability components
- $t_{ij}$: generalized travel time from $i$ to $j$ [min]
- $t^{drive}_{ij}$: in-vehicle/drive time from $i$ to $j$ (excluding waiting/reliability penalties) [min]
- $W$: waiting time (request/booking $\rightarrow$ boarding) [min]
- $E[W]$: mean waiting time [min]
- $P90(W)$: 90th percentile waiting time [min]
- $P(cancel)$: cancellation (missed trip) probability or rate [–]
- $MTTR$: mean time to repair/restore after an operational disruption [min]
- $E[MTTR]$: mean MTTR [min]

### Penalty weights (reliability penalties)
- $\lambda$: weight for high-quantile waiting penalty [–]
- $\phi$: penalty weight for cancellations [min] (interpretable as “equivalent minutes” per cancellation probability)
- $\psi$: penalty weight for disruption recovery time [–] (or [min/min] depending on formulation)

### Accessibility measures
- $A_{cum,i}(T)$: cumulative-opportunity accessibility for zone $i$ within threshold $T$ [opportunities]
- $T$: time threshold (e.g., 30/45/60) [min]
- $O_j$: opportunity weight at destination $j$ (e.g., hospital capacity, jobs, services) [opportunity units]
- $\mathbf{1}(\cdot)$: indicator function (1 if condition holds, else 0)

- $A_{grav,i}$: gravity-based accessibility for zone $i$ [weighted opportunities]
- $\beta$: impedance (decay) parameter in gravity function [1/min]

### Cost-effectiveness
- $C_k$: total cost at infrastructure level $k$ (TCO-style, CAPEX+OPEX) [currency]
- $MA_{k\rightarrow k+1}$: marginal accessibility gain from level $k$ to $k{+}1$ [accessibility units]
- $MC_{k\rightarrow k+1}$: marginal cost increase from level $k$ to $k{+}1$ [currency]
- $MCI_{k\rightarrow k+1}$: marginal cost-effectiveness index [accessibility units / currency]
  - Typical decision rule used in the paper: boundary when $MCI < 1$ (example threshold)

### Monte Carlo robustness
- $\Delta A_n$: accessibility improvement in trial $n$ (scenario vs baseline) [accessibility units]
- $P(\Delta A>0)$: probability that accessibility improvement is positive [–]
- $N$: number of Monte Carlo trials (e.g., $N=1000$) [count]

---

## Recommended baseline settings (example)

> Adjust to your study context; report sensitivity ranges if used.

- $T \in \{30,45,60\}$ minutes
- $\beta$: set from literature range; also run sensitivity (e.g., $\beta \in [0.03,0.07]$ 1/min)
- $\lambda,\phi,\psi$: set as baseline + sensitivity ranges (report in Appendix)
