# Claim-by-claim gap analysis

Compared artifacts:

- judged candidate: `DineshAI/ppIhZgFCTI@c281038c74481058728ae953bfe0c3707b6c4f5f`
- public reference: `michaldobiezynski/repro-towards-parameter-free-temporal-difference-learning@be52f518059c154d2439b53a043cdf8280e85cbb`
- live verdict dataset: `ICML-2026-agent-repro/verdicts@032252713cb3f66d7214b8108d6a3052f1a02f20`, filtered only by `space_id == "DineshAI/ppIhZgFCTI"`

| Claim | Judged gap | Sound reference pattern to rerun | Reference limitation not adopted |
| --- | --- | --- | --- |
| 1 | n=6,d=4; wrong displayed `eta_0`; no instance-optimal floor | d=100/n=200, exact constants, bias/variance split, LSTD floor, omega and schedule controls | narrative-only evidence and no downloadable raw data/code |
| 2 | does not use Theorem 4.10 omega-dependent step | matched i.i.d./Markov comparison and explicit formula audit | reference uses `eta_0=1.0`, not the theorem's stated rule |
| 3 | no omega-requiring comparator; toy scale | multi-omega family, regularization offset, no projection/averaging audit | reference substitutes `eta_0=30 lambda` for the theorem's rule |
| 4 | only two chains; slow case diverges | dense two-decade mixing sweep and polynomial-vs-exponential comparison | finite family cannot prove the authors' universal conjectural interpretation |
| 5 | one six-state chain; fitted rho treated as envelope | n=100-200 family and multiple thresholds | fitted spectral rho is not automatically a certified `m rho^t` envelope |

Evaluator-visible gaps in both public artifacts include absent downloadable raw CSV/JSON, absent current executable source, absent independent checker output, absent failing controls, absent locked environment/Git/CPU provenance, and no visibility matrix. The new candidate must expose each item from its canonical entrypoint.

