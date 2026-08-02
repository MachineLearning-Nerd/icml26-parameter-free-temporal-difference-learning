# Claim 1 source audit

Theorem 3.4 (`thm:exp_iid`, ar5iv `S3.Thmtheorem4`) assumes a finite
irreducible aperiodic chain and full-column-rank features with row norms at most
one. It samples transitions independently from stationarity. The exact schedule
is `eta0=(1-gamma)/8`, `alpha=T^(-1/T)`, `eta_t=eta0 alpha^t`; eta0 does not use
omega. The displayed last-iterate parameter-MSE bound contains an exponentially
decaying bias term and a `sigma^2 ln^2(T)/(omega^2 T)` variance term.

This corrects the historical rejected verifier, which used
`eta0=1/[8(1-gamma)]`.
