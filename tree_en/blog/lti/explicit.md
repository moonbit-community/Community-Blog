---
title: Explicit Typing Rules
collect: true
---

After defining the type and subtype relations, we can now present the typing rules for the kernel language. These rules define the typing judgment $\Gamma \vdash e : T$, meaning "in context $\Gamma$, term $e$ has type $T$."

Consistent with the definition of the subtype relation, these typing rules adopt an algorithmic presentation style and omit the subsumption rule commonly found in traditional type systems (where if $e$ has type $S$ and $S \lt: T$, then $e$ can also have type $T$).

By omitting this rule, the system computes a **unique, minimal type** for every typable term, which the author calls its **manifest type**. This design choice does not alter the set of typable terms in the language but ensures that every term has exactly one type derivation path. This significantly enhances the system's predictability.

### Core Rules

- **Variable**

  $$
  \frac{}{\Gamma \vdash x : \Gamma(x)} \quad (\text{Var})
  $$

- **Abstraction**  
  This rule unifies traditional term abstraction and type abstraction.

  $$
  \frac{\Gamma, \overline{X}, \overline{x}:\overline{S} \vdash e : T}{\Gamma \vdash \mathbf{fun}[\overline{X}] (\overline{x}:\overline{S}) e : \forall \overline{X}.\overline{S} \to T} \quad (\text{Abs})
  $$

  To derive the type of $\mathbf{fun}[\overline{X}] (\overline{x}:\overline{S})$, we add bindings for type variables $\overline{X}$ and value variables $\overline{x}:\overline{S}$ to context $\Gamma$. We then derive type $T$ for the function body $e$ in this extended context. The entire function's type is $\forall \overline{X}.\overline{S} \to T$.

- **Application**  
  This rule unifies traditional term application and polymorphic application. It first derives the type of function `f`, then verifies that all actual arguments (type and term arguments) conform to the function's signature.  
  The requirement is relaxed: actual argument types need only satisfy the subtype relation with parameter types, not exact matches.

  $$
  \frac{\Gamma \vdash f : \forall \overline{X} . \overline{S} \to R \quad \Gamma \vdash \overline{e} \lt: [\overline{T}/\overline{X}]\overline{S}}{\Gamma \vdash f[\overline{T}] (\overline{e}) : [\overline{T}/\overline{X}]R} \quad (\text{App})
  $$

  Here, the notation $\Gamma \vdash \overline{e} \lt: [\overline{T}/\overline{X}]\overline{S}$ abbreviates $\Gamma \vdash \overline{e} \lt: \overline{U}$ followed by verifying $\overline{U} \lt: [\overline{T}/\overline{X}]\overline{S}$. The result type is obtained by substituting actual type arguments $\overline{T}$ into the function's original return type $R$.

  [+](/blog/lti/subst_code.md#:embed)

- **Bot Application**  
  Introducing the $\bot$ type necessitates this special application rule to maintain type soundness.  
  Since $\bot$ is a subtype of any function type, a $\bot$-typed expression should be applicable to any valid arguments without type errors.

  $$
  \frac{\Gamma \vdash f : \bot \quad \Gamma \vdash \overline{e} : \overline{S}}{\Gamma \vdash f[\overline{T}] (\overline{e}) : \bot} \quad (\text{App-Bot})
  $$

  This rule states that when a $\bot$-typed term is applied, the entire expression has type $\bot$ regardless of arguments—the most precise (minimal) result type possible.

These rules collectively ensure a key property: **Uniqueness of Manifest Types**. If $\Gamma \vdash e : S$ and $\Gamma \vdash e : T$, then $S=T$.
