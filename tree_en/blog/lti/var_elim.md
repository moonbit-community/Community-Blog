---
title: Variable Elimination
collect: true
---

Suppose we want to generate constraints for variable $X$ such that type $\forall Y. () \to (Y\to Y)$ becomes a subtype of $\forall Y. () \to X$. According to the contravariant/covariant rules for function subtyping, this requires $Y \to Y \lt: X$. However, we cannot directly generate the constraint $\{ Y \to Y \lt: X \lt: \top\}$ because the type variable $Y$ is free in this constraint, yet it should be bound by $\forall Y$, resulting in a scope error.

The correct approach is to find a supertype of $Y \to Y$ that contains no $Y$ and is as precise as possible, then use it to constrain $X$. In this case, that supertype is $\bot \to \top$. The variable elimination mechanism formally accomplishes this task of "finding the most precise bound".

1. **Promotion**, $S \Uparrow^V T$: $T$ is a **minimal supertype** of $S$ containing no free variables from set $V$.
2. **Demotion**, $S \Downarrow^V T$: $T$ is a **maximal subtype** of $S$ containing no free variables from set $V$.

These two relations are defined by a set of recursive rules, ensuring that for any type $S$ and variable set $V$, the resulting $T$ is unique and always computable (i.e., they are total functions).  
We suggest readers pause here to consider how to design recursive rules for these relations and implement them in code (hint: for promotion, if $X \in V$ then promote it to $\top$, otherwise leave it unchanged; other cases are straightforward).

[+-](/blog/lti/ve_rules.md#:embed)

This carefully designed rule set guarantees the correctness and optimality of variable elimination, ensured by two key lemmas:

- **Soundness**: If $S \Uparrow^V T$, then $S \lt: T$ holds and $T$ contains no free variables from $V$. Dually, if $S \Downarrow^V T$, then $T \lt: S$ holds and $T$ contains no free variables from $V$.
- **Completeness**: The operation finds the "best" bound. For example, in promotion, if there exists another supertype $T'$ of $S$ containing no variables from $V$, then the $T$ computed by $S \Uparrow^V T$ must be a subtype of $T'$ (that is, $T \lt: T'$), proving $T$ is the smallest among all possible options.
