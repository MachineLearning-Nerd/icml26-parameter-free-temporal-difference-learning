# Claim 5 — Definition 4.1

**Verdict: VERIFIED.** This is a definition-level verification, not an empirical
convergence theorem. It exhausts all point-mass initial distributions for 12
finite chains with 32, 128, and 512 states.

## Exact source contract

Definition 4.1 assumes
`sup_mu0 dTV(P_pi^t mu0, mu_pi) <= m rho^t` for every `t in N_0` and defines,
for every `delta in (0,1)`,

`tau_delta = min { t in N_0 : m rho^t <= delta }`.

Source: arXiv:2603.02577, Definition 4.1, LaTeX label `def:reg_mixing_time`,
ar5iv anchor `S4.Thmtheorem1`. Retrieved 2026-08-02 with explicit User-Agent;
HTML SHA-256 `028bf78be98345c09a3718c4152a6fa5e3c8c9edf11e4540cf07af05e3988fd6`.
[Machine-readable contract](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/evidence/claim5/claim_contract.json) and
[source audit](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/evidence/claim5/source_audit.md).

## Assumptions and method

The checker uses refresh chains
`P = rho I + (1-rho) 1 pi^T` with uniform `pi`. Every transition is positive,
so each chain is irreducible and aperiodic. For this family the exact envelope
constant is `m=1-1/n`. The grid was fixed before observing first hits:

- `n in {32,128,512}` and `rho in {0.5,0.75,0.875,0.9375}`;
- `delta in {0.1,0.05,0.01,0.001,m rho^7}`;
- all `n` point-mass initial distributions, which attain the convex worst case.

The primary implementation iterates `m rho^t`. An independent implementation
instead evolves every distribution by
`mu_(t+1)=rho mu_t+(1-rho)pi`, computes TV directly, and finds its first crossing.
It does not call the primary first-hit function.

## Raw result

All **60/60** rows agreed. All 12 chain audits passed. The maximum discrepancy
between directly evolved TV and the closed form was
`5.583641188300348e-17`. Representative boundary rows:

| n | rho | delta | tau by definition | tau by direct TV | TV(tau-1) | TV(tau) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 32 | 0.5 | 0.007568359375 | 7 | 7 | 0.01513671875 | 0.007568359375 |
| 128 | 0.9375 | 0.05 | 47 | 47 | 0.0509650513 | 0.0477797356 |
| 512 | 0.9375 | 0.001 | 108 | 108 | 0.0010001785 | 0.0009376673 |

Download all 60 rows: [results.csv](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/evidence/claim5/results.csv).

## Independent checker and negative control

- Independent direct-TV checker: PASS; maximum discrepancy `5.584e-17`.
  [Machine-readable output](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/evidence/claim5/checker.json).
- Negative control: replace every answer by `tau_delta+1`. It was rejected on
  **60/60** rows, as intended. [Machine-readable output](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/evidence/claim5/control.json).
- The [executable verifier](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/main/code/claim5_verifier.py) exits nonzero if any
  primary row, assumption audit, independent result, or negative control fails.

## Reproduction and provenance

Exact fixed command:

```text
uv sync --frozen && uv run --no-sync python -m td_repro
```

Environment: Python 3.12.12, `uv.lock` SHA-256
`601569afc6a023d8b3e121157364d78b96eb24234cb5fd2c1558b86736007f22`.
Git SHA: `8a72923f14410d7d88c139ca66ca4c2cbae43579`.
HF run: `5639f97d-bb2e-47f6-878c-5f728815dcd5`.
Estimate: 1 core. Selected: HF `cpu-upgrade`. Actual allocation: 64 logical
and affinity CPUs, AMD EPYC 7R13, no GPU. Scientific runtime: 0.161 s; total
orchestrated job duration: 21 s. The test is deterministic and uses no random seeds.

## Limitations

This verifies the exact definition and boundary behavior over a predeclared
family; it does not prove any TD convergence theorem or an exponential error law.
The family is analytically tractable by design, but it is not a toy spot check:
the worst case is exhausted at up to 512 states, multiple exact equality boundaries
are included, and two independent computational routes must agree.

This page and `code/claim5_verifier.py` supersede the historical six-state
verification. Historical files remain unchanged and reachable.
