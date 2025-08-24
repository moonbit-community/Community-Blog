---
title: Promotion and Demotion Rules
collect: true
---

- **Promotion Rules ($S \Uparrow^V T$)**

  - For $\top$ and $\bot$:
    $$
    \top \Uparrow^V \top \quad (\text{VU-Top})
    $$
    $$
    \bot \Uparrow^V \bot \quad (\text{VU-Bot})
    $$
  - For type variable $X$:
    - If $X$ belongs to the set $V$ that needs to be eliminated, **promote** it to $\top$.
      $$
      \frac{X \in V}{X \Uparrow^V \top} \quad (\text{VU-Var-1})
      $$
    - If $X$ is not in $V$, it remains unchanged.
      $$
      \frac{X \notin V}{X \Uparrow^V X} \quad (\text{VU-Var-2})
      $$
  - For function types:
    - Recursively **demote** its parameter types (contravariant position) and **promote** its return type (covariant position).
      $$
      \frac{\overline{S} \Downarrow^V \overline{U} \quad T \Uparrow^V R \quad \overline{X} \notin V}{\forall\overline{X}.\overline{S} \to T \Uparrow^V \forall\overline{X}.\overline{U} \to R} \quad (\text{VU-Fun})
      $$

- **Demotion Rules ($S \Downarrow^V T$)**
  - Handling of $\top$ and $\bot$ is consistent with promotion rules.
  - For type variable $X$:
    - If $X$ belongs to $V$, **demote** it to $\bot$.
      $$
      \frac{X \in V}{X \Downarrow^V \bot} \quad (\text{VD-Var-1})
      $$
    - If $X$ is not in $V$, it remains unchanged.
  - For function types:
    - Recursively **promote** its parameter types and **demote** its return type.
      $$
      \frac{\overline{S} \Uparrow^V \overline{U} \quad T \Downarrow^V R \quad \overline{X} \notin V}{\forall\overline{X}.\overline{S} \to T \Downarrow^V \forall\overline{X}.\overline{U} \to R} \quad (\text{VD-Fun})
      $$

This can be implemented very straightforwardly in MoonBit:

![promotion_demotion](moonbit/src//lti/syntax.mbt#:include)
