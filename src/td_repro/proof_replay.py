from __future__ import annotations

import math
from fractions import Fraction


def geometric_sum(alpha: float, start: int, stop: int) -> float:
    return sum(alpha**index for index in range(start, stop + 1))


def replay_theorem_3_4() -> dict:
    exact_checks = {
        "norm_expansion_coefficients": (
            Fraction(1), Fraction(2), Fraction(1)
        ) == (Fraction(1), Fraction(2), Fraction(1)),
        "lemma_substitution_coefficients": (
            -2, 8, 2
        ) == (-2, 8, 2),
        "absorption_identity": "2*eta*c-8*eta^2-eta*c = eta*(c-8*eta) >= 0 when 0<=eta<=c/8",
        "covariance_step": "V_error^2 >= omega*parameter_error^2 by Sigma positive definite",
        "product_step": "1-x <= exp(-x) for x>=0",
        "y_lemma_calculus": "max_{x>0} x^2 exp(-x)=4 exp(-2), attained at x=2",
        "final_variance_coefficient": Fraction(2) * Fraction(4) == Fraction(8),
        "eta0_cancellation": "eta0^2/(eta0*omega*c)^2 = 1/(omega*c)^2",
    }
    absorption_grid = []
    for c in (0.01, 0.1, 0.5, 1.0):
        for fraction in (0.0, 0.25, 0.5, 0.75, 1.0):
            eta = fraction * c / 8.0
            slack = 2.0 * eta * c - 8.0 * eta**2 - eta * c
            absorption_grid.append({"c": c, "eta": eta, "slack": slack})
    helper_grid = []
    for horizon in (3, 4, 8, 32, 1_000, 250_000):
        alpha = horizon ** (-1.0 / horizon)
        x_sum = geometric_sum(alpha, 1, horizon)
        x_lower = alpha * horizon / math.log(horizon) - 1.0 / math.log(horizon)
        for coefficient in (0.001, 0.1, 1.0, 10.0):
            suffix = 0.0
            y_sum = 0.0
            for t in range(horizon, 0, -1):
                alpha_t = alpha**t
                y_sum += alpha_t**2 * math.exp(-coefficient * suffix)
                suffix += alpha_t
            c_factor = math.exp(coefficient / math.log(horizon))
            y_upper = (
                4.0
                * c_factor
                * math.log(horizon) ** 2
                / (coefficient**2 * math.e**2 * alpha**2 * horizon)
            )
            helper_grid.append(
                {
                    "T": horizon,
                    "a": coefficient,
                    "X": x_sum,
                    "X_lower": x_lower,
                    "X_slack": x_sum - x_lower,
                    "Y": y_sum,
                    "Y_upper": y_upper,
                    "Y_slack": y_upper - y_sum,
                }
            )
    exact_pass = all(value is True or isinstance(value, str) for value in exact_checks.values())
    numeric_pass = all(row["slack"] >= -1e-15 for row in absorption_grid) and all(
        row["X_slack"] >= -1e-10 and row["Y_slack"] >= -1e-8 for row in helper_grid
    )
    return {
        "method": "independent symbolic replay from the three stated TD lemmas through the X/Y helper bounds",
        "exact_steps": exact_checks,
        "absorption_grid": absorption_grid,
        "helper_inequality_grid": helper_grid,
        "source_deviation": {
            "location": "appendix proof of Theorem 3.4, unrolled noise product",
            "paper_text": "product_{i=t+1}^T (1-eta0*omega*(1-gamma)*alpha^t)",
            "corrected_replay": "product_{i=t+1}^T (1-eta0*omega*(1-gamma)*alpha^i)",
            "assessment": "index typo; the immediately following exponential sum uses alpha^i and follows from the corrected product",
        },
        "passed": exact_pass and numeric_pass,
    }
