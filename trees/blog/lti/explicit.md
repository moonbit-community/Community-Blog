---
title: Explicit Typing Rules
collect: true
---

在定义了类型与子类型关系之后，我们便可以给出内核语言的类型定则。这些规则定义了类型判断（typing judgment）的形式 $\Gamma \vdash e : T$，意为「在上下文 $\Gamma$ 中，项 $e$ 拥有类型 $T$ 」。

与子类型关系的定义一脉相承，这里的类型定则同样采用了一种算法化的呈现方式。且省略了传统类型系统中常见的包容规则（subsumption，若 $e$ 的类型为 $S$ 且 $S \lt: T$，则 $e$ 的类型亦可为 $T$）。

通过省略此规则，本系统为每一个可被类型化的项，都计算出一个**唯一的、最小的类型**，作者称之为该项的**显式类型**（manifest type）。这一设计选择，并不改变语言中可被类型化的项的集合，而只是确保了任何一个项的类型推导路径都是唯一的。这极大地增强了系统的可预测性。

### 核心定则 (Core Rules)

- **变量 (Variable)**

  $$
  \frac{}{\Gamma \vdash x : \Gamma(x)} \quad (\text{Var})
  $$

- **抽象 (Abstraction)**
  此规则统一了传统的项抽象与类型抽象。

  $$
  \frac{\Gamma, \overline{X}, \overline{x}:\overline{S} \vdash e : T}{\Gamma \vdash \mathbf{fun}[\overline{X}] (\overline{x}:\overline{S}) e : \forall \overline{X}.\overline{S} \to T} \quad (\text{Abs})
  $$

  若想要求解 $\mathbf{fun}[\overline{X}] (\overline{x}:\overline{S})$ 的类型，必须在上下文 $\Gamma$ 中添加类型变量 $\overline{X}$ 和值变量 $\overline{x}:\overline{S}$ 的绑定。然后，在这个扩展的上下文中，推导函数体 $e$ 的类型为 $T$。最终，整个函数的类型便是 $\forall \overline{X}.\overline{S} \to T$。

- **应用 (Application)**
  此规则同样统一了传统的项应用与多态应用。它首先推导函数 `f` 的类型，然后验证所有实际参数（包括类型参数与项参数）是否与函数的签名相符。
  这里的要求更宽松了一些：只要实际参数的类型满足参数类型的子类型关系即可，而不需要完全匹配。

  $$
  \frac{\Gamma \vdash f : \forall \overline{X} . \overline{S} \to R \quad \Gamma \vdash \overline{e} \lt: [\overline{T}/\overline{X}]\overline{S}}{\Gamma \vdash f[\overline{T}] (\overline{e}) : [\overline{T}/\overline{X}]R} \quad (\text{App})
  $$

  其中，记法 $\Gamma \vdash \overline{e} \lt: [\overline{T}/\overline{X}]\overline{S}$ 是一个缩写，表示 $\Gamma \vdash \overline{e} \lt: \overline{U}$，然后验证 $\overline{U} \lt: [\overline{T}/\overline{X}]\overline{S}$。最终，整个应用表达式的结果类型，是通过将实际类型参数 $\overline{T}$ 代入函数原始返回类型 $R$ 中得到的。

  [+](/blog/lti/subst_code.md#:embed)

- **Bot 应用 (Bot Application)**
  $\bot$ 类型的引入，要求我们补充一条特殊的应用规则，以维护系统的类型安全（type soundness）。
  由于 $\bot$ 是任何函数类型的子类型，一个类型为 $\bot$ 的表达式应当可以被应用于任何合法的参数，而不会产生类型错误。

  $$
  \frac{\Gamma \vdash f : \bot \quad \Gamma \vdash \overline{e} : \overline{S}}{\Gamma \vdash f[\overline{T}] (\overline{e}) : \bot} \quad (\text{App-Bot})
  $$

  此规则规定，当一个类型为 $\bot$ 的项被应用时，无论参数为何，整个表达式的结果类型也是 $\bot$，这正是我们能给出的最精确（即最小）的结果类型。

这些规则共同保证了本类型系统的一个关键性质，即**显式类型的唯一性（Uniqueness of Manifest Types）**：若 $\Gamma \vdash e : S$ 且 $\Gamma \vdash e : T$，那么必有 $S=T$。
