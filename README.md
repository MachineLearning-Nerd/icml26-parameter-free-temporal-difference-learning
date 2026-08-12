# Towards Parameter-Free Temporal Difference Learning

Independent ICML 2026 reproduction and claim-audit workspace for [OpenReview `ppIhZgFCTI`](https://openreview.net/forum?id=ppIhZgFCTI) and [arXiv `2603.02577`](https://arxiv.org/abs/2603.02577). It records the paper's five claims, the exact path that produces each result, the experiment history, and the limits of the evidence.

## Outcome first

The live evaluator scored the published artifact **6/10**: Claims 1 and 5 were **VERIFIED**, Claims 2 and 3 were **TOY**, and Claim 4 was **INCONCLUSIVE**. The local campaign's stronger machine-checkable verdicts are also recorded: Claim 1 passed its explicit finite-T contract, Claims 2 and 3 passed exact parameter-dependency audits, Claim 4 is blocked because the paper labels the proof-artifact interpretation a conjecture, and Claim 5 passed exhaustive definition/boundary checks. The live score is authoritative for this collection; a formula audit is not silently presented as a theorem-scale trajectory reproduction.

## Repository identity

| Field | Value |
| --- | --- |
| Collection name | `icml26-parameter-free-temporal-difference-learning` |
| Previous collection name | `icml26-repro-ppIhZgFCTI-towards-parameter-free-temporal-difference-learning` |
| Paper | *Towards Parameter-Free Temporal Difference Learning* |
| Authors | Yunxiang Li, Mark Schmidt, Reza Babanezhad, Sharan Vaswani |
| OpenReview | [`ppIhZgFCTI`](https://openreview.net/forum?id=ppIhZgFCTI) |
| arXiv | [`2603.02577`](https://arxiv.org/abs/2603.02577) |
| Hugging Face artifact | [`DineshAI/ppIhZgFCTI`](https://huggingface.co/spaces/DineshAI/ppIhZgFCTI) |
| Source archive | `b895345df9e25880ef21a9637f206cfb90110379337a4c8c62070b9a3df2ed70` |
| Audited HTML | `028bf78be98345c09a3718c4152a6fa5e3c8c9edf11e4540cf07af05e3988fd6` |
| Clean branch policy | The normalized copy keeps one public branch: `main` |

No author GitHub implementation is linked in the audited paper/source records. The executable code, reports, verifiers, raw evidence, and publication artifact in this repository are the reproduction work, not an author release.

## Claim ledger

Each row separates the paper statement, the production path, and the current verdict. Evidence paths are the canonical checked-in artifacts.

| Claim | Paper statement | How the claim is produced | Checked-in evidence | Local / live status |
| --- | --- | --- | --- | --- |
| C1 | Under i.i.d. sampling, exponential-step TD(0) achieves the optimal last-iterate bias/variance trade-off without knowing `ω` (Theorem 3.4). | Construct three 512-state/64-feature refresh MDPs; run 64 deterministic trajectories at `T={5k,20k,80k,250k}` with `η₀=(1−γ)/8` and `α=T^(−1/T)`; compare MSE and 95% CIs with the explicit bound; replay the second moment independently; reject constant-step control. | [`space/evidence/claim1/`](space/evidence/claim1/), [`reports/claim-by-claim/report.md`](reports/claim-by-claim/report.md) | **Verified** internally; **VERIFIED** live. |
| C2 | In the Markovian setting, standard TD(0) needs `ω` in `η₀` (Theorem 4.10). | Evaluate the exact `η₀=(1−γ)ω/[2(C ln²T+C')]` formula over `ω={0.02,0.01,0.005}`; reject an `ω`-deleted mutation; independently find the first horizon satisfying all theorem conditions. | [`space/evidence/claim2/`](space/evidence/claim2/), [`src/td_repro/theorem_audit.py`](src/td_repro/theorem_audit.py) | **Verified** for formula/data-flow dependency; **TOY** live because no trajectory reaches the extreme theorem horizon. |
| C3 | Regularized Markovian TD(0) removes `ω` from the algorithmic rule without projections or iterate averaging (Theorem 4.12). | Trace `λ=1/√T` and `η₀=λ/[C(λ)ln²T+C'(λ)+8+2λ²]`; compare three `ω` values; reject an `ω`-injected mutation; calibrate exact feasible horizons. | [`space/evidence/claim3/`](space/evidence/claim3/), [`src/td_repro/theorem_audit.py`](src/td_repro/theorem_audit.py) | **Verified** for exact parameter removal and structure; **TOY** live because direct theorem-horizon trajectories were not run. |
| C4 | The exponential dependence on mixing time in the regularized analysis is a proof artifact (discussion after Theorem 4.12). | Evaluate `exp(m/log(1/ρ))` over 13 predeclared `ρ` values and distinguish the exact bound factor from the paper's explicitly conjectural artifact interpretation. | [`space/evidence/claim4/`](space/evidence/claim4/), [`space/pages/current/claim-4.md`](space/pages/current/claim-4.md) | **BLOCKED** internally; **INCONCLUSIVE** live. The factor is checked, but the universal artifact claim is not resolved. |
| C5 | Definition 4.1 gives the first time `τδ` at which the geometric total-variation envelope falls below `δ`. | Exhaust every point-mass initial state on 12 refresh chains (`n={32,128,512}`); compare the closed-form first crossing with an independent direct-TV evolution; reject `τδ+1`. | [`space/evidence/claim5/`](space/evidence/claim5/), [`src/td_repro/claim5.py`](src/td_repro/claim5.py) | **Verified**: 60/60 rows, maximum discrepancy `5.584e−17`; **VERIFIED** live. |

### Common execution path

The canonical command is fixed across the formal campaign:

```bash
uv sync --frozen
uv run --no-sync python -m td_repro
```

The command dispatches to the claim implementations under [`src/td_repro/`](src/td_repro/), writes machine-readable results under `space/evidence/`, and runs artifact/verifier checks. The public Trackio-style pages under [`space/pages/current/`](space/pages/current/) expose the same claim-by-claim evidence and links. The exact environment is Python 3.12.12 with the locked dependency graph in [`uv.lock`](uv.lock); the recorded scientific runs used Hugging Face `cpu-upgrade`, no GPU, and 64 AMD EPYC 7R13 logical CPUs.

## What the paper is doing

The paper studies linear-function-approximation TD(0) under two sampling regimes:

- With i.i.d. samples from the stationary distribution, it uses a horizon-specific exponential step-size schedule to make the last iterate balance initialization bias against sampling variance without requiring the smallest feature-covariance eigenvalue `ω`.
- With a single Markovian trajectory, it analyzes standard TD(0), whose initial step size depends on `ω`, and a regularized variant whose rule removes that dependency and avoids projections and iterate averaging.

The reproduction therefore separates practical numerical evidence from exact theorem structure. Claims 2 and 3 require horizons as large as approximately `10^11`–`10^60` under the audited constants and mixing values; the repository reports those feasibility calculations instead of substituting a convenient step size and calling it a full theorem reproduction.

## Branch audit and normalization

The original workspace used `orx/*` branches for sequential experiment nodes. Every branch below is an ancestor of the final `main` commit, so the normalized copy can preserve its provenance through immutable commit links while deleting the noisy branch names. The branch-purpose descriptions are based on each tip commit and the files introduced before the next node.

| Original branch | Tip commit | What it did |
| --- | --- | --- |
| `main` | [`e4262e84`](https://github.com/MachineLearning-Nerd/icml26-parameter-free-temporal-difference-learning/tree/e4262e84b855a9eb553b446c50ffdf0ef762c6ce) | Final publication surface and live 6/10 judge result. |
| `orx/baseline-exact-definition-4-1-contract` | [`85c4fdfa`](https://github.com/MachineLearning-Nerd/icml26-parameter-free-temporal-difference-learning/tree/85c4fdfa59831b8a73cb29b88ffa36b88b9a3ec3) | Established the exact Claim 5 definition contract and first verifier. |
| `orx/claim-5-evaluator-visible-exact-verifier` | [`b93e050a`](https://github.com/MachineLearning-Nerd/icml26-parameter-free-temporal-difference-learning/tree/b93e050a8a153ca0fe32468450321d613f896ba2) | Exposed Claim 5's executable verifier and evaluator-visible evidence. |
| `orx/claims-1-4-theorem-calibrated-cumulative-suite` | [`e8f3639c`](https://github.com/MachineLearning-Nerd/icml26-parameter-free-temporal-difference-learning/tree/e8f3639c6f4acc8cbfcdaebdf0e66018d84695d0) | Added the theorem-calibrated C1–C4 audit, exact formulas, controls, and horizon search. |
| `orx/cumulative-proof-replay-and-evaluator-evidence` | [`ffab58c0`](https://github.com/MachineLearning-Nerd/icml26-parameter-free-temporal-difference-learning/tree/ffab58c0b9f2ba0d6b9c6b607ba39f1ecbb96a6f) | Added independent proof replay, cumulative evidence, and release red-team material. |
| `orx/visual-report-and-release-candidate` | [`fe93fad1`](https://github.com/MachineLearning-Nerd/icml26-parameter-free-temporal-difference-learning/tree/fe93fad1ee267e35b57fceb7649cc69f3486a1a1) | Generated the five report figures and assembled the visual release candidate. |
| `orx/final-artifact-validation` | [`ffa6ad14`](https://github.com/MachineLearning-Nerd/icml26-parameter-free-temporal-difference-learning/tree/ffa6ad14284d9e1ffc9a9db02acfaadd0f473ac1) | Repaired and ran final artifact, environment, traversal, and manifest validation. |
| `orx/publication-manifest-and-final-release-audit` | [`793a87d1`](https://github.com/MachineLearning-Nerd/icml26-parameter-free-temporal-difference-learning/tree/793a87d147a60686002663ae87b0a92e7236e807) | Added the exact 44-path publication allowlist and SHA-256 release manifest. |
| `orx/post-publication-exact-revision-verification` | [`1f668a2e`](https://github.com/MachineLearning-Nerd/icml26-parameter-free-temporal-difference-learning/tree/1f668a2e083295919db2141b774fcaff35608bfe) | Downloaded the published Space revision afresh and verified hashes, navigation, verifier output, and displayed/raw parity. |
| `publication/claim-by-claim-20260802` | [`e4262e84`](https://github.com/MachineLearning-Nerd/icml26-parameter-free-temporal-difference-learning/tree/e4262e84b855a9eb553b446c50ffdf0ef762c6ce) | Publication alias pointing at the final `main` head. |

The author/reproduction history is not rewritten in the paper or HF artifact. Only this GitHub collection copy is normalized: its final public branch is `main`, and all collection commits are attributed to `MachineLearning-Nerd <37579156+MachineLearning-Nerd@users.noreply.github.com>`.

## Reproduction limitations

- The formal runs are CPU evidence and do not claim GPU acceleration or a different hardware result.
- C2 and C3 exact dependency audits do not replace trajectory runs at the theorem-prescribed horizons.
- C4's proof-artifact interpretation is explicitly conjectural in the paper; the honest verdict remains unresolved.
- C5 checks a definition and its boundary behavior, not TD convergence.
- Historical six-state evidence remains under `space/historical/` for provenance but is not the current result.

## Citation

```bibtex
@article{li2026towards,
  author  = {Yunxiang Li and Mark Schmidt and Reza Babanezhad and Sharan Vaswani},
  title   = {Towards Parameter-Free Temporal Difference Learning},
  journal = {arXiv preprint arXiv:2603.02577},
  year    = {2026},
  doi     = {10.48550/arXiv.2603.02577},
  url     = {https://arxiv.org/abs/2603.02577}
}
```

## Thank you

Thank you to Yunxiang Li, Mark Schmidt, Reza Babanezhad, and Sharan Vaswani for the theoretical work and for making the paper available to the research community. This reproduction records both successful checks and unresolved limitations so that the authors' claims receive clear credit without overstating what the experiments establish.
