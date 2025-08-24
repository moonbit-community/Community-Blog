---
title: Language Specification
collect: true
---

Before rigorously discussing the topic of type inference, we must first clearly define its inference target—an unambiguous, fully annotated **internal language**. This language serves as the "true" representation within the compiler and is the final form into which the **external language**—written by programmers and allowing omitted annotations—is translated.  

The internal language used in this article originates from the well-known calculus System $F_\leq$ proposed by Cardelli and Wegner, which incorporates subtyping and impredicative polymorphism. However, we extend it by adding the $\bot$ (Bottom) type. To ensure the existence of supremum and infimum, this algebraic structure's completeness is fundamental for the concise and deterministic operation of the constraint-solving algorithm in subsequent chapters. Additionally, it can serve as the result type for expressions that never return (e.g., functions that throw exceptions). We first define the formal language as follows  
(Note: Overline denotes sequence notation $\overline{X} = X_1, X_2, \dots, X_n$; similarly, $\overline{x} : \overline{T} = x_1 : T_1, \dots, x_n : T_n$):

$$
\begin{array}{ll}
T ::= X & \text{type variable} \\
\quad~\mid~ \top & \text{maximal type} \\
\quad~\mid~ \bot & \text{minimal type} \\
\quad~\mid~ \forall \overline{X} . \overline{T} \rightarrow T & \text{function type} \\[1em]
e ::= x & \text{variable} \\
\quad~\mid~ \text{fun}[ \overline{X} ]\, ( \overline{x} : \overline{T} )\, e & \text{abstraction} \\
\quad~\mid~ e[ \overline{T} ]\, ( \overline{e} ) & \text{application} \\[1em]
\Gamma ::= \bullet & \text{empty context} \\
\quad~\mid~ \Gamma, x : T & \text{variable binding} \\
\quad~\mid~ \Gamma, X & \text{type variable binding}
\end{array}
$$

We can simply map the above formal language to the following MoonBit code,  
where `Var` implements type variables:

```moonbit
pub(all) enum Type {
  TyVar(Var)
  TyTop
  TyBot
  TyFun(Array[Var], Array[Type], Type)
} derive(Eq)

pub(all) enum Expr {
  EVar(Var)
  EApp(Expr, Array[Type], Array[Expr])
  EAbs(Array[Var], Array[(Var, Type)], Expr)
}
```

[+](/blog/lti/subtype.md#:embed)
