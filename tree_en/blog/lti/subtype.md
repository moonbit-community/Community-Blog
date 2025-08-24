---
title: Subtyping Relation
collect: true
---

The subtyping relation, denoted as $S \lt: T$ (read as "$S$ is a subtype of $T$"), is the core of this formal system. It defines a "substitutability" between types: wherever a term of type $T$ is required, it is safe to substitute a term of type $S$.

Unlike definitions in many theoretical works, this article deliberately adopts an **algorithmic** approach to present the subtyping relation. This means the definition includes only a minimal core set of rules directly usable for implementation of the decision procedure, while properties like transitivity—typically treated as axioms—become provable lemmas in this system. This style brings the definition closer to a specification for a type-checking algorithm:

$$
\begin{array}{ll}
X \lt: X & \text{(S-Refl)} \\[1em]
T \lt: \top & \text{(S-Top)} \\[1em]
\bot \lt: T & \text{(S-Bot)} \\[1em]
\dfrac{
    \overline{T} \lt: \overline{R} \quad S \le: U
}{
    \forall \overline{X}. \overline{R} \rightarrow S \lt: \forall \overline{X}. \overline{T} \rightarrow U
}
& \text{(S-Fun)}
\end{array}
$$

where $\overline{T} \lt: \overline{R}$ holds if and only if $\text{len}(T) = \text{len}(S) \land \forall 1 \leq i \leq \text{len}(S). S_i \lt: T_i$.  
The S-Fun rule captures the key characteristics of function subtyping: **contravariant** in argument types (reversed subtyping direction) and **covariant** in return type (preserved subtyping direction). Readers may attempt to translate this formalism into a MoonBit predicate function or refer to the folded code snippet below.

[+-](/blog/lti/subtype_code.md#:embed)

To support subsequent constraint-solving algorithms, the system must compute the least upper bound (join, denoted $\lor$) and greatest lower bound (meet, denoted $\land$) for any two types. Thanks to $\bot$ and $\top$, these operations are total functions in this system—bounds exist for every type pair. We define them as follows:

- **Least Upper Bound $S \vee T$**
  - If $S \lt: T$, the result is $T$.
  - If $T \lt: S$, the result is $S$.
  - If $S$ and $T$ are $\forall\overline{X}.\overline{V} \to P$ and $\forall\overline{X}.\overline{W} \to Q$ respectively, the result is $\forall\overline{X}.(\overline{V} \wedge \overline{W}) \to (P \vee Q)$.
  - In all other cases, the result is $\top$.

- **Greatest Lower Bound $S \wedge T$**
  - If $S \lt: T$, the result is $S$.
  - If $T \lt: S$, the result is $T$.
  - If $S$ and $T$ are $\forall\overline{X}.\overline{V} \to P$ and $\forall\overline{X}.\overline{W} \to Q$ respectively, the result is $\forall\overline{X}.(\overline{V} \vee \overline{W}) \to (P \wedge Q)$.
  - In all other cases, the result is $\bot$.

Simple structural induction proves these operations satisfy:
- $S \vee T$ and $S \wedge T$ are the least upper bound and greatest lower bound of $S$ and $T$ respectively.
- If $S \lt: U$ and $T \lt: U$, then $S \vee T \lt: U$.
- If $U \lt: S$ and $U \lt: T$, then $U \lt: S \wedge T$.

Readers are encouraged to implement this in code; solutions can be viewed by expanding the snippet below.

[+-](/blog/lti/subtype_code2.md#:embed)
