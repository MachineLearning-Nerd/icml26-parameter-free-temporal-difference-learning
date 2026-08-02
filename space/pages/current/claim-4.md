# Claim 4 — exponential mixing dependence versus proof artifact

**Verdict: BLOCKED. Confidence: MEDIUM that BLOCKED is the only faithful verdict.**

Source: arXiv:2603.02577, discussion immediately after Theorem 4.12,
`thm:reg_markov`; audited HTML SHA-256 `028bf78be98345c09a3718c4152a6fa5e3c8c9edf11e4540cf07af05e3988fd6`.

The exact Theorem 4.12 bound contains `exp(m/log(1/rho))`. A 13-point
predeclared sweep verifies its scale directly:

| rho | tau_0.05 | log10 bound factor |
| ---: | ---: | ---: |
| 0.5 | 5 | 0.625 |
| 0.9 | 29 | 4.114 |
| 0.95 | 59 | 8.450 |
| 0.975 | 119 | 17.119 |
| 0.99 | 298 | 43.126 |
| 0.995 | 598 | 86.468 |

The factor is strictly increasing at all 13 points; replacing it by a constant
is rejected. This fixes the historical two-configuration comparison and avoids
interpreting divergence as controlled exponential error scaling.

The stronger phrase “is an artifact” is not a theorem. Immediately after
Theorem 4.12 the paper says, “We conjecture” that the worse dependence is an
artifact of the analysis. A finite chain sweep cannot resolve that universal
claim. Without a machine-checkable sharper proof, a matching lower bound, or an
assumption-satisfying counterexample, VERIFIED or FALSIFIED would be dishonest.

[All 13 raw rows](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/evidence/claim4/results.csv) ·
[current verifier](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/code/current_verifier.py) ·
[factor-sweep source](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/code/theorem_audit.py).
