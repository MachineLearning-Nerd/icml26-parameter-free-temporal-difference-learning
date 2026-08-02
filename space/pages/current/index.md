# Claim-by-claim reproduction

This is the canonical evaluator entrypoint for the current campaign. Evidence is
accepted only when a committed verifier exits nonzero on failure, its independent
checker agrees, and a deliberately wrong control is rejected.

## Current status

| Claim | Canonical page | Status | Scope |
| --- | --- | --- | --- |
| 1 — i.i.d. TD(0) | Pending | BLOCKED | Exact theorem audit complete; full verifier pending |
| 2 — Markovian TD(0) | Pending | BLOCKED | Exact theorem audit complete; full verifier pending |
| 3 — regularized TD(0) | Pending | BLOCKED | Exact theorem audit complete; full verifier pending |
| 4 — mixing dependence | Pending | BLOCKED | Paper states a conjectured proof artifact; verifier pending |
| 5 — Definition 4.1 | [Current verification](#/current-claim-5) | VERIFIED | Exact definition; exhaustive initial states on 12 refresh chains |

## Visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Pending | Missing | Missing | Missing | Missing | Missing | Pending | BLOCKED |
| 2 | Pending | Missing | Missing | Missing | Missing | Missing | Pending | BLOCKED |
| 3 | Pending | Missing | Missing | Missing | Missing | Missing | Pending | BLOCKED |
| 4 | Pending | Missing | Missing | Missing | Missing | Missing | Pending | BLOCKED |
| 5 | [Claim 5](#/current-claim-5) | [Python](../code/claim5_verifier.py) | Yes | [CSV](../evidence/claim5/results.csv) | Inline + [JSON](../evidence/claim5/checker.json) | Inline + [JSON](../evidence/claim5/control.json) | Yes | VERIFIED |

## Historical evidence

The earlier six-state work remains available in the navigation and is labeled
**Historical rejected baseline**. It is preserved for provenance, but is not the
current verification.
