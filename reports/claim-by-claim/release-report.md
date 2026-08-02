- Previous live judged score: `5/10`
- Conservative projected score range after the proposed change: `7–9/10`
- Best-supported possible new score: `9/10` — forecast, not a judge result

# Release forecast

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 1 | 2 | HIGH | VERIFIED | Exact schedule, 512×64 scale, 64 seeds, explicit-bound replay, independent moments, failing control; “optimal” terminology depends on cited lower-bound literature |
| 2 | 1 | 2 | HIGH | VERIFIED | Exact eta0 changes linearly with omega and omega-deleted control fails; conditional asymptotic rate is not directly iterated |
| 3 | 1 | 2 | HIGH | VERIFIED | Exact data flow excludes omega, matched mutation fails, named update has no projection/averaging; conditional asymptotic rate is not directly iterated |
| 4 | 1 | 1 | MEDIUM | BLOCKED | Exponential factor verified over tau 5–598, but the paper explicitly labels proof-artifact status a conjecture |
| 5 | 1 | 2 | HIGH | VERIFIED | Exhaustive initial states on 12 chains, 60 boundary rows, independent TV checker, off-by-one control |

Current total score: `5/10`.
Conservative projected total score range: `7–9/10`.
Best-supported possible total: `9/10`, only as a forecast.

Claims 1, 2, 3, and 5 materially changed since the previous verdict. Claim 4
remains BLOCKED because resolving “proof artifact” requires a sharper proof,
lower bound, or assumption-satisfying counterexample.

Exact publication action after every release gate passes: upload only the
text-file allowlist to the existing `DineshAI/ppIhZgFCTI` Space using the
Hugging Face API, verify the returned revision and hashes, then mirror the same
text paths plus this report and notebook to GitHub `main`.

[Complete command ledger](command-ledger.md) ·
[illustrated scientific report](report.md)

HF Jobs bill CPU Upgrade at `$0.0005/minute` (`$0.03/hour`). Completed jobs
before final validation consumed 13 rounded billing minutes, approximately
`$0.0065`; final totals are recomputed after the release-validation run.
