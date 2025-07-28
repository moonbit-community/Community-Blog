---
title: Language Specification
collect: true
---

在严谨地探讨类型推导这一议题之前，我们必须首先清晰地界定其推断的目标——一个无歧义的、
被完全标注的**内核语言**（internal language）。此语言是编译器内部的「真实」表达，亦是程序员书写的、
允许省略标注的**外部语言**（external language）所要翻译成的最终形式。
本文所用的内核语言，源自 Cardelli 与 Wegner 提出的，融合了子类型化与非论域性多态的著名演算 System $F_\leq$，
但在此基础上我们增设了 $\bot$ (Bottom) 类型，为了保证上确界和下确界的存在，这种代数结构的完备性，
是后续章节中约束求解算法得以简洁、确定地运行的根本保障。此外它也可以被用作那些永不返回的表达式（如抛出异常的函数）的结果类型，
我们先定义形式语言如下
（注：横线是序列记号 $\overline{X} = X_1, X_2, \dots, X_n$，类似的，$\overline{x} : \overline{T} = x_1 : T_1, \dots, x_n : T_n$）：

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

我们可将上面的形式语言简单翻译到下面的 MoonBit 代码，
其中 `Var` 是类型变量的实现：

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
