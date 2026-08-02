"""Current Claim 5 verifier; extracted from Git SHA 8a72923 for evaluator use."""

import sys

import numpy as np


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


def verify() -> bool:
    tests = 0
    rejections = 0
    max_error = 0.0
    for n_states in (32, 128, 512):
        m = 1.0 - 1.0 / n_states
        for rho in (0.5, 0.75, 0.875, 0.9375):
            minimum_transition_probability = (1.0 - rho) / n_states
            if minimum_transition_probability <= 0.0:
                return False
            deltas = (0.1, 0.05, 0.01, 0.001, m * rho**7)
            max_steps = max(definition_first_hit(m, rho, d) for d in deltas) + 2
            curve = direct_tv_curve(n_states, rho, max_steps)
            for delta in deltas:
                tau = definition_first_hit(m, rho, delta)
                direct = next(t for t, tv in enumerate(curve) if tv <= delta + 1e-12)
                tests += 1
                rejections += int(tau + 1 != direct)
                max_error = max(max_error, abs(curve[direct] - m * rho**direct))
                if tau != direct:
                    return False
    print({"tests": tests, "off_by_one_rejections": rejections, "max_error": max_error})
    return tests == 60 and rejections == 60 and max_error < 1e-12


if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
