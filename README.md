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

확인해봤고, **업로드 자체는 정상입니다.** 다만 **README.md가 중간부터 마크다운이 깨져서(중복/코드펜스 꼬임/$$ 수식 남음)** “근거자료(재현성)”로는 보이지만, **가독성/신뢰성 측면에서 손해**를 보고 있어요.

## 1) 업로드 확인 결과

아래 3개 파일이 **정상 위치에 존재**합니다.

* `assumptions/cost_assumptions.md` 존재 ([GitHub][1])
* `outputs/scenario_summary.csv` 존재 ([GitHub][2])
* `repro/level_toggles.md` 존재 ([GitHub][3])

즉, **파일 커밋은 제대로 됐습니다.**

---

## 2) 문제점: README가 “How to Compute” 이후 깨짐

README에서

* `## How to Compute (Pseudo-code)` 다음에
* `## Reproducibility`가 먼저 나오고,
* Step 0가 **중복으로 두 번** 나오며,
* ` ````markdown` 같은 **깨진 코드펜스**가 끼고,
* `$$...$$` 수식이 그대로 남아 GitHub에서 렌더링이 불안정합니다. ([GitHub][4])

이 상태면 심사자가 GitHub를 봤을 때 “정리가 덜 됐다” 인상을 받을 수 있어요.

---

## 3) 가장 빠른 수정: README에서 “How to Compute”부터 끝까지 **통째로 교체**

GitHub에서 `README.md` 편집(Edit) → 아래 블록으로 **완전히 교체**하세요.

### 교체 시작 지점

`## How to Compute (Pseudo-code)` 라인부터 **파일 끝까지 전부 삭제** 후, 아래를 붙여넣기.

### 붙여넣기 블록 (100% GitHub 호환)

````markdown
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
````

### Step 1) Compute generalized travel time matrix for each scenario

```math
t_{ij}(s)=t^{drive}_{ij}(s)+E[W](s)+\lambda\cdot P90(W)(s)+\phi\cdot P(cancel)(s)+\psi\cdot E[MTTR](s)
```

### Step 2) Compute accessibility

```math
A_{cum,i}(T;s)=\sum_j O_j\cdot \mathbf{1}(t_{ij}(s)\le T)
```

```math
A_{grav,i}(s)=\sum_j O_j\cdot e^{-\beta t_{ij}(s)}
```

### Step 3) Improvements vs baseline

```math
\Delta A(s)=\bar{A}(s)-\bar{A}(S0)
```

### Step 4) MCI boundary

```math
MA_{k\rightarrow k+1}=\bar{A}(s_{k+1})-\bar{A}(s_k)
```

```math
MC_{k\rightarrow k+1}=C_{k+1}-C_k
```

```math
MCI_{k\rightarrow k+1}=\frac{MA_{k\rightarrow k+1}}{MC_{k\rightarrow k+1}}
```

### Step 5) Monte Carlo robustness

```math
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

````

[1]: https://github.com/warnymic/hadong-its/tree/main/assumptions "hadong-its/assumptions at main · warnymic/hadong-its · GitHub"
[2]: https://github.com/warnymic/hadong-its/tree/main/outputs "hadong-its/outputs at main · warnymic/hadong-its · GitHub"
[3]: https://github.com/warnymic/hadong-its/tree/main/repro "hadong-its/repro at main · warnymic/hadong-its · GitHub"
[4]: https://github.com/warnymic/hadong-its/blob/main/README.md "hadong-its/README.md at main · warnymic/hadong-its · GitHub"
