# Claim 5 method

Use the refresh-chain family

`P = rho I + (1-rho) 1 pi^T`, with uniform `pi`.

Every transition probability is positive, hence each chain is irreducible and aperiodic. For any initial distribution, `mu_t = pi + rho^t(mu_0-pi)`. The worst-case initial distribution is a point mass and its TV deviation is exactly `m rho^t`, where `m=1-1/n`.

The primary checker iterates the definition's scalar inequality. The independent checker evolves all point-mass state distributions without calling the primary checker and directly computes worst-case TV. The grid is fixed at `n={32,128,512}`, `rho={1/2,3/4,7/8,15/16}`, and five thresholds per chain. A mutated off-by-one answer must be rejected for every row.

This verifies the definition and its first-hitting interpretation on an exact, non-toy family; it does not claim that an arbitrary fitted spectral eigenvalue is automatically a valid envelope constant.

