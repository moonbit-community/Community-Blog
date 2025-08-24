---
title: Typing Rules
collect: true
---

This section is the final piece of our type checker, describing the entire bidirectional type checking process.

### Variable Rules

**1. Synthesis - Variable (Synthesis-Var)**

$$
\frac{}{\Gamma \vdash x \Rightarrow \Gamma(x)} \quad (\text{S-Var})
$$

This is the **synthesis** rule for variables. To synthesize the type of a variable $x$, simply look up its declared type $\Gamma(x)$ in the current typing context $\Gamma$. This is the most straightforward form of type derivation: a variable's type is its declared type.

---

**2. Checking - Variable (Checking-Var)**

$$
\frac{\Gamma \vdash \Gamma(x) \lt: T}{\Gamma \vdash x \Leftarrow T} \quad (\text{C-Var})
$$

This is the **checking** rule for variables. To verify that variable $x$ conforms to expected type $T$, we first retrieve its actual type $\Gamma(x)$ from context $\Gamma$, then validate that this actual type $\Gamma(x)$ is a subtype of $T$. The subtype relation is denoted by $\Gamma \vdash \Gamma(x) \lt: T$.

---

### Function Abstraction Rules

**3. Synthesis - Abstraction (Synthesis-Abs)**

$$
\frac{\Gamma, \overline{X}, \overline{x}:\overline{S} \vdash e \Rightarrow T}{\Gamma \vdash \textbf{fun} [\overline{X}] (\overline{x}:\overline{S}) e \Rightarrow \forall \overline{X}. \overline{S} \rightarrow T} \quad (\text{S-Abs})
$$

This is the **synthesis** rule for **fully annotated function abstractions**.

- For a function of the form `fun [X] (x:S) e` where type parameters $\overline{X}$ and value parameter types $\overline{S}$ are explicitly annotated.
- The premise requires that after adding type variables $\overline{X}$ and value variables with types $\overline{x}:\overline{S}$ to context $\Gamma$, we can **synthesize** type $T$ for the body $e$.
- The entire function expression can then be synthesized as polymorphic function type $\forall \overline{X}. \overline{S} \rightarrow T$.

---

**4. Checking - Unannotated Abstraction (Checking-Abs-Inf)**

$$
\frac{\Gamma, \overline{X}, \overline{x}:\overline{S} \vdash e \Leftarrow T}{\Gamma \vdash \textbf{fun} [\overline{X}] (\overline{x}) e \Leftarrow \forall \overline{X}. \overline{S} \rightarrow T} \quad (\text{C-Abs-Inf})
$$

This core rule infers parameter types for **unannotated anonymous functions**.

- When **checking** an unannotated function `fun [X] (x) e` against expected type $\forall \overline{X}. \overline{S} \rightarrow T$, we extract parameter types $\overline{S}$ and return type $T$ from the expected type.
- We then add type variables $\overline{X}$ and inferred parameter types $\overline{x}:\overline{S}$ to the context, and **check** that body $e$ conforms to return type $T$ in this extended context.
- Note: $\overline{X}$ cannot be omitted in this system.

---

**5. Checking - Annotated Abstraction (Checking-Abs)**

$$
\frac{\Gamma, \overline{X} \vdash \overline{T} \lt: \overline{S} \quad \Gamma, \overline{X}, \overline{x}:\overline{S} \vdash e \Leftarrow R}{\Gamma \vdash \textbf{fun} [\overline{X}] (\overline{x}:\overline{S}) e \Leftarrow \forall \overline{X}. \overline{T} \rightarrow R} \quad (\text{C-Abs})
$$

This rule handles **annotated functions** in **checking** mode.

- When checking an annotated function `fun [X] (x:S) e` against expected type $\forall \overline{X}. \overline{T} \rightarrow R$:
- First, due to contravariance of function parameters, verify that expected parameter types $\overline{T}$ are subtypes of the function's actual parameter types $\overline{S}$.
- Then check that body $e$ conforms to expected return type $R$ in the extended context.

---

### Function Application Rules

**6. Synthesis - Application (Synthesis-App)**

$$
\frac{\Gamma \vdash f \Rightarrow \forall \overline{X}. \overline{S} \rightarrow R \quad \Gamma \vdash \overline{e} \Leftarrow [\overline{T}/\overline{X}]\overline{S}}{\Gamma \vdash f [\overline{T}] (\overline{e}) \Rightarrow [\overline{T}/\overline{X}]R} \quad (\text{S-App})
$$

This is the **synthesis** rule for function application.

- First, **synthesize** the type of $f$ as polymorphic function $\forall \overline{X}. \overline{S} \rightarrow R$.
- Substitute type variables $\overline{X}$ with provided type arguments $\overline{T}$ to obtain expected parameter types $[\overline{T}/\overline{X}]\overline{S}$.
- **Check** that actual arguments $\overline{e}$ conform to these expected types.
- The application's type is then **synthesized** as $[\overline{T}/\overline{X}]R$.

---

**7. Checking - Application (Checking-App)**

$$
\frac{\Gamma \vdash f \Rightarrow \forall \overline{X}. \overline{S} \rightarrow R \quad \Gamma \vdash [\overline{T}/\overline{X}]R \lt: U \quad \Gamma \vdash \overline{e} \Leftarrow [\overline{T}/\overline{X}]\overline{S}}{\Gamma \vdash f [\overline{T}] (\overline{e}) \Leftarrow U} \quad (\text{C-App})
$$

This **checking** rule for function application adds a final subtype check.

- First two steps mirror `S-App`: synthesize $f$'s type and check arguments $\overline{e}$.
- After computing the application's return type $[\overline{T}/\overline{X}]R$, verify it is a subtype of the expected type $U$.

---

### Rules Combining Bidirectional Checking and Type Argument Synthesis

**8. Synthesis - Application - Infer Specification (Synthesis-App-InfAlg)**

$$
\frac{
  \begin{array}{ccc}
    \Gamma \vdash f : \forall \overline{X}.\overline{T} \to R & \Gamma \vdash \overline{e} : \overline{S} & |\overline{X}| > 0 \\
    \emptyset \vdash_X \overline{S} \lt: \overline{T} \Rightarrow \overline{D} & C = \bigwedge \overline{D} & \sigma = \sigma_{CR}
  \end{array}
}{
  \Gamma \vdash f(\overline{e}) \Rightarrow \sigma R
}
\quad (\text{S-App-InfAlg})
$$

This **synthesis** rule infers **missing type arguments** in function applications, derived from the "Type Argument Calculation" section.

---

**9. Checking - Application - Infer Specification (Checking-App-InfAlg)**

$$
\frac{\begin{matrix} \Gamma \vdash f \Rightarrow \forall \overline{X}. \overline{T} \rightarrow R \quad \Gamma \vdash \overline{e} \Rightarrow \overline{S} \quad |\overline{X}| \gt 0 \\ \emptyset \vdash \overline{S} \lt: \overline{T} \Rightarrow C \quad \emptyset \vdash R \lt: V \Rightarrow D \quad \sigma \in \bigwedge C \wedge D \end{matrix}}{\Gamma \vdash f(\overline{e}) \Leftarrow V} \quad (\text{C-App-InfAlg})
$$

This **checking** version of `App-InfAlg` describes constraint-solving for type parameters.

- Steps:
  1. Synthesize types for $f$ and $\overline{e}$.
  2. Generate constraints:
     - $C$: Argument types $\overline{S}$ must be subtypes of expected parameter types $\overline{T}$.
     - $D$: Actual return type $R$ must be a subtype of expected type $V$.
  3. Solve the conjunction $\bigwedge C \wedge D$. If a solution (substitution $\sigma$) exists, type checking succeeds. Since this is a checking rule, we only require solution existence, not computation.

---

### Top and Bottom Types

**10. Checking - Top Type (Checking-Top)**

$$
\frac{\Gamma \vdash e \Rightarrow T}{\Gamma \vdash e \Leftarrow \top} \quad (\text{C-Top})
$$

This rule switches from checking to synthesis mode. When checking $e$ against top type $\top$ (where all types are subtypes of $\top$), the check always succeeds. Since $\top$ provides no constraints, we directly **synthesize** $e$'s concrete type $T$.

---

**11. Synthesis - Application - Bottom Type (Synthesis-App-Bot)**

$$
\frac{\Gamma \vdash f \Rightarrow \bot \quad \Gamma \vdash \overline{e} \Rightarrow \overline{S}}{\Gamma \vdash f [\overline{T}] (\overline{e}) \Rightarrow \bot} \quad (\text{S-App-Bot})
$$

Special case when function type is $\bot$ (bottom type), representing non-terminating expressions (e.g., exceptions).

- If $f$'s type is $\bot$, the application result is $\bot$ regardless of arguments.
- Since $\bot$ is a subtype of all types (including function types), a $\bot$-typed expression can be applied as any function.

---

**12. Checking - Application - Bottom Type (Checking-App-Bot)**

$$
\frac{\Gamma \vdash f \Rightarrow \bot \quad \Gamma \vdash \overline{e} \Rightarrow \overline{S}}{\Gamma \vdash f [\overline{T}] (\overline{e}) \Leftarrow R} \quad (\text{C-App-Bot})
$$

**Checking** rule for $\bot$-typed functions.

- If $f$ has type $\bot$, the application result is $\bot$.
- Since $\bot$ is a subtype of any type $R$, the check always succeeds.
