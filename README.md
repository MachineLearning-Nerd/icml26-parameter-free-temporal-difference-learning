# Towards Parameter-Free Temporal Difference Learning — reproduction

![Exact exponential schedule converges while the control stalls](reports/claim-by-claim/images/headline_td_scaling.svg)

This repository reproduces the five judged claims of arXiv:2603.02577. The
strongest result is Theorem 3.4: exact horizon-specific TD(0), on three
512-state/64-feature MDPs with 64 seeds, reduced last-iterate MSE from about
`0.40` at `T=5,000` to `0.0066–0.0074` at `T=250,000`, with slopes
`-1.089,-1.085,-1.068`; the paper predicts a `ln²(T)/T` variance form.
The constant-step control stalled near `0.119` with slope `-0.005`.

**Live judge result (2026-08-02): 6/10.** Claims 1 and 5 are VERIFIED; Claims 2
and 3 remain TOY because exact formula/data-flow checks do not replace an actual
trajectory run at the theorem-prescribed horizons; Claim 4 is INCONCLUSIVE
because the paper itself calls the proof-artifact interpretation a conjecture.
The campaign's internal contracts still verify the exact omega dependency and
removal in Claims 2 and 3, but they did not earn full empirical credit.

[Detailed illustrated report](reports/claim-by-claim/report.md) ·
[release forecast](reports/claim-by-claim/release-report.md) ·
[raw evidence](space/evidence) ·
[tutorial notebook](notebooks/td_reproduction.py)

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-ppIhZgFCTI-towards-parameter-free-temporal-difference-learning/blob/main/notebooks/td_reproduction.py)

## Reproduction scope

Paper schedule for Claim 1: `eta0=(1-gamma)/8`, not the reciprocal used by the
historical rejected baseline. The full-dimensional run uses HF `cpu-upgrade`
only; no GPU or local scientific compute. Exact Markovian theorem conditions
first become feasible around `10^11–10^60` iterations, so those claims are
verified as exact dependency/data-flow statements and their unmeasured
conditional convergence regimes are disclosed.

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | Publication surface | Not run as an experiment (publication surface) | Mirrors the winning report and Space text | — |
| [`orx/baseline-exact-definition-4-1-contract`](https://github.com/MachineLearning-Nerd/icml26-repro-ppIhZgFCTI-towards-parameter-free-temporal-difference-learning/tree/orx/baseline-exact-definition-4-1-contract) | Exact Claim 5 baseline | `uv sync --frozen && uv run --no-sync python -m td_repro` | VERIFIED, 60/60; off-by-one rejected 60/60 | HF cpu-upgrade, no GPU, 21s job |
| [`orx/claims-1-4-theorem-calibrated-cumulative-suite`](https://github.com/MachineLearning-Nerd/icml26-repro-ppIhZgFCTI-towards-parameter-free-temporal-difference-learning/tree/orx/claims-1-4-theorem-calibrated-cumulative-suite) | Full-dimensional Claim 1 and exact Claims 2–4 audits | `uv sync --frozen && uv run --no-sync python -m td_repro` | Claims 1–3 VERIFIED; Claim 4 BLOCKED; Claim 5 regression passes | HF cpu-upgrade, no GPU, 2m38s job |
| [`orx/cumulative-proof-replay-and-evaluator-evidence`](https://github.com/MachineLearning-Nerd/icml26-repro-ppIhZgFCTI-towards-parameter-free-temporal-difference-learning/tree/orx/cumulative-proof-replay-and-evaluator-evidence) | Proof replay and evaluator-visible artifact | `uv sync --frozen && uv run --no-sync python -m td_repro` | All scientific checks and Space verifier pass | HF cpu-upgrade, no GPU, 2m44s job |
| [`orx/final-artifact-validation`](https://github.com/MachineLearning-Nerd/icml26-repro-ppIhZgFCTI-towards-parameter-free-temporal-difference-learning/tree/orx/final-artifact-validation) | Final report, notebook, and blind traversal | `uv sync --frozen && uv run --no-sync python -m td_repro` | All scientific and artifact checks pass; `marimo check` passes | HF cpu-upgrade, no GPU, 2m44s job |
| [`orx/publication-manifest-and-final-release-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-ppIhZgFCTI-towards-parameter-free-temporal-difference-learning/tree/orx/publication-manifest-and-final-release-audit) | Exact text allowlist and SHA-256 release manifest | `uv sync --frozen && uv run --no-sync python -m td_repro` | All release gates pass; 44-path manifest is complete | HF cpu-upgrade, no GPU, 2m38s job |
| [`orx/post-publication-exact-revision-verification`](https://github.com/MachineLearning-Nerd/icml26-repro-ppIhZgFCTI-towards-parameter-free-temporal-difference-learning/tree/orx/post-publication-exact-revision-verification) | Fresh download and live revision audit | `uv sync --frozen && uv run --no-sync python -m td_repro` | Published revision hashes, navigation, verifier, and displayed/raw numbers pass | HF cpu-upgrade, no GPU, 2m02s job |

## Run locally for inspection

Formal evidence was generated remotely. To inspect the tutorial:

```bash
uv sync --frozen
uv run marimo edit notebooks/td_reproduction.py
```

The fixed formal command is:

```bash
uv sync --frozen && uv run --no-sync python -m td_repro
```
