from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen


REVISION = "ca74b23c1429bf2f3ae54320bb7289bcc8fb6b24"
BASE_URL = f"https://huggingface.co/spaces/DineshAI/ppIhZgFCTI/resolve/{REVISION}"
MANIFEST_PATH = "evidence/release/upload-manifest.sha256"
MANIFEST_SHA256 = "0d973c061d1d393cea85e1edcbc7a33409db566ea53cacdff51ccd8a0ef18673"
JUDGED = "c281038c74481058728ae953bfe0c3707b6c4f5f"
ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def download(relative: str, target: Path) -> None:
    request = Request(f"{BASE_URL}/{quote(relative, safe='/')}?download=true", headers={"User-Agent": "OpenResearch-PostPublication-Audit/1.0"})
    with urlopen(request, timeout=60) as response:
        payload = response.read()
    destination = target / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(payload)


def read_csv(root: Path, relative: str) -> list[dict[str, str]]:
    with (root / relative).open(newline="") as handle:
        return list(csv.DictReader(handle))


def displayed_result_checks(root: Path) -> dict[str, bool]:
    pages = {claim: (root / f"pages/current/claim-{claim}.md").read_text() for claim in range(1, 6)}

    claim1_rows = read_csv(root, "evidence/claim1/results.csv")
    primary = [row for row in claim1_rows if row["scale_floor"] != "control_constant_step"]
    groups = {}
    for row in primary:
        groups.setdefault(row["scale_floor"], []).append(row)
    claim1 = all(
        f"{float(rows[0]['mean_mse']):.4f}" in pages[1]
        and f"{float(rows[-1]['mean_mse']):.6f}" in pages[1]
        and f"{float(rows[-1]['log_log_slope']):.3f}" in pages[1]
        for rows in groups.values()
    )

    claim2_data = json.loads((root / "evidence/claim2/results.json").read_text())
    claim2 = all(f"{eta:.4e}" in pages[2] for eta in claim2_data["eta0"]) and all(
        f"{value:.4f}" in pages[2] for value in claim2_data["first_feasible_log10_T"].values()
    )

    claim3_data = json.loads((root / "evidence/claim3/results.json").read_text())
    claim3 = f"{claim3_data['eta0'][0]:.7e}" in pages[3] and all(
        f"{value:.4f}" in pages[3] for value in claim3_data["first_feasible_log10_T"].values()
    )

    claim4_rows = read_csv(root, "evidence/claim4/results.csv")
    displayed_rhos = {"0.5", "0.9", "0.95", "0.975", "0.99", "0.995"}
    claim4 = all(
        row["tau_0.05"] in pages[4] and f"{float(row['log10_bound_factor']):.3f}" in pages[4]
        for row in claim4_rows
        if row["rho"] in displayed_rhos
    )

    claim5_rows = read_csv(root, "evidence/claim5/results.csv")
    claim5_checker = json.loads((root / "evidence/claim5/checker.json").read_text())
    claim5_control = json.loads((root / "evidence/claim5/control.json").read_text())
    claim5 = (
        f"{len(claim5_rows)}/{len(claim5_rows)}" in pages[5]
        and str(claim5_checker["max_abs_closed_form_tv_error"]) in pages[5]
        and f"{claim5_control['rejections']}/{claim5_control['tests']}" in pages[5]
    )
    return {"claim1": claim1, "claim2": claim2, "claim3": claim3, "claim4": claim4, "claim5": claim5}


def verify_published_revision() -> dict:
    with tempfile.TemporaryDirectory(prefix="published-space-") as temporary:
        target = Path(temporary)
        download("evidence/release/upload-allowlist.txt", target)
        download(MANIFEST_PATH, target)
        allowlist = [line for line in (target / "evidence/release/upload-allowlist.txt").read_text().splitlines() if line]
        manifest = {}
        for line in (target / MANIFEST_PATH).read_text().splitlines():
            digest, relative = line.split("  ", 1)
            manifest[relative] = digest

        for relative in allowlist:
            if not (target / relative).exists():
                download(relative, target)
        upload_hash_mismatches = [relative for relative, digest in manifest.items() if sha256(target / relative) != digest]
        manifest_hash_matches = sha256(target / MANIFEST_PATH) == MANIFEST_SHA256
        allowlist_complete = set(allowlist) == set(manifest) | {MANIFEST_PATH}

        protected_mismatches = []
        protected_manifest = ROOT / ".openresearch/protected/judged-space-c281038c.manifest.sha256"
        for line in protected_manifest.read_text().splitlines():
            expected, original = line.split("  ./", 1)
            remote = f"historical/judged-{JUDGED}/{original}" if original in {"README.md", "logbook.json"} else original
            if not (target / remote).exists():
                download(remote, target)
            if sha256(target / remote) != expected:
                protected_mismatches.append(original)

        readme = (target / "README.md").read_text()
        logbook = json.loads((target / "logbook.json").read_text())
        reachable = [logbook["root"]["file"], *(node["file"] for node in logbook["root"]["children"])]
        for relative in reachable:
            if not (target / relative).exists():
                download(relative, target)
        index = (target / logbook["root"]["file"]).read_text()
        claim_pages = [(target / f"pages/current/claim-{claim}.md").read_text() for claim in range(1, 6)]
        traversal_passed = (
            "#/current" in readme
            and logbook["root"]["file"] == "pages/current/index.md"
            and "Missing" not in index
            and all(f"| {claim} |" in index for claim in range(1, 6))
            and all("verifier" in page.lower() and "raw" in page.lower() and "verdict" in page.lower() for page in claim_pages)
        )

        verifier = subprocess.run(
            [sys.executable, str(target / "code/current_verifier.py")],
            cwd=target,
            text=True,
            capture_output=True,
            check=False,
        )
        number_checks = displayed_result_checks(target)
        passed = (
            not upload_hash_mismatches
            and manifest_hash_matches
            and allowlist_complete
            and not protected_mismatches
            and traversal_passed
            and verifier.returncode == 0
            and all(number_checks.values())
        )
        return {
            "revision": REVISION,
            "fresh_directory": True,
            "uploaded_paths_checked": len(allowlist),
            "upload_hash_mismatches": upload_hash_mismatches,
            "manifest_hash_matches": manifest_hash_matches,
            "allowlist_complete": allowlist_complete,
            "protected_historical_mismatches": protected_mismatches,
            "reachable_pages_opened": reachable,
            "canonical_traversal_passed": traversal_passed,
            "current_verifier_returncode": verifier.returncode,
            "current_verifier_stdout": verifier.stdout.strip(),
            "displayed_result_numbers_match_raw": number_checks,
            "passed": passed,
        }
