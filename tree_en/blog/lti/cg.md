---
title: Constraint Generation
collect: true
---

Rather than treating type parameter inference as a search problem of "finding and verifying the optimal solution" among infinite possibilities,  
we reframe it as a problem of "solving for unknown boundaries" similar to solving algebraic equations.  
Instead of guessing what the type parameters $\overline{X}$ might be,  
we derive the conditions $\overline{X}$ must satisfy by analyzing the subtyping relation itself.

Observing that our rules contain subtyping constraints, consider the general case $S \lt: T$,  
which inherently implies constraints on its components (including unknown variables).  
If $X$ is an unknown variable in $T$, the structure of $S$ necessarily restricts the possible forms of $X$.  
Our algorithm transforms this implicit structural restriction into a set of explicit assertions about $X$'s bounds.

However, before systematically extracting these constraints, we must first address a preliminary yet critical challenge related to variable scoping.  
If not handled properly, the constraints we generate may themselves be ill-formed.  
This challenge motivates the algorithm's first concrete step: **variable elimination**.

[+](/blog/lti/var_elim.md#:embed)

Constraint generation is the core engine of the local type parameter synthesis algorithm.  
After ensuring scoping safety through variable elimination,  
this step's mission is to transform a subtyping judgment—for example,  
$S \lt: T$ where $S$ or $T$ contains undetermined type parameters $\overline{X}$—into a set of explicit constraints on these unknowns $\overline{X}$.  
We now formally define the structure of constraints in code:

- **Constraint**: In this system, each constraint takes the form $S_i \lt: X_i \lt: T_i$, specifying both a **lower bound** $S_i$ and an **upper bound** $T_i$ for a single unknown type variable $X_i$.

- **Constraint Set**: A constraint set $C$ is a finite mapping (implementable as a Hash Map in code) from a group of unknown variables $\overline{X}$ to their corresponding constraints. A key invariant is that the bounds ($S_i$, $T_i$) in any constraint must not contain any pending unknown variables (i.e., variables in $\overline{X}$) or any local variables to be eliminated (i.e., variables in $V$). The **empty constraint set ($\emptyset$)** represents the least restrictive constraint, equivalent to $\bot \lt: X_i \lt: \top$ for each $X_i$.  
- **Constraint set intersection ($\wedge$)** is defined as the intersection of two constraint sets $C$ and $D$, obtained by merging constraints for the same variable. The new lower bound is the **least upper bound (join, $\vee$)** of the original lower bounds, while the new upper bound is the **greatest lower bound (meet, $\wedge$)** of the original upper bounds.

[+-](/blog/lti/cg_def_code.md#:embed)

The **constraint generation** process is formalized as a derivation relation $V \vdash_{\overline{X}} S \lt: T \Rightarrow C$, meaning: given a set of variables $V$ to avoid, the (weakest) constraint set $C$ on unknown variables $\overline{X}$ required for $S \lt: T$ to hold, where $C$ is the output of this relation.

The algorithm is defined by recursive rules, with key rules as follows (note: we always assume $\overline{X} \cap V = \emptyset$):

- **Trivial Cases**: When the upper bound of the subtyping relation is $\top$ or the lower bound is $\bot$, the relation holds unconditionally, thus generating an empty constraint set $\emptyset$.  
- **Upper Bound Constraint**: When judging $Y \lt: S$ (where $Y \in \overline{X}$ is an unknown variable and $S$ is a known type), the algorithm generates an upper bound constraint for $Y$.  
  $$
  \frac{Y \in \overline{X} \quad S \Downarrow^V T \quad \text{FV}(S) \cap \overline{X} = \emptyset}{V \vdash_{\overline{X}} Y \lt: S \Rightarrow \{ \bot \lt: Y \lt: T \}} \quad (\text{CG-Upper})
  $$  
  Note that the **variable elimination** operation ($S \Downarrow^V T$) ensures the upper bound $T$ is well-formed.  
- **Lower Bound Constraint**: Dually, when judging $S \lt: Y$, the algorithm generates a lower bound constraint for $Y$.  
  $$
  \frac{Y \in \overline{X} \quad S \Uparrow^V T \quad \text{FV}(S) \cap \overline{X} = \emptyset}{V \vdash_{\overline{X}} S \lt: Y \Rightarrow \{ T \lt: Y \lt: \top \}} \quad (\text{CG-Lower})
  $$  
- **Function Type**: When comparing function types, the algorithm recursively processes parameter and return types, then merges the resulting sub-constraint sets.  
  $$
  \frac{V \cup \{\overline{Y}\} \vdash_{\overline{X}} \overline{T} \lt: \overline{R} \Rightarrow \overline{C} \quad V \cup \{\overline{Y}\} \vdash_{\overline{X}} S \lt: U \Rightarrow D}{V \vdash_{\overline{X}} \forall \overline{Y}.\overline{R} \to S \lt: \forall \overline{Y}.\overline{T} \to U \Rightarrow (\bigwedge \overline{C}) \wedge D} \quad (\text{CG-Fun})
  $$  
  Here, constraints are accumulated through **intersection ($\wedge$)** of sub-constraint sets.

[+-](/blog/lti/cg_code.md#:embed)

A crucial observation is that in any invocation $V \vdash_{\overline{X}} S \lt: T \Rightarrow C$, the unknown variables $\overline{X}$ appear only on one side of $S$ or $T$. This makes the entire process a **matching-modulo-subtyping** problem rather than a full unification problem, ensuring the algorithm's simplicity and determinism.

<!-- The correctness of this generation algorithm is guaranteed by two complementary theorems:

- **Soundness**: The algorithm is correct. If it generates constraint set $C$ for $S\lt:T$, then any type substitution $\sigma$ satisfying $C$ (denoted $\sigma \in C$) necessarily makes $\sigma S \lt: \sigma T$ hold.  
- **Completeness**: The algorithm is "sufficiently good". Conversely, if there exists a substitution $\sigma$ such that $\sigma S \lt: \sigma T$ holds, then the algorithm must successfully generate a constraint set $C$, and $\sigma$ must satisfy $C$ (i.e., $\sigma \in C$).  

Together, these properties show that the constraint generator precisely characterizes all possible solutions—no more, no less. -->
