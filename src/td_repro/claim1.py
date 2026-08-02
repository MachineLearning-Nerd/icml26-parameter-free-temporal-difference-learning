from __future__ import annotations

import math
import time

import numpy as np


N_STATES = 512
N_FEATURES = 64
N_SEEDS = 64
HORIZONS = (5_000, 20_000, 80_000, 250_000)
GAMMA = 0.5
RHO = 0.6
NOISE = 0.2
ETA0 = (1.0 - GAMMA) / 8.0


def make_problem(scale_floor: float) -> dict:
    rng = np.random.default_rng(260302577)
    q, _ = np.linalg.qr(rng.normal(size=(N_STATES, N_FEATURES)))
    scales = np.linspace(1.0, scale_floor, N_FEATURES)
    features = q * scales
    features /= np.linalg.norm(features, axis=1).max()
    reward_direction = rng.normal(size=N_FEATURES)
    raw_reward = features @ reward_direction
    rewards = 0.2 * raw_reward / np.abs(raw_reward).max()
    stationary_feature = features.mean(axis=0)
    expected_next = RHO * features + (1.0 - RHO) * stationary_feature
    covariance = features.T @ features / N_STATES
    td_matrix = features.T @ (features - GAMMA * expected_next) / N_STATES
    td_rhs = features.T @ rewards / N_STATES
    optimum = np.linalg.solve(td_matrix, td_rhs)
    omega = float(np.linalg.eigvalsh(covariance)[0])
    return {
        "features": features,
        "rewards": rewards,
        "optimum": optimum,
        "omega": omega,
        "max_feature_norm": float(np.linalg.norm(features, axis=1).max()),
        "rank": int(np.linalg.matrix_rank(features)),
        "stationary_residual": 0.0,
        "max_abs_reward": float(np.abs(rewards).max() + NOISE),
    }


def simulate(problem: dict, constant_step: bool = False) -> list[dict]:
    features = problem["features"]
    rewards = problem["rewards"]
    optimum = problem["optimum"]
    snapshots = []
    for horizon in HORIZONS:
        rng = np.random.default_rng((314159 if constant_step else 271828) + horizon)
        weights = np.zeros((N_SEEDS, N_FEATURES))
        alpha = horizon ** (-1.0 / horizon)
        for t in range(1, horizon + 1):
            states = rng.integers(N_STATES, size=N_SEEDS)
            next_states = states.copy()
            refresh = rng.random(N_SEEDS) >= RHO
            next_states[refresh] = rng.integers(N_STATES, size=int(refresh.sum()))
            reward_noise = np.where(rng.random(N_SEEDS) < 0.5, -NOISE, NOISE)
            phi = features[states]
            phi_next = features[next_states]
            prediction = np.einsum("ij,ij->i", phi, weights)
            next_prediction = np.einsum("ij,ij->i", phi_next, weights)
            td_error = rewards[states] + reward_noise + GAMMA * next_prediction - prediction
            eta = ETA0 if constant_step else ETA0 * alpha**t
            weights += eta * td_error[:, None] * phi
        squared_errors = np.square(weights - optimum).sum(axis=1)
        snapshots.append(
            {
                "T": horizon,
                "mean_squared_parameter_error": float(squared_errors.mean()),
                "ci95_half_width": float(1.96 * squared_errors.std(ddof=1) / math.sqrt(N_SEEDS)),
                "median_squared_parameter_error": float(np.median(squared_errors)),
                "rate_normalized_error": float(squared_errors.mean() * horizon / math.log(horizon) ** 2),
            }
        )
    return snapshots


def exact_sigma_squared(problem: dict) -> float:
    features = problem["features"]
    rewards = problem["rewards"]
    optimum = problem["optimum"]
    values = features @ optimum
    same_delta = rewards + (GAMMA - 1.0) * values
    refresh_delta = rewards[:, None] - values[:, None] + GAMMA * values[None, :]
    expected_delta_squared = (
        RHO * np.square(same_delta)
        + (1.0 - RHO) * np.square(refresh_delta).mean(axis=1)
        + NOISE**2
    )
    return float(np.mean(np.square(features).sum(axis=1) * expected_delta_squared))


def theorem_bound(problem: dict, T: int) -> float:
    alpha = T ** (-1.0 / T)
    omega = problem["omega"]
    initial_error = float(np.square(problem["optimum"]).sum())
    sigma_squared = exact_sigma_squared(problem)
    bias = initial_error * math.e * math.exp(
        -ETA0 * omega * (1.0 - GAMMA) * alpha * T / math.log(T)
    )
    variance = (
        8.0
        * sigma_squared
        / (math.e * (omega * (1.0 - GAMMA)) ** 2)
        * math.log(T) ** 2
        / (alpha**2 * T)
    )
    return bias + variance


def scalar_independent_checker() -> dict:
    seeds = 20_000
    horizon = 100_000
    gamma = GAMMA
    eta0 = ETA0
    alpha = horizon ** (-1.0 / horizon)
    mean_reward = 0.2
    noise = 0.2
    optimum = mean_reward / (1.0 - gamma)
    mean_error = -optimum
    second_moment = optimum**2
    weights = np.zeros(seeds)
    rng = np.random.default_rng(1618033)
    for t in range(1, horizon + 1):
        eta = eta0 * alpha**t
        contraction = 1.0 - eta * (1.0 - gamma)
        mean_error *= contraction
        second_moment = contraction**2 * second_moment + eta**2 * noise**2
        sample_noise = np.where(rng.random(seeds) < 0.5, -noise, noise)
        weights += eta * (mean_reward + sample_noise - (1.0 - gamma) * weights)
    errors = np.square(weights - optimum)
    observed = float(errors.mean())
    standard_error = float(errors.std(ddof=1) / math.sqrt(seeds))
    return {
        "method": "independent closed second-moment recursion for scalar TD compared with 20,000 trajectories",
        "horizon": horizon,
        "analytic_mse": second_moment,
        "monte_carlo_mse": observed,
        "monte_carlo_standard_error": standard_error,
        "absolute_z_score": abs(observed - second_moment) / standard_error,
        "passed": abs(observed - second_moment) <= 5.0 * standard_error,
    }


def log_slope(rows: list[dict]) -> float:
    x = np.log([row["T"] for row in rows])
    y = np.log([row["mean_squared_parameter_error"] for row in rows])
    return float(np.polyfit(x, y, 1)[0])


def verify_claim1() -> dict:
    started = time.perf_counter()
    problems = []
    for scale_floor in (1.0, 0.8, 0.6):
        problem = make_problem(scale_floor)
        rows = simulate(problem)
        for row in rows:
            row["theorem_upper_bound"] = theorem_bound(problem, row["T"])
            row["bound_satisfied"] = (
                row["mean_squared_parameter_error"] + row["ci95_half_width"]
                <= row["theorem_upper_bound"]
            )
        problems.append(
            {
                "scale_floor": scale_floor,
                "omega": problem["omega"],
                "assumptions": {
                    "n_states": N_STATES,
                    "n_features": N_FEATURES,
                    "feature_rank": problem["rank"],
                    "max_feature_norm": problem["max_feature_norm"],
                    "max_abs_reward": problem["max_abs_reward"],
                    "irreducible": True,
                    "aperiodic": True,
                    "stationary_residual": problem["stationary_residual"],
                },
                "rows": rows,
                "log_log_slope": log_slope(rows),
                "all_theorem_bounds_satisfied": all(row["bound_satisfied"] for row in rows),
            }
        )
    control_problem = make_problem(1.0)
    control_rows = simulate(control_problem, constant_step=True)
    control_slope = log_slope(control_rows)
    independent = scalar_independent_checker()
    assumptions_pass = all(
        item["assumptions"]["feature_rank"] == N_FEATURES
        and item["assumptions"]["max_feature_norm"] <= 1.0 + 1e-12
        and item["assumptions"]["max_abs_reward"] <= 1.0
        for item in problems
    )
    primary_pass = all(
        item["all_theorem_bounds_satisfied"]
        and item["rows"][-1]["mean_squared_parameter_error"] < item["rows"][0]["mean_squared_parameter_error"]
        for item in problems
    )
    negative_control_pass = control_slope > -0.25
    passed = assumptions_pass and primary_pass and independent["passed"] and negative_control_pass
    return {
        "claim_id": "claim1",
        "verdict": "VERIFIED" if passed else "BLOCKED",
        "passed": passed,
        "contract": "Theorem 3.4 exact last-iterate schedule, eta0=(1-gamma)/8 and alpha=T^(-1/T), is omega-free and its explicit finite-T bound covers observed iid TD(0) error on the predeclared full-dimensional family.",
        "scope": "computational theorem reproduction over three 512-state/64-feature MDPs; not a universal formal proof",
        "schedule": {"gamma": GAMMA, "eta0": ETA0, "uses_omega": False},
        "deterministic_seeds": [260302577, 271828, 314159, 1618033],
        "problems": problems,
        "independent_checker": independent,
        "negative_control": {
            "mutation": "replace exponential schedule by constant eta_t=eta0",
            "expected": "variance floor; final log-log slope greater than -0.25",
            "rows": control_rows,
            "slope": control_slope,
            "passed_as_control": negative_control_pass,
        },
        "non_circularity": "horizons and feature spectra were predeclared; pass thresholds do not use the paper's target slope; the exact bound is evaluated after simulation, and the constant-step control uses identical data dimensions and noise.",
        "runtime_seconds": time.perf_counter() - started,
    }
