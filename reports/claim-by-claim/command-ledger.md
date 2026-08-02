# Reproduction command ledger

Generated HF job wrappers and credentials are intentionally excluded. The fixed
scientific command is recorded verbatim; all scientific work was launched by
`orx exp run`.

## Startup and source audit

```text
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx skill orx-reports
orx projects --json
orx project view 96dcb489-a0e2-43fe-9fe1-2d395e85bc2b
orx runs 96dcb489-a0e2-43fe-9fe1-2d395e85bc2b
git status --short
git branch -a
git rev-parse HEAD
git ls-remote origin refs/heads/main
df -h .
orx paper 2603.02577
```

Paper HTML and arXiv source were retrieved with User-Agent
`OpenResearch-Reproduction-Audit/1.0 (paper 2603.02577; contact via repository)`.
The exact judged and reference Spaces and verdict dataset were downloaded at
their recorded revisions with `hf download`; tokens were never printed.

## Fixed environment and command

```text
uv lock
uv lock --check
orx project edit 96dcb489-a0e2-43fe-9fe1-2d395e85bc2b --run-command 'uv sync --frozen && uv run --no-sync python -m td_repro'
```

## Experiment tree and launches

Every node was created with `orx create-experiment 96dcb489-a0e2-43fe-9fe1-2d395e85bc2b`
and the parent recorded in the dashboard. Launches:

```text
orx exp run 29b780af-b8e3-4770-bbb8-df21e70f5747 --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 30m
orx exp run 6c68c432-513b-40e2-b138-edb4dc47d19f --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 30m
orx exp run d22b1b76-3f7e-41e7-a105-875187d04da8 --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 45m
orx exp run be0d89e6-4ba5-4428-8127-a1f146c34b2f --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 45m
orx exp run 11032dea-cc30-4f6a-a039-e3e3490b2677 --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 45m
orx exp run 3ddd2e89-7219-40f7-af80-d213ed4bffff --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 30m
orx exp run 3ddd2e89-7219-40f7-af80-d213ed4bffff --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 30m
orx exp run daa125c6-7e93-4a32-b9ff-c138423d3ea7 --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 30m
orx exp run 80505713-311b-4c85-a81b-36477f69a036 --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 30m
```

The first final-artifact run returned 1 because its release validators found a
missing marimo CLI command and a one-byte protected-file mismatch; it did not
answer a scientific claim. The provisional node was repaired and the identical
command was rerun successfully. The first post-publication submission attempt
was rejected before job creation by an HF API rate limit; the listed command
was resubmitted after the five-minute window and produced the recorded run.

Each launch was followed by `orx exp wait <experiment-id> --timeout 480`,
`orx runs 96dcb489-a0e2-43fe-9fe1-2d395e85bc2b --experiment <id>`, and
`orx logs <run-id>`. Node findings were saved with `orx exp desc <id> --set`.

## Static edit-box checks

```text
python3 -m py_compile <changed Python files>
jq empty <changed JSON files>
git diff --check
git status --short
git fetch origin
git checkout <experiment branch>
git push -u origin <experiment branch>
```

No training, verification, benchmark, data generation, notebook validation, or
figure generation was executed by these local inspection commands.

## Publication and post-publication audit

The existing Space head was checked immediately before mutation and equaled
`c281038c74481058728ae953bfe0c3707b6c4f5f`. A local orchestration-only Python
call to `huggingface_hub.HfApi.create_commit` added the 44 paths in
`space/evidence/release/upload-allowlist.txt`, with that judged head supplied as
`parent_commit`. It returned
`ca74b23c1429bf2f3ae54320bb7289bcc8fb6b24`.

The post-publication fixed-command run then used only standard-library HTTPS to
download that exact revision into a fresh HF job directory. It verified the
published manifest, the historical subset, canonical traversal, current
verifier, and displayed/raw numerical parity before returning 0.
