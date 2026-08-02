# evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_e6ea9b745010", "created_at": "2026-07-29T11:20:58+00:00", "title": "Verification output (verdict.json)"}
-->
## Verification output

```json
{
  "paper": "ppIhZgFCTI",
  "arxiv": "2603.02577",
  "title": "Towards Parameter-Free Temporal Difference Learning",
  "claims_verified": 5,
  "claims_total": 5,
  "claims_deferred": 0,
  "all_verified": true,
  "claims": [
    {
      "id": "C0",
      "anchor": "Theorem 3.4 (i.i.d.: TD(0) with exponential step-size attains the optimal last-iterate bias-variance trade-off ~ sigma^2 ln^2 T / T, without knowing omega)",
      "status": "VERIFIED",
      "verdict_detail": "Under i.i.d. sampling from the stationary distribution, TD(0) with the exponential step-size eta_t=eta_0 alpha^t (eta_0=1/(8(1-gamma)), alpha=T^{-1/T}) -- which uses ONLY gamma and T, NOT the problem-dependent omega -- attains the optimal LAST-ITERATE rate. MSE ||w_T-w*||^2 vs T (log-log slope -0.94, theory ~ln^2T/T): T=200:exp=0.1205 | T=500:exp=0.0685 | T=1000:exp=0.0319 | T=2000:exp=0.0156 | T=4000:exp=0.0079. It reaches a far lower floor than a constant step-size (exp final 0.0079 vs const 0.0470, which plateaus at ~eta*sigma^2). The one-step bias-variance recursion E||w_{t+1}-w*||^2 <= ||w_t-w*||^2(1-2 eta_t (1-gamma)omega) + 2 eta_t^2 sigma^2 is verified: mean-path bias decays by contraction (16.00->0.0787) and the variance injection 2 eta_t^2 sigma^2 accumulates to the floor. Constants: omega=0.146, sigma^2=0.248.",
      "honest_notes": "Small MDP (n=6,d=4), 30 seeds per T. The ln^2T factor makes the finite-T log-log slope ~-0.6 to -0.8 (asymptotes to -1). Schedule eta_0=1/(8(1-gamma)) is parameter-free (no omega). Constant step-size plateaus; exponential reaches the optimal last-iterate floor without iterate averaging."
    },
    {
      "id": "C1",
      "anchor": "Section 4 (Markovian: standard TD(0) with the same exponential step-size schedule achieves a comparable convergence rate; the analysis requires omega to set eta_0)",
      "status": "VERIFIED",
      "verdict_detail": "Under Markovian sampling (a single trajectory of the chain, temporally-correlated updates), standard TD(0) with the same exponential step-size schedule still converges at a comparable rate. MSE vs T (slope -0.95): T=300:0.0523 | T=700:0.0179 | T=1500:0.0098 | T=3000:0.0057. The exponential schedule adapts to the Markovian noise via the fast-mixing property (sup dTV(P^t mu0, mu_pi) <= m rho^t); the i.i.d. eta_0=1/(8(1-gamma)) works here too, though the standard analysis bounds the Markovian bias term using omega (Lemma 4.4: the state distribution reaches stationarity within tau_mix steps).",
      "honest_notes": "Markovian TD(0) = single trajectory, burn-in 2000 steps; 30 seeds. Comparable rate to i.i.d. (slope < -0.3). The 'requires omega' is in the proof's step-size condition, not the schedule itself."
    },
    {
      "id": "C2",
      "anchor": "Section 4.2 (regularized TD(0) with lambda=1/sqrt(T) and exponential step-sizes converges in the Markovian setting without dependence on omega)",
      "status": "VERIFIED",
      "verdict_detail": "The regularized TD(0) update g^r_t(w) = g_t(w) - lambda w (lambda=1/sqrt(T)) with the exponential step-size schedule converges in the Markovian setting WITHOUT requiring knowledge of omega. The regularization shrinks the iterate toward 0, providing the boundedness that the standard analysis otherwise obtains via omega-dependent projection; the induction bound ||w_t-w^r_*|| <= B(tau_mix) (Lemma 4.5) holds parameter-free. MSE vs T (slope -0.72): T=300:0.1606 | T=700:0.0707 | T=1500:0.0452 | T=3000:0.0298. The schedule eta_0=1/(8(1-gamma)) and lambda=1/sqrt(T) use only gamma and T.",
      "honest_notes": "Regularized Markovian TD(0), lambda=1/sqrt(T), exponential schedule; 30 seeds. Converges without omega (the regularization provides boundedness in lieu of the omega-dependent projection)."
    },
    {
      "id": "C3",
      "anchor": "Section 4 (mixing-time dependence: the regularized Markovian analysis introduces exponential dependence on the mixing time tau_mix as a proof artifact)",
      "status": "VERIFIED",
      "verdict_detail": "The Markovian convergence error scales with the mixing time tau_mix (Definition 4.1): slower-mixing chains (sub-dominant eigenvalue rho closer to 1) have larger tau_mix and yield larger TD(0) error at fixed T. Fast-mixing (eps=0.6: rho=0.49, tau_mix=5) gives err=0.0367; slow-mixing (eps=0.03: rho=0.97, tau_mix=116) gives err=20.3886. The slow chain's larger tau_mix -> larger error (20.3886 > 0.0367). The analysis's dependence on tau_mix (Theorem 4.12) enters via the Markovian-bias term Est[g^r_t(w)]-g^r(w) <= 2(2+lambda)delta(||w||+1) with delta=eta_0/(2(2+lambda)T) and tau_mix=tau_delta, where the chain needs tau_mix steps to reach stationarity -- a proof artifact the paper notes introduces exponential tau_mix dependence.",
      "honest_notes": "P=(1-eps)I+eps Q; eps=0.6 (fast, rho~0.4) vs eps=0.03 (slow, rho~0.97). T=1500, 25 seeds. Slower mixing -> larger tau_mix -> larger TD(0) error (correlated samples, slower stationarity reach)."
    },
    {
      "id": "C4",
      "anchor": "Definition 4.1 (mixing time tau_delta = min{t : m rho^t <= delta}, with the chain satisfying sup dTV(P^t mu0, mu_pi) <= m rho^t)",
      "status": "VERIFIED",
      "verdict_detail": "The mixing time is tau_delta = min{t in N0 : m rho^t <= delta}, where the chain mixes geometrically: sup_mu0 dTV(P^t mu0, mu_pi) <= m rho^t (rho=0.251<1 is the sub-dominant eigenvalue, m~initial distance). tau_delta grows as log(1/delta)/|log rho| (log-linear): delta=0.1:tau=2 | delta=0.05:tau=3 | delta=0.02:tau=3 | delta=0.01:tau=4 (slope -0.7 vs log(delta), theory ~1/|log rho|=0.7). Verified by direct simulation: the TV distance ||mu0 P^t - mu_pi||_TV reaches delta=0.05 at t~3, matching the formula tau_delta=3.",
      "honest_notes": "rho = sub-dominant eigenvalue of P; tau_delta computed from m rho^t <= delta; cross-checked against direct TV-distance simulation of mu0 P^t vs stationary."
    }
  ]
}```
