---
title: Bidirectional Checking
collect: true
---

At this point, we have thoroughly dissected the first key focus of this article: local type parameter synthesis. Through a logically rigorous and fully executable algorithm comprising "variable elimination," "constraint generation," and "parameter calculation," it perfectly resolves the cumbersome type parameter annotation issues caused by fine-grained multipropositions, achieving the first of the three design principles stated in the introduction.

However, our toolbox remains incomplete. Revisiting the three design principles proposed in the introduction based on ML code analysis, two critical challenges remain unresolved:

1. **Convenience of Higher-Order Programming**: How to infer the type of bound variables (e.g., `x` in `fun[](x) x+1`) within anonymous functions?
2. **Support for Purely Functional Style**: How to enable extensive local variable bindings (e.g., `let x = ...`) without explicit type annotations?

The local type parameter synthesis mechanism, with its inherently **bottom-up** information flow, derives an optimal result type based on the existing types of functions and parameters. This approach falls short for the two problems above because expressions like `fun[](x) x+1` contain no substructures that provide type information for `x`.

We consider a powerful local inference technique conceptually complementary to the former. Instead of relying solely on bottom-up information synthesis, it introduces a **top-down** information flow, allowing the **context** surrounding an expression to guide its internal type checking. This is **Bidirectional Type Checking**. Though its core idea has long been a "folk consensus" in the programming language community and has been applied in some attribute grammar-based ML compilers, this article rigorously axiomatizes it within a formal system combining subtyping and impredicative polymorphism. We present it as an independent local inference method, revealing surprisingly potent capabilities.

#### **Two Modes: Synthesis and Checking**

1. **Synthesis Mode ($\Rightarrow$)**
   - In this mode, type information propagates **bottom-up**.
   - Its goal is to compute (or "synthesize") the type of an expression based on the types of its subexpressions.
   - This corresponds to traditional type checking and applies to contexts where the expected type is unknown, such as top-level expressions or the function part of an application node.

2. **Checking Mode ($\Leftarrow$)**
   - In this mode, type information propagates **top-down**.
   - Its goal is to verify (or "check") whether an expression satisfies an "expected type" (or a subtype thereof) provided by its context.
   - This mode activates when the context already determines the expression's type.

The essence of bidirectional checking lies in the flexible switching between modes. A typical function application `f(e)` perfectly illustrates this process: the type checker first **synthesizes** the type of function `f`, then uses this information to switch modes and **check** the argument `e`.

[+](/blog/lti/bidi_rules.md#:embed)

The final implementation centers on two key functions: `synthesis` and `check`.  
This is the most crucial exercise in this article.  
Readers are strongly encouraged to implement these functions themselves to appreciate the elegance of bidirectional checking  
and learn techniques for translating type rules into code.

[+-](/blog/lti/bidi_code.md#:embed)

The last critical objective is the design for local variable bindings,  
which requires introducing a new syntactic construct `ELet`. Its rules are straightforward:

$$
\frac{\Gamma \vdash e \Rightarrow S \quad \Gamma, x:S \vdash b \Rightarrow T}{\Gamma \vdash \textbf{let } x = e \textbf{ in } b \Rightarrow T} \quad (\text{S-Let})
$$

$$
\frac{\Gamma \vdash e \Rightarrow S \quad \Gamma, x:S \vdash b \Leftarrow T}{\Gamma \vdash \textbf{let } x = e \textbf{ in } b \Leftarrow T} \quad (\text{C-Let})
$$

Implementation is left as an exercise.
