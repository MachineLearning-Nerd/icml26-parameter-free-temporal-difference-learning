from __future__ import annotations

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPACE = ROOT / "space"
JUDGED = "c281038c74481058728ae953bfe0c3707b6c4f5f"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_protected_subset() -> dict:
    manifest = ROOT / ".openresearch" / "protected" / "judged-space-c281038c.manifest.sha256"
    missing = []
    mismatched = []
    for line in manifest.read_text().splitlines():
        expected, relative = line.split("  ./", 1)
        current = SPACE / relative
        if not current.exists():
            missing.append(relative)
            continue
        if relative in {"README.md", "logbook.json"}:
            current = SPACE / "historical" / f"judged-{JUDGED}" / relative
        if sha256(current) != expected:
            mismatched.append(relative)
    return {"missing": missing, "hash_mismatches": mismatched, "passed": not missing and not mismatched}


def validate_navigation() -> dict:
    logbook = json.loads((SPACE / "logbook.json").read_text())
    nodes = [logbook["root"], *logbook["root"]["children"]]
    missing = [node["file"] for node in nodes if not (SPACE / node["file"]).exists()]
    current = (SPACE / logbook["root"]["file"]).read_text()
    slugs = {node["slug"] for node in logbook["root"]["children"]}
    broken_routes = [slug for slug in re.findall(r"\(#/([^)]+)\)", current) if slug not in slugs]
    visibility_complete = "Missing" not in current and all(f"| {claim} |" in current for claim in range(1, 6))
    return {"missing_pages": missing, "broken_routes": broken_routes, "visibility_complete": visibility_complete, "passed": not missing and not broken_routes and visibility_complete}


def validate_claim_pages() -> dict:
    failures = []
    required = ("Verdict", "Source", "Raw", "verifier")
    for claim in range(1, 6):
        path = SPACE / "pages" / "current" / f"claim-{claim}.md"
        text = path.read_text()
        absent = [token for token in required if token.lower() not in text.lower()]
        if absent:
            failures.append({"claim": claim, "missing_tokens": absent})
    return {"failures": failures, "passed": not failures}


def validate_figures() -> dict:
    names = (
        "headline_td_scaling.svg",
        "bound_calibration.svg",
        "omega_dependency.svg",
        "mixing_factor.svg",
        "feasible_horizons.svg",
    )
    failures = []
    for name in names:
        report_path = ROOT / "reports" / "claim-by-claim" / "images" / name
        space_path = SPACE / "images" / name
        try:
            ET.parse(report_path)
            ET.parse(space_path)
        except (ET.ParseError, FileNotFoundError) as error:
            failures.append({"name": name, "error": str(error)})
            continue
        if sha256(report_path) != sha256(space_path):
            failures.append({"name": name, "error": "report/Space hash mismatch"})
    return {"failures": failures, "passed": not failures}


def validate_no_secrets() -> dict:
    suspicious = []
    patterns = (re.compile(r"hf_[A-Za-z0-9]{20,}"), re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----"))
    for path in SPACE.rglob("*"):
        if not path.is_file() or path.suffix.lower() in {".png", ".ico"}:
            continue
        text = path.read_text(errors="ignore")
        if any(pattern.search(text) for pattern in patterns):
            suspicious.append(str(path.relative_to(SPACE)))
    return {"suspicious_files": suspicious, "passed": not suspicious}


def validate_upload_allowlist() -> dict:
    allowlist_path = SPACE / "evidence" / "release" / "upload-allowlist.txt"
    paths = [line for line in allowlist_path.read_text().splitlines() if line]
    missing = [path for path in paths if path != "evidence/release/upload-manifest.sha256" and not (SPACE / path).is_file()]
    non_text = []
    hashes = {}
    for relative in paths:
        path = SPACE / relative
        if not path.exists():
            continue
        try:
            path.read_text()
        except UnicodeDecodeError:
            non_text.append(relative)
        hashes[relative] = sha256(path)
    return {"paths": paths, "missing": missing, "non_text": non_text, "sha256": hashes, "passed": not missing and not non_text and len(paths) == len(set(paths))}


def main() -> int:
    checks = {
        "protected_subset": validate_protected_subset(),
        "navigation": validate_navigation(),
        "claim_pages": validate_claim_pages(),
        "figures": validate_figures(),
        "secret_scan": validate_no_secrets(),
        "upload_allowlist": validate_upload_allowlist(),
    }
    passed = all(check["passed"] for check in checks.values())
    print(json.dumps({"passed": passed, "checks": checks}, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
