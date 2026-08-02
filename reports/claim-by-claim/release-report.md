- Previous live judged score: `5/10`
- Conservative projected score range after the proposed change: `7–9/10`
- Best-supported possible new score: `9/10` — forecast, not a judge result

# Release forecast

**Live judge result:** `6/10` at 2026-08-02T09:42:44+00:00 on published
revision `ca74b23c1429bf2f3ae54320bb7289bcc8fb6b24`. The pre-publication forecast
above was optimistic; the actual verdicts were VERIFIED, TOY, TOY,
INCONCLUSIVE, VERIFIED.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 2 | 2 | HIGH | VERIFIED | Live judge accepted the exact schedule, 512×64 scale, 64 seeds, bound replay, independent moments, and failing control |
| 2 | 1 | 2 | HIGH | TOY (live judge) | Exact eta0 dependency is machine-checked, but no trajectory run reaches the theorem-prescribed schedule and conditions |
| 3 | 1 | 2 | HIGH | TOY (live judge) | Exact omega-free data flow is machine-checked, but no trajectory run reaches the theorem-prescribed schedule and conditions |
| 4 | 0 | 1 | MEDIUM | INCONCLUSIVE (live judge); BLOCKED internally | Exponential factor is verified, but proof-artifact causality is explicitly conjectural |
| 5 | 2 | 2 | HIGH | VERIFIED | Live judge accepted exhaustive initial states on 12 chains, 60 boundary rows, independent TV checker, and off-by-one control |

Current live judged score: `6/10`.
Pre-publication projected range: `7–9/10`.
Pre-publication best-supported possible total: `9/10`; this was a forecast and
was not achieved.

Claims 1 and 5 moved from TOY to VERIFIED. Claims 2 and 3 remained TOY because
formula inspection did not substitute for prescribed-schedule trajectories.
Claim 4 moved from TOY to INCONCLUSIVE; resolving it still requires a sharper
proof, lower bound, or assumption-satisfying counterexample.

## Publication state

Baseline HF Head and Judge Head were both
`c281038c74481058728ae953bfe0c3707b6c4f5f`; the previous live judged score
remains `5/10`. The text-only Hugging Face API upload used the exact allowlist
and returned Space revision
`ca74b23c1429bf2f3ae54320bb7289bcc8fb6b24`. The live judge evaluated that
exact revision at 2026-08-02T09:42:44+00:00 and recorded the 6/10 breakdown
above.

Winning experiment branch:
`orx/post-publication-exact-revision-verification`, Git
`0a750c33ab91de7b231ad11079510070a8ed496f`. The actual Space candidate was
frozen at its parent `orx/publication-manifest-and-final-release-audit`, Git
`f879068316a1313360f411480d2540bf51666c77`.

## Experiment tree summary

| Stage | Git | HF job | Outcome |
| --- | --- | --- | --- |
| Exact Definition 4.1 baseline | `8a72923` | 21s | Claim 5 VERIFIED |
| Theorem-calibrated cumulative suite | `b592c39` | 2m38s | Claims 1–3 VERIFIED; Claim 4 BLOCKED; Claim 5 regression passes |
| Proof replay and evaluator evidence | `48d7e73` | 2m44s | Proof replay and visible verifier pass |
| Visual release candidate | `dabe06b` | 3m31s | Five HF-generated SVGs and report pass |
| Final artifact validation | `b21b8b4` | 2m44s | Science, visibility, secret, subset, and marimo gates pass |
| Publication manifest | `f879068` | 2m38s | Exact 44-path allowlist and manifest pass |
| Published revision verification | `0a750c3` | 2m02s | Fresh download, hashes, traversal, verifier, and number parity pass |

The final-artifact node also records one 3m26s setup-only failure: the old
marimo version lacked `marimo check`, and one protected JSON copy had gained a
trailing newline. The same provisional node was repaired and rerun. Marimo was
therefore pinned from 0.14.17 to 0.23.14; NumPy and the scientific dependencies
were unchanged. This release-tooling lock change is disclosed because the
environment was not byte-identical to the earlier frozen nodes.

## Release gates and provenance

- Fixed command on every formal node: `uv sync --frozen && uv run --no-sync python -m td_repro`.
- Compute: HF `cpu-upgrade`; estimate 16 cores for cumulative runs; actual 64
  affinity/logical AMD EPYC 7R13 CPUs; no GPU.
- Nine submitted jobs consumed 20m30s wall time. Per-job minute rounding gives
  25 billed minutes, approximately `$0.0125` at the documented
  [`$0.0005/minute`](https://huggingface.co/docs/hub/jobs-pricing) rate.
- The old/new subset check found no missing or changed judged evidence. The
  published upload manifest SHA-256 is
  `0d973c061d1d393cea85e1edcbc7a33409db566ea53cacdff51ccd8a0ef18673`.
- The post-publication HF run downloaded all 44 allowlisted paths into a fresh
  directory at the exact revision. It found zero upload hash mismatches and
  zero protected-history mismatches, opened all reachable current and
  historical pages, obtained verifier exit code 0, and matched displayed result
  numbers to raw files for all five claims.
- The exact publication action was: add only the allowlisted text files to the
  existing `DineshAI/ppIhZgFCTI` Space through one API commit, verify its exact
  revision on HF CPU, then mirror the repository presentation and the exact
  `space/` text paths to GitHub `main`.

[Complete command ledger](command-ledger.md) ·
[illustrated scientific report](report.md) ·
[post-publication machine record](post-publication-verification.json) ·
[exact upload allowlist](../../space/evidence/release/upload-allowlist.txt) ·
[SHA-256 manifest](../../space/evidence/release/upload-manifest.sha256)
