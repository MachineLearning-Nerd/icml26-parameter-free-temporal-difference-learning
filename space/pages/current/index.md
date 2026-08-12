# Claim-by-claim reproduction

This is the canonical evaluator entrypoint for the current campaign. Evidence is
accepted only when a committed verifier exits nonzero on failure, its independent
checker agrees, and a deliberately wrong control is rejected.

![Headline TD scaling](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/images/headline_td_scaling.svg)

[Illustrated report on GitHub](https://github.com/MachineLearning-Nerd/icml26-parameter-free-temporal-difference-learning/blob/main/reports/claim-by-claim/report.md) ·
[tutorial notebook](https://github.com/MachineLearning-Nerd/icml26-parameter-free-temporal-difference-learning/blob/main/notebooks/td_reproduction.py)

## Current status

| Claim | Canonical page | Status | Scope |
| --- | --- | --- | --- |
| 1 — i.i.d. TD(0) | [Current verification](#/current-claim-1) | VERIFIED | Exact schedule, proof replay, 512 states, 64 features, 64 seeds |
| 2 — Markovian TD(0) | [Current verification](#/current-claim-2) | VERIFIED | Exact omega dependency; convergence-horizon limitation disclosed |
| 3 — regularized TD(0) | [Current verification](#/current-claim-3) | VERIFIED | Exact omega-free data flow; convergence-horizon limitation disclosed |
| 4 — mixing dependence | [Current verification](#/current-claim-4) | BLOCKED | Exponential bound verified; proof-artifact interpretation is conjectural |
| 5 — Definition 4.1 | [Current verification](#/current-claim-5) | VERIFIED | Exact definition; exhaustive initial states on 12 refresh chains |

## Visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Claim 1](#/current-claim-1) | Yes | Yes | CSV | Yes | Yes | Yes | VERIFIED |
| 2 | [Claim 2](#/current-claim-2) | Yes | Yes | JSON | Yes | Yes | Yes | VERIFIED |
| 3 | [Claim 3](#/current-claim-3) | Yes | Yes | JSON | Yes | Yes | Yes | VERIFIED |
| 4 | [Claim 4](#/current-claim-4) | Yes | Yes | CSV | Yes | Yes | Yes | BLOCKED |
| 5 | [Claim 5](#/current-claim-5) | [Python](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/code/claim5_verifier.py) | Yes | [CSV](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/evidence/claim5/results.csv) | Inline + JSON | Inline + JSON | Yes | VERIFIED |

## Historical evidence

The earlier six-state work remains available in the navigation and is labeled
**Historical rejected baseline**. It is preserved for provenance, but is not the
current verification.
