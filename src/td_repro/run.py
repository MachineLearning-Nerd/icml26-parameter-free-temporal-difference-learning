from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

from td_repro.claim1 import verify_claim1
from td_repro.claim5 import verify_claim5
from td_repro.figures import make_figures
from td_repro.post_publication import verify_published_revision
from td_repro.theorem_audit import verify_theorem_audits


ROOT = Path(__file__).resolve().parents[2]
FIXED_COMMAND = "uv sync --frozen && uv run --no-sync python -m td_repro"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_sha() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def cpu_allocation() -> dict:
    affinity = None
    if hasattr(os, "sched_getaffinity"):
        affinity = len(os.sched_getaffinity(0))
    model = "unknown"
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        for line in cpuinfo.read_text().splitlines():
            if line.lower().startswith("model name"):
                model = line.split(":", 1)[1].strip()
                break
    return {
        "estimated_cores_required": 16,
        "selected_backend": "hf",
        "selected_flavor": "cpu-upgrade",
        "logical_cpus": os.cpu_count(),
        "affinity_cpus": affinity,
        "cpu_model": model,
        "gpu_used": False,
    }


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def main() -> int:
    started = time.perf_counter()
    claim1 = verify_claim1()
    theorem_claims = verify_theorem_audits()
    claim5 = verify_claim5()
    visible_verifier = subprocess.run(
        [sys.executable, str(ROOT / "space" / "code" / "current_verifier.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    artifact_commands = {
        "artifact_validation": [sys.executable, "-m", "td_repro.artifact_validation"],
        "marimo_check": [sys.executable, "-m", "marimo", "check", "notebooks/td_reproduction.py"],
    }
    artifact_validators = {}
    for name, command in artifact_commands.items():
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
        artifact_validators[name] = {
            "command": " ".join(command),
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    post_publication = verify_published_revision()
    runtime = time.perf_counter() - started
    evidence = {
        "paper": "arXiv:2603.02577",
        "run_started_utc": datetime.now(UTC).isoformat(),
        "git_sha": git_sha(),
        "fixed_command": FIXED_COMMAND,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "uv_lock_sha256": file_sha256(ROOT / "uv.lock"),
        "compute": cpu_allocation(),
        "deterministic_seeds": claim1["deterministic_seeds"],
        "claims": [claim1, *theorem_claims, claim5],
        "evaluator_visible_verifier": {
            "command": "python space/code/current_verifier.py",
            "returncode": visible_verifier.returncode,
            "stdout": visible_verifier.stdout.strip(),
            "stderr": visible_verifier.stderr.strip(),
        },
        "artifact_validators": artifact_validators,
        "post_publication_verification": post_publication,
        "all_claims_passed": claim1["passed"] and all(claim["passed"] for claim in theorem_claims) and claim5["passed"] and visible_verifier.returncode == 0 and all(item["returncode"] == 0 for item in artifact_validators.values()) and post_publication["passed"],
        "total_runtime_seconds": runtime,
    }
    evidence["report_figures_svg_base64"] = make_figures(evidence["claims"])
    artifact_dir = ROOT / ".openresearch" / "artifacts" / "claim5"
    write_json(artifact_dir / "raw" / "results.json", evidence)
    write_json(artifact_dir / "independent_checker_output.json", claim5["independent_checker"])
    write_json(artifact_dir / "negative_control_output.json", claim5["negative_control"])
    for claim in evidence["claims"]:
        claim_dir = ROOT / ".openresearch" / "artifacts" / claim["claim_id"]
        write_json(claim_dir / "raw" / "results.json", claim)
        if "independent_checker" in claim:
            write_json(claim_dir / "independent_checker_output.json", claim["independent_checker"])
        if "proof_replay" in claim:
            write_json(claim_dir / "proof_replay.json", claim["proof_replay"])
        if "negative_control" in claim:
            write_json(claim_dir / "negative_control_output.json", claim["negative_control"])
    print("OPENRESEARCH_EVIDENCE_BEGIN")
    print(json.dumps(evidence, indent=2, sort_keys=True))
    print("OPENRESEARCH_EVIDENCE_END")
    return 0 if evidence["all_claims_passed"] else 1
