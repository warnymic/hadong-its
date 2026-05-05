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

## How to Compute (Pseudo-code)

### Inputs
- Scenarios: `S0..S5` mapped to infrastructure levels `L0..L4`
- Network: links/nodes, travel times (from SUMO or routing engine)
- Demand/OD: origin zones `i`, destinations/opportunities `j`, weights `O_j`
- Operational KPIs per scenario: `OTP`, `E[W]`, `P90(W)`, `P(cancel)`, `E[MTTR]`
- Costs per level `C_k` (TCO = CAPEX + OPEX)

### Step 0) Define levels and scenario mapping
```text
L0: baseline (DRT-only or no infra support)
L1: comm + monitoring (MVP ops)
L2: core HD map + ODD stabilization
L3: smart intersections at key junctions
L4: full RSU deployment
S0..S5 correspond to increasing levels (your paper's mapping)

### Step 1) Compute generalized travel time matrix for each scenario

```math id="step1-gtt"
t_{ij}(s)=t^{drive}_{ij}(s)+E[W](s)+\lambda\cdot P90(W)(s)+\phi\cdot P(cancel)(s)+\psi\cdot E[MTTR](s)
```

### Step 2) Compute accessibility

```math id="step2-acum"
A_{cum,i}(T;s)=\sum_j O_j\cdot \mathbf{1}(t_{ij}(s)\le T)
```

```math id="step2-agrav"
A_{grav,i}(s)=\sum_j O_j\cdot e^{-\beta t_{ij}(s)}
```

### Step 3) Improvements vs baseline

```math id="step3-deltaA"
\Delta A(s)=\bar{A}(s)-\bar{A}(S0)
```

### Step 4) MCI boundary

```math id="step4-MA"
MA_{k\rightarrow k+1}=\bar{A}(s_{k+1})-\bar{A}(s_k)
```

```math id="step4-MC"
MC_{k\rightarrow k+1}=C_{k+1}-C_k
```

```math id="step4-MCI"
MCI_{k\rightarrow k+1}=\frac{MA_{k\rightarrow k+1}}{MC_{k\rightarrow k+1}}
```

### Step 5) Monte Carlo robustness

```math id="step5-prob"
P(\Delta A>0)=\frac{1}{N}\sum_{n=1}^{N}\mathbf{1}(\Delta A_n>0)
```

---

## Example Outputs (Filled Example from the Paper)

* Scenario summary (CSV): `outputs/scenario_summary.csv`
* Level toggles: `repro/level_toggles.md`
* Cost assumptions (TCO structure): `assumptions/cost_assumptions.md`

---

## Reproducibility

This repository provides the equation set, notation, level toggles (L0–L4), and scenario-level summary outputs used in the paper.
Raw operational logs are not publicly shared due to data governance constraints; however, all scenario definitions and aggregation outputs required to reproduce the reported boundary (MCI) are provided.
The pipeline is designed to be re-applied to other regions using the same minimum schema (Trip/Dispatch/OD/Waiting/Event).

