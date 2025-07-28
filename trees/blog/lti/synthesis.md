---
title: Local Type Argument Synthesis
collect: true
---

截至目前，我们已经定义了内核语言的类型规则，
但是距离我们的目标还有很大距离：核心语言要求我们做出很多注解，
包括多态实例化时需要提供的类型参数，因为这在代码中非常常见，因此这是我们本节首要解决的痛点。

此即**局部类型参数合成**（Local Type Argument Synthesis）的目标：允许程序员在调用多态函数时，安全地省略其类型参数，写成 $\text{id}(3)$ 而不是 $\text{id}[\mathbb{Z}](3)$ 的形式。省略类型参数后，一个核心挑战随之而来：对于一个给定的应用，如 $\text{id} (x)$（其中 $x : \mathbb{Z}$，且 $\mathbb{Z} \lt: \mathbb{R}$），通常存在多种合法的类型参数实例化方案，例如这里的 $\text{id} [\mathbb{Z}](x)$ 或 $\text{id} [\mathbb{R}](x)$。我们必须确立一个清晰的标准来做出选择：选择能为整个应用表达式带来最精确（即最小）结果类型的类型参数。在 $\text{id} (x)$ 的例子中，由于 $\text{id} [\mathbb{Z}](x)$ 的结果类型 $\mathbb{Z}$ 是 $\text{id} [\mathbb{R}](x)$ 的结果类型 $\mathbb{R}$ 的一个子类型，前者显然是更优、更具信息量的选择。

然而，这种基于「最佳结果类型」的局部策略并非万能。在某些情况下，「最佳」解可能并不存在。例如，假设一个函数 $f$ 的类型为 $\forall X. () \to (X \to X)$。对于应用 $f()$，$f[\mathbb{Z}]()$ 和 $f[\mathbb{R}]()$ 都是合法的补全，其结果类型分别为 $\mathbb{Z} \to \mathbb{Z}$ 和 $\mathbb{R} \to \mathbb{R}$。这两种函数类型在子类型关系下是**不可比较的**，因此不存在一个唯一的最小结果类型。在这种情况下，局部合成宣告失败。

回顾之前的核心语言定义，我们要求 application 构造的形式为 $e[\overline{T}](\overline{e})$，
也就是说我们手动填写了类型参数 $\overline{T}$，规则 `App` 能够根据此参数为应用表达式计算出结果类型。
现在我们为了语言更简单易用，允许省略类型参数 $\overline{T}$，现在我们更新语言的构造：

![spec](moonbit/src//lti/syntax.mbt#:include)

这里加入了新的表达式结构 `EAppI(Expr, Array[Expr])`，对应我们的省略类型参数形式。
（为了后文叙述方便，这里也增加了后文会用到的 `EAbsI` 构造）
现在我们需要一条新的规则：

$$
\frac{\text{magic we don't know}}{\Gamma \vdash f (\overline{e}) : [\overline{T}/\overline{X}]R} \quad (\text{App-Magic})
$$

身为人类我们可以用直觉来制定规则，甚至设计出一些无法写成代码的声明式规则，
精确地定义「何为一次正确的、最优的类型参数推断」：

$$
\frac{
    \begin{array}{l}
    \Gamma \vdash f : \forall \overline{X}. \overline{T} \to R
    \qquad \exists \overline{U}
    \\
    \Gamma \vdash \overline{e} : \overline{S}
    \qquad
    |\overline{X}| > 0
    \qquad
    \overline{S} \lt: [\overline{U}/\overline{X}]\overline{T}
    \\
    \text{forall} (\overline{V}). \overline{S} \lt: [\overline{V}/\overline{X}]\overline{T} \implies [\overline{U}/\overline{X}]R \lt: [\overline{V}/\overline{X}]R
    \end{array}
}{\Gamma \vdash f(\overline{e}) : [\overline{U}/\overline{X}]R} \quad (\text{App-InfSpec})
$$

此处我们使用存在量化 $\exists \overline{U}$，并且要求 $\overline{U}$ 满足很多条件。
例如 $\overline{S} \lt: [\overline{U}/\overline{X}]\overline{T}$ 为合法性约束。
它规定我们所选定的类型参数 $\overline{U}$ 必须是合法的。
所谓合法，即指将 $\overline{U}$ 代入函数的形式参数类型 $\overline{T}$ 后，实际参数的类型 $\overline{S}$ 必须是其子类型。
更重要的是最后一条 $\text{forall} (\overline{V}). \overline{S} \lt: [\overline{V}/\overline{X}]\overline{T} \implies [\overline{U}/\overline{X}]R \lt: [\overline{V}/\overline{X}]R$ 规则，
它要求我们对所有可能的类型参数元组 $\overline{V}$ 进行考量，
这可以转化为对潜在无限空间 $\overline{V}$ 进行搜索的过程，是典型的非构造性描述，
我们无法在计算机中实现它。

至此，我们的目标已经明确：我们需要一个真正可执行的算法，其结果与 (App-InfSpec) 一致，
但不需要我们进行非构造性的搜索和回溯。这正是「约束生成」这一步骤所要扮演的角色。
它的设计动机，源于对问题本身的一次精妙的视角转换。
