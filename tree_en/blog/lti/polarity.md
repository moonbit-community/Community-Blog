---
title: Polarity
collect: true
---

To compute specific type parameters regarding $R$, there is another crucial operation: the change in polarity due to variable substitution.  
The polarity of a type variable $X$ in another type expression $R$ describes how the type of the entire expression changes accordingly when the type of that variable becomes larger or smaller.

- **Covariant**: If $R$ is covariant in $X$, then "becoming larger" of $X$ (becoming a supertype) causes $R$ to also "become larger". For example, in $T \to X$, $X$ is covariant. If $\mathbb{Z} \lt: \mathbb{R}$, then $T \to \mathbb{Z} \lt: T \to \mathbb{R}$.
- **Contravariant**: If $R$ is contravariant in $X$, then "becoming larger" of $X$ causes $R$ to "become smaller" (become a subtype). For example, in $X \to T$, $X$ is contravariant. If $\mathbb{Z} \lt: \mathbb{R}$, then $\mathbb{R} \to T \lt: \mathbb{Z} \to T$.
- **Invariant**: If $R$ is invariant in $X$, then $R$ remains unchanged only if $X$ remains unchanged. Any change results in incomparable outcomes. For example, in $X \to X$, $X$ is invariant.
- **Constant**: If $R$ is constant in $X$, then changes in $X$ do not affect the type of $R$. Constant types typically refer to those that do not contain variables, such as primitive types or concrete classes.

Currently, our consideration of polarity focuses primarily on function types,  
and we only need to pay attention to the position of variables in function types (whether on the left or right of the arrow),  
while also considering nested function structures. It is recommended that the reader pause here to think about the design of this algorithm.  
Of course, you can also directly expand the code block below to view the specific implementation.

[+-](/blog/lti/variance_code.md#:embed)
