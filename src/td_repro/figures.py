from __future__ import annotations

import base64
import html
import math


COLORS = ("#2563eb", "#059669", "#d97706", "#dc2626")


def line_svg(title: str, x_label: str, y_label: str, series: list[dict], log_x: bool = False, log_y: bool = False) -> str:
    width, height = 760, 430
    left, right, top, bottom = 90, 30, 55, 70
    plot_w, plot_h = width - left - right, height - top - bottom
    all_x = [value for item in series for value in item["x"]]
    all_y = [value for item in series for value in item["y"]]
    tx = (lambda value: math.log10(value)) if log_x else (lambda value: value)
    ty = (lambda value: math.log10(value)) if log_y else (lambda value: value)
    x_values = [tx(value) for value in all_x]
    y_values = [ty(value) for value in all_y]
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)
    x_pad = (x_max - x_min or 1.0) * 0.04
    y_pad = (y_max - y_min or 1.0) * 0.08
    x_min, x_max = x_min - x_pad, x_max + x_pad
    y_min, y_max = y_min - y_pad, y_max + y_pad

    def px(value: float) -> float:
        return left + (tx(value) - x_min) / (x_max - x_min) * plot_w

    def py(value: float) -> float:
        return top + (y_max - ty(value)) / (y_max - y_min) * plot_h

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
        f"<title>{html.escape(title)}</title>",
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="28" text-anchor="middle" font-family="sans-serif" font-size="19" font-weight="700">{html.escape(title)}</text>',
    ]
    for tick in range(6):
        fraction = tick / 5
        x = left + fraction * plot_w
        y = top + fraction * plot_h
        x_value = x_min + fraction * (x_max - x_min)
        y_value = y_max - fraction * (y_max - y_min)
        x_text = f"10^{x_value:.1f}" if log_x else f"{x_value:.3g}"
        y_text = f"10^{y_value:.1f}" if log_y else f"{y_value:.3g}"
        parts.extend([
            f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{top+plot_h}" stroke="#e5e7eb"/>',
            f'<line x1="{left}" y1="{y:.2f}" x2="{left+plot_w}" y2="{y:.2f}" stroke="#e5e7eb"/>',
            f'<text x="{x:.2f}" y="{top+plot_h+22}" text-anchor="middle" font-family="sans-serif" font-size="11">{x_text}</text>',
            f'<text x="{left-10}" y="{y+4:.2f}" text-anchor="end" font-family="sans-serif" font-size="11">{y_text}</text>',
        ])
    parts.extend([
        f'<line x1="{left}" y1="{top+plot_h}" x2="{left+plot_w}" y2="{top+plot_h}" stroke="#111827"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_h}" stroke="#111827"/>',
        f'<text x="{left+plot_w/2}" y="{height-18}" text-anchor="middle" font-family="sans-serif" font-size="13">{html.escape(x_label)}</text>',
        f'<text x="20" y="{top+plot_h/2}" text-anchor="middle" transform="rotate(-90 20 {top+plot_h/2})" font-family="sans-serif" font-size="13">{html.escape(y_label)}</text>',
    ])
    for index, item in enumerate(series):
        color = COLORS[index % len(COLORS)]
        points = " ".join(f"{px(x):.2f},{py(y):.2f}" for x, y in zip(item["x"], item["y"]))
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2.5"/>')
        for x, y in zip(item["x"], item["y"]):
            parts.append(f'<circle cx="{px(x):.2f}" cy="{py(y):.2f}" r="4" fill="{color}"/>')
        legend_x = left + 12 + (index % 2) * 280
        legend_y = top + 18 + (index // 2) * 20
        parts.extend([
            f'<line x1="{legend_x}" y1="{legend_y}" x2="{legend_x+24}" y2="{legend_y}" stroke="{color}" stroke-width="3"/>',
            f'<text x="{legend_x+31}" y="{legend_y+4}" font-family="sans-serif" font-size="12">{html.escape(item["label"])}</text>',
        ])
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def make_figures(claims: list[dict]) -> dict[str, str]:
    by_id = {claim["claim_id"]: claim for claim in claims}
    claim1 = by_id["claim1"]
    primary = [
        {"label": f"omega={item['omega']:.4g}", "x": [row["T"] for row in item["rows"]], "y": [row["mean_squared_parameter_error"] for row in item["rows"]]}
        for item in claim1["problems"]
    ]
    primary.append({"label": "constant-step control", "x": [row["T"] for row in claim1["negative_control"]["rows"]], "y": [row["mean_squared_parameter_error"] for row in claim1["negative_control"]["rows"]]})
    base = claim1["problems"][0]
    claim2 = by_id["claim2"]
    claim3 = by_id["claim3"]
    claim4 = by_id["claim4"]
    rho = [0.6, 0.9, 0.99]
    figures = {
        "headline_td_scaling.svg": line_svg("Exact exponential schedule converges; constant step stalls", "horizon T (log scale)", "last-iterate MSE (log scale)", primary, True, True),
        "bound_calibration.svg": line_svg("Observed error remains below Theorem 3.4's explicit bound", "horizon T (log scale)", "MSE / upper bound (log scale)", [{"label": "observed MSE", "x": [row["T"] for row in base["rows"]], "y": [row["mean_squared_parameter_error"] for row in base["rows"]]}, {"label": "explicit bound", "x": [row["T"] for row in base["rows"]], "y": [row["theorem_upper_bound"] for row in base["rows"]]}], True, True),
        "omega_dependency.svg": line_svg("Standard eta0 needs omega; regularized eta0 does not", "omega", "eta0 at T=1e6 (log scale)", [{"label": "Theorem 4.10 standard", "x": list(claim2["omega_values"]), "y": claim2["eta0_values_at_T_1e6"]}, {"label": "Theorem 4.12 regularized", "x": list(claim3["omega_values"]), "y": claim3["eta0_at_T_1e6_for_each_omega"]}], False, True),
        "mixing_factor.svg": line_svg("The displayed mixing factor spans 86 orders of magnitude", "tau_0.05", "log10 exp(m/log(1/rho))", [{"label": "Theorem 4.12 factor", "x": [row["tau_0.05"] for row in claim4["mixing_sweep"]], "y": [row["log10_bound_factor"] for row in claim4["mixing_sweep"]]}]),
        "feasible_horizons.svg": line_svg("Exact Markovian theorem regimes begin at extreme horizons", "rho", "first feasible log10(T)", [{"label": "standard", "x": rho, "y": [claim2["calibrated_first_feasible_horizons"][str(value)]["log10_T_first_feasible"] for value in rho]}, {"label": "regularized", "x": rho, "y": [claim3["calibrated_first_feasible_horizons"][str(value)]["log10_T_first_feasible"] for value in rho]}]),
    }
    return {name: base64.b64encode(svg.encode()).decode() for name, svg in figures.items()}
