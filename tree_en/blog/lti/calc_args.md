---
title: Calculating Type Arguments
collect: true
---

Through the preceding constraint generation step, we have successfully transformed a non-constructive optimal solution search problem into a concrete, tangible outcome: a constraint set $C$. This constraint set encapsulates all boundary conditions that the undetermined type parameters $\overline{X}$ must satisfy for the entire polymorphic application to be type-correct. For each unknown variable $X_i$, we obtain a valid interval of the form $S_i \lt: X_i \lt: T_i$.

At this point, the first phase of the algorithm—"What do we know about the unknowns?"—has been successfully completed. However, our work is not yet finished. A constraint interval, such as $\mathbb{Z} \lt: X \lt: \mathbb{R}$, may itself permit multiple valid solutions (e.g., $\mathbb{Z}$ or $\mathbb{R}$). Ultimately, we must select a **concrete** type value for each $X_i$ to finalize the construction of the core language term.

This leads us to the final and crucial step of the algorithm: **By what criteria should we make the ultimate choice from each variable's valid interval?** The answer must return to our original intent—the **optimality** requirement declared in the App-InfSpec specification: Our choices must yield a **unique, minimal result type** for the entire application expression. Therefore, the algorithm's last step is to design a selection strategy that leverages the constraint set $C$ we have diligently collected, combines it with the function's original return type $R$, and computes a set of concrete type arguments that ultimately minimize $R$. This is the core task of this section: "Calculating Type Arguments."

[+](/blog/lti/polarity.md#:embed)

To minimize the return type $R$, our selection strategy becomes evident:

- If $X_i$ is **covariant** in $R$, we should choose the **minimum value** within its valid interval, i.e., its constraint's **lower bound**.
- If $X_i$ is **contravariant** in $R$, we should choose the **maximum value** within its valid interval, i.e., its constraint's **upper bound**.
- If $X_i$ is **invariant** in $R$, then to ensure result uniqueness and comparability, its valid interval must be a "single point," i.e., its constraint's **upper and lower bounds must be equal**.

The above strategy is formalized as an algorithm for computing the **minimal substitution** $\sigma_{CR}$. Given a satisfiable constraint set $C$ and return type $R$:

For each constraint $S \lt: X_i \lt: T$ in $C$:

- If $R$ is **covariant** or **constant** in $X_i$, then $\sigma_{CR}(X_i) = S$.
- If $R$ is **contravariant** in $X_i$, then $\sigma_{CR}(X_i) = T$.
- If $R$ is **invariant** in $X_i$ and $S=T$, then $\sigma_{CR}(X_i) = S$.
- In all other cases (especially when $S \neq T$ for invariant variables), $\sigma_{CR}$ is **undefined**.

When $\sigma_{CR}$ is undefined, the algorithm fails, precisely corresponding to the scenario in `App-InfSpec` where no unique optimal solution can be found.

[+-](/blog/lti/solve_code.md#:embed)

[+](/blog/lti/proof_eq.md#:embed)

This core proposition proves the equivalence between our designed concrete algorithm and the `App-InfSpec` specification. It allows us to ultimately replace that non-executable specification with a fully algorithmic rule `App-InfAlg`:

$$
\frac{
  \begin{array}{ccc}
    \Gamma \vdash f : \forall \overline{X}.\overline{T} \to R & \Gamma \vdash \overline{e} : \overline{S} & |\overline{X}| > 0 \\
    \emptyset \vdash_X \overline{S} \lt: \overline{T} \Rightarrow \overline{D} & C = \bigwedge \overline{D} & \sigma = \sigma_{CR}
  \end{array}
}{
  \Gamma \vdash f(\overline{e}) : \sigma R
}
\quad (\text{App-InfAlg})
$$
