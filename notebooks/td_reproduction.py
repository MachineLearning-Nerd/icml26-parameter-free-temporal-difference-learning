import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Parameter-free TD learning, claim by claim

    ![Exact schedule evidence](https://raw.githubusercontent.com/MachineLearning-Nerd/icml26-parameter-free-temporal-difference-learning/main/reports/claim-by-claim/images/headline_td_scaling.svg)

    The central question is whether the last TD(0) iterate can balance bias and
    noise without knowing **omega**, the smallest feature-covariance eigenvalue.
    The blue/green/orange curves use the paper's exact exponential schedule;
    the red constant-step control stalls.
    """)
    return


@app.cell
def _():
    claim_rows = [
        {"Claim": 1, "Evidence": "512 states, 64 features, 64 seeds; slopes -1.089 to -1.068", "Verdict": "VERIFIED"},
        {"Claim": 2, "Evidence": "standard eta0 scales exactly with omega", "Verdict": "VERIFIED"},
        {"Claim": 3, "Evidence": "regularized eta0 invariant across omega", "Verdict": "VERIFIED"},
        {"Claim": 4, "Evidence": "bound factor spans 86 orders; artifact is conjectural", "Verdict": "BLOCKED"},
        {"Claim": 5, "Evidence": "60/60 direct TV first-hit matches", "Verdict": "VERIFIED"},
    ]
    return (claim_rows,)


@app.cell
def _(claim_rows, mo):
    mo.vstack([
        mo.md("## What was established"),
        mo.ui.table(claim_rows, pagination=False),
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## The exact schedule

    \[
      \eta_0=(1-\gamma)/8,\qquad
      \alpha=T^{-1/T},\qquad
      \eta_t=\eta_0\alpha^t.
    \]

    Omega appears in the **bound**, but not in this i.i.d. schedule. The earlier
    historical verifier used the reciprocal `1/[8(1-gamma)]`; the current run
    corrects that source mismatch.

    ![Omega dependency](https://raw.githubusercontent.com/MachineLearning-Nerd/icml26-parameter-free-temporal-difference-learning/main/reports/claim-by-claim/images/omega_dependency.svg)
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Why Claim 4 is blocked

    ![Mixing factor](https://raw.githubusercontent.com/MachineLearning-Nerd/icml26-parameter-free-temporal-difference-learning/main/reports/claim-by-claim/images/mixing_factor.svg)

    The exponential factor is genuinely present in Theorem 4.12's bound. The
    paper then **conjectures** that it is a proof artifact. Finite experiments
    cannot turn that conjecture into a theorem, so the faithful verdict is
    BLOCKED.

    Formal evidence is already embedded here; rerunning the expensive experiment
    is optional. See the [illustrated report](https://github.com/MachineLearning-Nerd/icml26-parameter-free-temporal-difference-learning/blob/main/reports/claim-by-claim/report.md).
    """)
    return


if __name__ == "__main__":
    app.run()
