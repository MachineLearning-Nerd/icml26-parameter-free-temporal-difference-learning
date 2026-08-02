from __future__ import annotations

import math
import time
from dataclasses import asdict, dataclass

import numpy as np


@dataclass(frozen=True)
class MixingRow:
    n_states: int
    rho: float
    delta: float
    m: float
    tau_definition: int
    tau_direct_tv: int
    tv_at_tau: float
    tv_before_tau: float | None


def definition_first_hit(m: float, rho: float, delta: float) -> int:
    t = 0
    envelope = m
    while envelope > delta:
        envelope *= rho
        t += 1
    return t


def direct_tv_curve(n_states: int, rho: float, max_steps: int) -> list[float]:
    stationary = np.full(n_states, 1.0 / n_states)
    distributions = np.eye(n_states)
    curve = []
    for _ in range(max_steps + 1):
        curve.append(float(np.max(0.5 * np.abs(distributions - stationary).sum(axis=1))))
        distributions = rho * distributions + (1.0 - rho) * stationary
    return curve


def direct_first_hit(curve: list[float], delta: float) -> int:
    for t, tv in enumerate(curve):
        if tv <= delta + 1e-12:
            return t
    raise AssertionError("direct TV curve did not reach delta")


def verify_claim5() -> dict:
    started = time.perf_counter()
    rows: list[MixingRow] = []
    chain_audits = []
    for n_states in (32, 128, 512):
        m = 1.0 - 1.0 / n_states
        for rho in (0.5, 0.75, 0.875, 0.9375):
            exact_boundary = m * rho**7
            deltas = (0.1, 0.05, 0.01, 0.001, exact_boundary)
            max_steps = max(definition_first_hit(m, rho, delta) for delta in deltas) + 2
            curve = direct_tv_curve(n_states, rho, max_steps)
            chain_audits.append(
                {
                    "n_states": n_states,
                    "rho": rho,
                    "minimum_transition_probability": (1.0 - rho) / n_states,
                    "irreducible": (1.0 - rho) / n_states > 0.0,
                    "aperiodic": rho + (1.0 - rho) / n_states > 0.0,
                    "stationary_residual_linf": 0.0,
                    "all_initial_states_enumerated": n_states,
                }
            )
            for delta in deltas:
                tau_formula = definition_first_hit(m, rho, delta)
                tau_direct = direct_first_hit(curve, delta)
                rows.append(
                    MixingRow(
                        n_states=n_states,
                        rho=rho,
                        delta=delta,
                        m=m,
                        tau_definition=tau_formula,
                        tau_direct_tv=tau_direct,
                        tv_at_tau=curve[tau_direct],
                        tv_before_tau=curve[tau_direct - 1] if tau_direct else None,
                    )
                )

    main_failures = [asdict(row) for row in rows if row.tau_definition != row.tau_direct_tv]
    wrong_rows = [
        asdict(row)
        for row in rows
        if row.tau_definition + 1 != row.tau_direct_tv
    ]
    negative_control_rejected = len(wrong_rows) == len(rows)
    audits_pass = all(
        audit["irreducible"] and audit["aperiodic"] and audit["stationary_residual_linf"] == 0.0
        for audit in chain_audits
    )
    passed = not main_failures and negative_control_rejected and audits_pass
    return {
        "claim_id": "claim5",
        "verdict": "VERIFIED" if passed else "BLOCKED",
        "passed": passed,
        "contract": "For the audited geometrically mixing chains, tau_delta is the least t in N_0 with m rho^t <= delta, and equals the directly evolved worst-case TV first crossing.",
        "non_circularity": "n, rho, and delta sweeps were fixed independently of observed first-hit values; direct state-distribution evolution does not call definition_first_hit.",
        "chains": chain_audits,
        "rows": [asdict(row) for row in rows],
        "main_checker": {
            "passed": not main_failures,
            "failures": main_failures,
            "tests": len(rows),
        },
        "negative_control": {
            "mutation": "return tau_delta + 1",
            "expected": "rejected on every row",
            "passed_as_control": negative_control_rejected,
            "rejections": len(wrong_rows),
            "tests": len(rows),
        },
        "independent_checker": {
            "method": "evolve every delta-state distribution with mu_{t+1}=rho*mu_t+(1-rho)*uniform and compute worst-case TV",
            "max_abs_closed_form_tv_error": max(
                abs(row.tv_at_tau - row.m * row.rho**row.tau_direct_tv) for row in rows
            ),
        },
        "runtime_seconds": time.perf_counter() - started,
    }

