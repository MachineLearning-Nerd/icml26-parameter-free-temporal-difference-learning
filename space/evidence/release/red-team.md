# Evaluator-blind pre-publication review

The reviewer used only the candidate artifact and the judge rubric. Repository
knowledge and OpenResearch logs were excluded.

## Round 1 — gaps found

Files opened, in order: `README.md`, `logbook.json`, `pages/index.md`,
`pages/claims/page.md`, `pages/verification-run/page.md`, then the first draft
of `pages/current/index.md` and `pages/current/claim-5.md`.

Conclusions that could not be verified from that traversal:

- the old navigation did not distinguish current from historical verification;
- Claim 5's raw rows, checker, control, and exact source were not linked;
- Claims 1–4 had no current canonical pages;
- no current cumulative verifier or pinned environment was visible;
- the old Claim 4 language did not distinguish the exact bound factor from the
  paper's conjectural “proof artifact” interpretation.

Fixes: current pages now precede historical pages, the old pages are labeled
exactly **Historical rejected baseline**, every claim has inline numbers and raw
links, `code/current_verifier.py` is the obvious verifier, and Claim 4 is BLOCKED.

## Round 2 — after fixes

Files opened, in order: `README.md`, `logbook.json`, `pages/current/index.md`,
`pages/current/claim-1.md` through `claim-5.md`, `code/current_verifier.py`,
`environment/pyproject.toml`, `environment/LOCK.md`, every file under
`evidence/claim1` through `evidence/claim5`, and the historical manifest.

The reviewer located for every claim: exact source anchor and quantifiers,
assumptions, inline data, raw download, checker, deliberately wrong control,
fixed command, Git/run provenance, CPU/runtime details, limitations, and an
executable verifier that exits nonzero on mismatch. Claim 4 remains unresolved
scientifically, but its BLOCKED basis and exact bound-factor evidence are fully
discoverable. No missing visibility-matrix cell remains.

The GitHub report and notebook links are supplementary; all scoring evidence is
present inside the Space candidate itself. External links are rechecked after
the exact text is mirrored to GitHub main.
