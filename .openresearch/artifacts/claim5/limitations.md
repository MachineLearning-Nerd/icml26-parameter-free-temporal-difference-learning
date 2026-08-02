# Limitations and deviations

- Definition 4.1 is a definition, not an empirical convergence theorem. The check validates its exact first-hitting interpretation on an analytically controlled family rather than pretending finite simulation proves a universal theorem.
- The refresh-chain family is deliberately structured so that the geometric envelope is exact. This avoids the rejected baseline's unjustified substitution of a fitted subdominant eigenvalue for a proven envelope constant.
- Floating-point direct TV evolution uses a `1e-12` comparison tolerance. The selected probabilities are dyadic, and the checker separately reports its deviation from the closed form.

