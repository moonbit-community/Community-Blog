---
title: Proof Sketch
collect: true
---

At this point, we have fully defined a completely executable algorithm consisting of three steps: "Variable Elimination," "Constraint Generation," and "Parameter Calculation." But how do we ensure that the behavior of this concrete algorithm is entirely consistent with the non-constructive, declarative `App-InfSpec` specification?

The proof of their equivalence is distilled into a core proposition asserting:

1. **If the most general substitution $\sigma_{CR}$ exists, then it is the optimal solution required by the specification.**
2. **If the most general substitution $\sigma_{CR}$ does not exist, then the optimal solution required by the specification also necessarily does not exist.**

**Proof Sketch:**

*   **Part 1 (Correctness of the Algorithm):**
    To prove that $\sigma_{CR}$ is optimal, we take an arbitrary other valid substitution $\sigma'$ satisfying the constraints and need to prove $\sigma_{CR}(R) \lt: \sigma'(R)$.
    Consider constructing a "chain of substitutions" from $\sigma_{CR}$ to $\sigma'$, where each step changes only one variable's value. For example, $\sigma_0 = \sigma_{CR}$, $\sigma_1 = \sigma_0[X_1 \mapsto \sigma'(X_1)]$, ..., $\sigma_n = \sigma'$.
    Next, we prove that at each step along this path, the resulting type is monotonically non-decreasing, i.e., $\sigma_{i-1}(R) \lt: \sigma_i(R)$. The proof of this step relies directly on the aforementioned polarity definitions. For instance, if $R$ is covariant in $X_i$, our algorithm selected the lower bound $S$, and $\sigma'(X_i)$ must be greater than or equal to $S$. Therefore, by the definition of covariance, the resulting type must "increase." Similarly, the assertion holds in other cases.
    Ultimately, by transitivity, we conclude $\sigma_{CR}(R) \lt: \sigma'(R)$, proving the optimality of $\sigma_{CR}$.

*   **Part 2 (Completeness of Algorithm Failure):**
    When the algorithm fails, it must be because the constraint interval $[S, T]$ for some invariant variable $X_i$ has $S \neq T$.
    We use proof by contradiction: assume that an optimal solution $\sigma$ still exists under these circumstances. Since $S \neq T$, we can always find another valid substitution $\sigma'$ such that $\sigma(X_i)$ differs from $\sigma'(X_i)$. However, because $R$ is invariant in $X_i$, $\sigma(R)$ and $\sigma'(R)$ become incomparable. This contradicts the assumption that "$\sigma$ is the optimal solution (i.e., it is smaller than all other solutions)".
    Therefore, in this case, the optimal solution necessarily does not exist.
