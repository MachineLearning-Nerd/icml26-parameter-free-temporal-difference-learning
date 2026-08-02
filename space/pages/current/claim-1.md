# Claim 1 — i.i.d. last-iterate TD(0)

**Verdict: VERIFIED. Confidence: HIGH for the explicit Theorem 3.4 contract;
MEDIUM for the paper's informal “optimal” terminology.**

## Exact claim and assumptions

Theorem 3.4 uses independent stationary transitions and
`eta_t=eta0 alpha^t`, with `eta0=(1-gamma)/8` and `alpha=T^(-1/T)`.
The displayed last-iterate parameter-MSE bound is an exponentially decaying
bias plus `8 sigma^2 ln^2(T)/[e(omega(1-gamma))^2 alpha^2 T]`.
The schedule does not contain omega. Source: `thm:exp_iid`, ar5iv
`S3.Thmtheorem4`; audited HTML SHA-256
`028bf78be98345c09a3718c4152a6fa5e3c8c9edf11e4540cf07af05e3988fd6`.

All three MDPs are finite positive refresh chains with uniform stationarity,
512 states and 64 full-rank features. Every feature row has norm at most one;
rewards including noise have magnitude at most 0.4. The feature spectra were
fixed before the run and give omega `0.0102173`, `0.00797916`, `0.00553670`.

## Evidence first

| omega | T=5,000 MSE | T=250,000 MSE | log-log slope | all 95% CIs below exact bound |
| ---: | ---: | ---: | ---: | --- |
| 0.0102173 | 0.3952 ± 0.0054 | 0.006625 ± 0.000320 | -1.089 | yes |
| 0.00797916 | 0.4001 ± 0.0055 | 0.006800 ± 0.000325 | -1.085 | yes |
| 0.00553670 | 0.4129 ± 0.0055 | 0.007379 ± 0.000355 | -1.068 | yes |

Each row uses 64 deterministic trajectories and independently restarts with the
horizon-specific schedule at `T={5k,20k,80k,250k}`. All 12 observed means plus
95% intervals lie below the explicit bound. [All primary and control rows](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/evidence/claim1/results.csv).

## Independent proof and control

An independent scalar second-moment recursion gives MSE
`4.6303020e-6`; 20,000 direct trajectories give `4.6354965e-6`, only
`0.111` Monte Carlo standard errors apart. The algebraic replay reconstructs
the norm expansion, TD lemma substitutions, `eta<=c/8` absorption, covariance
step, product unrolling, and X/Y helper inequalities.

The paper appendix prints `alpha^t` once inside an `i`-indexed product. The
replay uses `alpha^i`, required by the recurrence and used by the paper on its
immediately following line. This disclosed index typo does not change the
corrected derivation.

Negative control: the identical MDP/noise setup with constant `eta_t=eta0`
has slope `-0.0052` and a variance floor near `0.1187`, so it is rejected.

Code: [standalone verifier](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/code/current_verifier.py).
Checker/control: [machine output](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/evidence/claim1/checks.json).
[Proof replay output](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/evidence/claim1/proof_replay.json) ·
[full generator source](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/code/claim1.py).

## Provenance and limitations

Exact command: `uv sync --frozen && uv run --no-sync python -m td_repro`.
Git `b592c39b47e584ab29cbcdfe4494d0f6b300895c`; run
`95f8445d-21d1-417d-aa5e-bdf97e5a0a84`; seeds recorded in raw evidence.
Estimate 16 cores; HF `cpu-upgrade`; actual 64 AMD EPYC 7R13 CPUs; no GPU.
Scientific runtime 134.736 s; job duration 2m38s.

The “optimal” priority/lower-bound wording relies on cited literature; this
campaign verifies the achieved last-iterate bias/variance form and exact bound,
not a historical priority claim.
