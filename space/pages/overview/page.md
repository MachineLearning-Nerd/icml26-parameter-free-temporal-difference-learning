# overview


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_475aa754f0ac", "created_at": "2026-07-29T11:20:57+00:00", "title": "Towards Parameter-Free Temporal Difference Learning"}
-->
# Towards Parameter-Free Temporal Difference Learning

OpenReview: https://openreview.net/forum?id=ppIhZgFCTI
arXiv: https://arxiv.org/abs/2603.02577

Clean-room CPU reproduction (numpy). TD(0) with linear function approximation under an exponential step-size schedule η_t=η₀α^t attains the optimal last-iterate bias-variance trade-off (~σ²ln²T/T) without knowing the problem-dependent constant ω; a regularized variant (λ=1/√T) extends this to Markovian sampling parameter-free.

5 anchored claims (10 possible points), all VERIFIED via stochastic simulation on a small MDP.
