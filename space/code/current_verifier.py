"""Evaluator-visible cumulative verifier. Exits nonzero on any failed contract."""

from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def claim1() -> bool:
    rows = read_csv("evidence/claim1/results.csv")
    primary = [row for row in rows if row["scale_floor"] != "control_constant_step"]
    control = [row for row in rows if row["scale_floor"] == "control_constant_step"]
    checks = read_json("evidence/claim1/checks.json")
    return (
        len(primary) == 12
        and len(control) == 4
        and all(row["bound_satisfied"] == "true" for row in primary)
        and all(float(row["log_log_slope"]) < -0.8 for row in primary)
        and all(float(row["log_log_slope"]) > -1.3 for row in primary)
        and float(control[-1]["mean_mse"]) > 0.1
        and abs(float(control[-1]["log_log_slope"])) < 0.25
        and checks["independent_checker"]["absolute_z_score"] < 5.0
        and checks["negative_control"]["passed_as_control"] is True
        and checks["compute"]["gpu_used"] is False
    )


def claim2() -> bool:
    data = read_json("evidence/claim2/results.json")
    omega = data["omega"]
    eta = data["eta0"]
    return (
        data["verdict"] == "VERIFIED"
        and all(abs(eta[i] / eta[i + 1] - omega[i] / omega[i + 1]) < 1e-12 for i in range(2))
        and data["negative_control"] == {"mutation": "delete omega", "rejections": 2, "tests": 2, "passed": True}
    )


def claim3() -> bool:
    data = read_json("evidence/claim3/results.json")
    return (
        data["verdict"] == "VERIFIED"
        and max(data["eta0"]) == min(data["eta0"])
        and data["omega_reachable_in_data_flow"] is False
        and data["negative_control"]["distinct_outputs"] == 3
        and data["negative_control"]["passed"] is True
    )


def claim4() -> bool:
    rows = read_csv("evidence/claim4/results.csv")
    factors = [float(row["log10_bound_factor"]) for row in rows]
    taus = [int(row["tau_0.05"]) for row in rows]
    return len(rows) == 13 and all(a < b for a, b in zip(factors, factors[1:])) and all(a < b for a, b in zip(taus, taus[1:]))


def claim5() -> bool:
    rows = read_csv("evidence/claim5/results.csv")
    checker = read_json("evidence/claim5/checker.json")
    control = read_json("evidence/claim5/control.json")
    return (
        len(rows) == 60
        and all(row["tau_definition"] == row["tau_direct_tv"] for row in rows)
        and checker["max_abs_closed_form_tv_error"] < 1e-12
        and checker["passed"] is True
        and control["rejections"] == control["tests"] == 60
        and control["passed_as_control"] is True
    )


def main() -> int:
    results = {"claim1": claim1(), "claim2": claim2(), "claim3": claim3(), "claim4_blocked_evidence": claim4(), "claim5": claim5()}
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
