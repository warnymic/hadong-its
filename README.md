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
## Reproducibility
This repository provides the equation set, notation, level toggles (L0–L4), and scenario-level summary outputs used in the paper.
Raw operational logs are not publicly shared due to data governance constraints; however, all scenario definitions and aggregation outputs required to reproduce the reported boundary (MCI) are provided.
The pipeline is designed to be re-applied to other regions using the same minimum schema (Trip/Dispatch/OD/Waiting/Event).
### Inputs
- Scenarios: `S0..S5` mapped to infrastructure levels `L0..L4`
- Network: links/nodes, travel times (from SUMO or routing engine)
- Demand/OD: origin zones `i`, destinations/opportunities `j`, weights `O_j`
- Operational KPIs per scenario (from logs or simulation):
  - `OTP`, `E[W]`, `P90(W)`, `P(cancel)`, `E[MTTR]`
- Costs per level `C_k` (TCO = CAPEX + OPEX)

### Step 0) Define levels and scenario mapping
```text
L0: baseline (DRT-only or no infra support)
L1: comm + monitoring (MVP ops)
L2: core HD map + ODD stabilization
L3: smart intersections at key junctions
L4: full RSU deployment
S0..S5 correspond to increasing levels (your paper's mapping)

````markdown
### Step 0) Define levels and scenario mapping
```text
L0: baseline (DRT-only or no infra support)
L1: comm + monitoring (MVP ops)
L2: core HD map + ODD stabilization
L3: smart intersections at key junctions
L4: full RSU deployment
S0..S5 correspond to increasing levels (your paper's mapping)
````

### Step 1) Compute generalized travel time matrix for each scenario

For each scenario `s` (level `k`):

1. Obtain drive time `t_drive_ij(s)` for all OD pairs `(i,j)`

   * from SUMO outputs, or shortest path on scenario network
2. Obtain KPI terms for scenario `s`:

   * `E[W](s), P90(W)(s), P(cancel)(s), E[MTTR](s)`
3. Compute generalized travel time:

```math
t_{ij}(s)=t^{drive}_{ij}(s)+E[W](s)+\lambda\cdot P90(W)(s)+\phi\cdot P(cancel)(s)+\psi\cdot E[MTTR](s)
```

### Step 2) Compute accessibility (two measures recommended)

For each origin zone `i` and scenario `s`:

**(a) Cumulative opportunity accessibility**

```math
A_{cum,i}(T;s)=\sum_j O_j\cdot \mathbf{1}(t_{ij}(s)\le T)
```

**(b) Gravity-based accessibility**

```math
A_{grav,i}(s)=\sum_j O_j\cdot e^{-\beta t_{ij}(s)}
```

Optional aggregation:

* Area average: `Ā(s) = mean_i A_i(s)`
* Equity view: report by sub-region (e.g., 읍내 vs 면지역) or percentile bands

### Step 3) Compute improvements vs baseline

Choose baseline `S0` (or `L0`) and compute:

```math
\Delta A(s)=\bar{A}(s)-\bar{A}(S0)
```

Do this for both `A_cum` and `A_grav`.

### Step 4) Compute marginal effects and MCI boundary

Let scenario `s_k` correspond to level `k`.

Marginal accessibility:

```math
MA_{k\rightarrow k+1}=\bar{A}(s_{k+1})-\bar{A}(s_k)
```

Marginal cost:

```math
MC_{k\rightarrow k+1}=C_{k+1}-C_k
```

Marginal cost-effectiveness index:

```math
MCI_{k\rightarrow k+1}=\frac{MA_{k\rightarrow k+1}}{MC_{k\rightarrow k+1}}
```

Decision rule (example used in the paper):

* Boundary when `MCI < 1.0`
* Minimum Infrastructure Package (MIP) = highest level before boundary (e.g., `L1–L3`)

### Step 5) Monte Carlo robustness (uncertainty in ops conditions)

1. Define distributions for uncertain inputs (per scenario or globally):

   * `Demand`, `E[W]`, `P90(W)`, `P(cancel)`, `E[MTTR)` (e.g., triangular)
2. For trial `n = 1..N`:

   * sample uncertain variables
   * recompute `t_ij(s)`, `A(s)`, and `ΔA(s)`
3. Report robustness:

```math
P(\Delta A>0)=\frac{1}{N}\sum_{n=1}^{N}\mathbf{1}(\Delta A_n>0)
```

Also report mean and P10/P90 of `ΔA`.

### Minimal reporting checklist (for ITS evaluation framing)

* Scenario definition table (L0–L4, S0–S5)
* KPI summary table (OTP, E[W], P90, cancel, MTTR)
* Accessibility improvements (ΔA_cum, ΔA_grav)
* MCI table and identified boundary
* Monte Carlo robustness: mean(ΔA), P(ΔA>0), P10/P90

## Example Outputs (Filled Example from the Paper)

### Table A. Scenario KPI summary (S0–S5)
> Note: The paper reports key accessibility/cost-effectiveness outcomes; absolute KPI values (OTP, waiting time, cancellation, MTTR) should be filled from logs/simulation outputs if disclosed.

| Scenario | Level | OTP (%) | E[W] (min) | P90(W) (min) | Cancel rate (%) | MTTR (min) |
|---|---|---:|---:|---:|---:|---:|
| S0 | L0 | n/a | n/a | n/a | n/a | n/a |
| S1 | L1 | n/a | n/a | n/a | n/a | n/a |
| S2 | L2 | n/a | n/a | n/a | n/a | n/a |
| S3 | L3 | n/a | n/a | n/a | n/a | n/a |
| S4 | L4 | n/a | n/a | n/a | n/a | n/a |

---

### Table B. Accessibility results (baseline vs scenario)
> The paper reports cumulative opportunity accessibility gains of **+18.3% at L2** and **+22.7% at L3** (vs baseline), and an additional **+4.1% gain at L4** compared to L3.

| Scenario | Level | ΔA_cum vs baseline | Notes |
|---|---|---:|---|
| S0 | L0 | 0.0% | Baseline |
| S1 | L1 | n/a | (not explicitly reported as % gain) |
| S2 | L2 | **+18.3%** | Core HD mapping |
| S3 | L3 | **+22.7%** | Smart intersections at 5 key junctions |
| S4 | L4 | **+26.8%*** | *Computed as 22.7% + 4.1% (increment over L3)* |

---

### Table C. Marginal cost-effectiveness (MCI) and boundary
> The paper confirms a clear boundary at **L3→L4** with **MCI = 0.43**, while **L4 costs 3.2× L3** and yields only **+4.1% additional gain**.

| Transition | Incremental gain | Relative cost | MCI | Boundary? (MCI<1) |
|---|---:|---:|---:|---|
| L0→L1 | n/a | n/a | n/a | n/a |
| L1→L2 | n/a | n/a | n/a | n/a |
| L2→L3 | n/a | n/a | n/a | n/a |
| L3→L4 | **+4.1%** (over L3) | **3.2×** (vs L3) | **0.43** | **YES** |

```math id="5j8t6f"
MCI_{k\rightarrow k+1}=\frac{MA_{k\rightarrow k+1}}{MC_{k\rightarrow k+1}}
````

---

### Table D. Monte Carlo robustness (N=1,000)

> Robustness reported for L3: **P(ΔA>0)=97.3%** with N=1,000.

| Scenario |    N |   P(ΔA>0) | Notes                       |
| -------- | ---: | --------: | --------------------------- |
| S3 (L3)  | 1000 | **97.3%** | Robust positive improvement |
| Others   |  n/a |       n/a | not explicitly reported     |

```math id="f7e0aj"
P(\Delta A>0)=\frac{1}{N}\sum_{n=1}^{N}\mathbf{1}(\Delta A_n>0)
```

---

### Summary (1–2 lines)

* Minimum Infrastructure Package (MIP) supported by the paper: **L1–L3**
* Clear cost-effectiveness boundary: **L3→L4 (MCI=0.43)**

```
