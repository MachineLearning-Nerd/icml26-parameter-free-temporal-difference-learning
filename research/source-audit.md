# Paper source and exact claim anchors

Retrieved on 2026-08-02 with an explicit research-audit User-Agent.

| Source | SHA-256 | Relevant anchors |
| --- | --- | --- |
| `https://export.arxiv.org/e-print/2603.02577` | `b895345df9e25880ef21a9637f206cfb90110379337a4c8c62070b9a3df2ed70` | `notations_sec.tex:43-56`; `sgd.tex:112-124,147-154,302-351` |
| `https://ar5iv.labs.arxiv.org/html/2603.02577` | `028bf78be98345c09a3718c4152a6fa5e3c8c9edf11e4540cf07af05e3988fd6` | `#S3.Thmtheorem4`, `#S4.Thmtheorem1`, `#S4.Thmtheorem10`, `#S4.Thmtheorem12` |

Assumption 2.1 requires an irreducible, aperiodic policy-induced chain with a unique stationary distribution. Assumption 2.2 requires a full-column-rank feature matrix and `||phi(s)||^2 <= 1` for every state. `omega` is the smallest eigenvalue of `Sigma=Phi^T D Phi`.

Theorem 3.4 uses `eta_0=(1-gamma)/8`, not `1/[8(1-gamma)]`. Theorem 4.10 uses an omega-dependent `eta_0=(1-gamma)omega / (2[C ln^2(T)+C'])`. Theorem 4.12 uses `lambda=1/sqrt(T)` and `eta_0=lambda / ([C ln^2(T)+C']+(8+2lambda^2))`, with no omega in the algorithmic rule. The paper states that the `exp(m/log(1/rho))` factor induces exponential mixing-time dependence and explicitly labels its artifact interpretation a conjecture.

