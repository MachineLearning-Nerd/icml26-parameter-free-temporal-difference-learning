# claims


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_e8119a24403a", "created_at": "2026-07-29T11:20:58+00:00", "title": "Claims to reproduce"}
-->
## Claims to reproduce

1. **Theorem 3.4 (i.i.d.):** under i.i.d. sampling with the exponential step-size schedule η_t=η₀α^t (η₀=1/(8(1−γ)), α=T^{−1/T}), TD(0) attains the optimal last-iterate bias-variance trade-off (~σ²ln²T/T) without knowing ω.
2. **Section 4 (Markovian):** standard TD(0) with the same schedule achieves a comparable convergence rate under Markovian sampling (the analysis requires ω for η₀).
3. **Section 4.2 (regularized):** a regularized TD(0) variant (λ=1/√T) with exponential step-sizes removes the dependence on ω in the Markovian setting.
4. **Section 4 (mixing-time artifact):** the regularized Markovian analysis introduces exponential dependence on the mixing time τ_mix as a proof artifact (Theorem 4.12).
5. **Definition 4.1 (mixing time):** τ_δ=min{t∈ℕ₀ : mρ^t ≤ δ}, with the chain satisfying sup dTV(P^t μ₀, μ_π) ≤ mρ^t.
