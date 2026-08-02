# Claim 1 method

The primary route runs exact last-iterate TD(0) with the paper's horizon-specific
exponential schedule on three 512-state, 64-feature, full-rank refresh-chain
problems. Each feature row has norm at most one and every reward is bounded by
0.4. Sixty-four deterministic trajectories are run independently at four
predeclared horizons. The observed mean plus its 95% interval must lie below the
paper's explicit finite-T bound.

An independent scalar second-moment recursion is compared with 20,000 direct
trajectories. A constant-step mutation is the negative control. A separate
algebraic replay reconstructs the norm expansion, lemma substitutions,
step-size absorption, product unrolling, and X/Y helper bounds.
