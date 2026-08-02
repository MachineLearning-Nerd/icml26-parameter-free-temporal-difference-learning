# Claim 3 — regularization removes omega from the Markovian rule

**Verdict: VERIFIED for the exact parameter-removal and algorithm-structure
claim. Confidence: HIGH.**

Theorem 4.12 sets `lambda=1/sqrt(T)` and
`eta0=lambda/[C ln^2(T)+C'+8+2lambda^2]`. Its data-flow symbols are only
`T`, `lambda`, `C(lambda)`, and `C'(lambda)`; omega is unreachable. At
`T=10^6`, the same eta0 `8.4416948e-12` is obtained for omega
`0.02,0.01,0.005`. An omega-injected mutation produces three distinct outputs
and is rejected. The named code path is regularized TD(0), returns the last
iterate, and contains neither projection nor iterate averaging.

This is a matched comparison with Claim 2: its standard eta0 changes 4x over
the same omega sweep while the regularized eta0 is invariant.

The independently calibrated first exact horizons are `10^18.0598` for
rho 0.6/0.9 and `10^59.8180` for rho 0.99. Direct iteration is unavailable,
so no substituted practical step size is used to claim convergence.

[Raw JSON](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/evidence/claim3/results.json) ·
[current verifier](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/code/current_verifier.py).

Command and compute are identical to Claim 1. Run `95f8445d-21d1-417d-aa5e-bdf97e5a0a84`,
Git `b592c39`, HF `cpu-upgrade`, 64 actual CPUs, no GPU.
