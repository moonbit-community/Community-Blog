---
title: Subtyping Relation
collect: true
---

子类型关系，记作 $S \lt: T$（读作 $S$ 是 $T$ 的一个子类型），是本形式系统的核心。它定义了类型之间的一种「可替换性」：凡是需要类型 $T$ 的地方，都可以安全地使用一个类型为 $S$ 的项来代替。

与许多理论文献中的定义不同，本文特意选择了一种**算法化**（algorithmic）的方式来呈现子类型关系。这意味着，定义中仅包含一组最核心的、可直接用于实现判定的规则，而像传递性（transitivity）这样通常作为公理的性质，在此系统中则成为了可被证明的引理。这种风格使得定义本身更接近于一个类型检查算法的规约：

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

其中 $\overline{T} \lt: \overline{R}$ 成立当且仅当 $\text{len}(T) = \text{len}(S) \land \forall 1 \leq i \leq \text{len}(S). S_i \lt: T_i$。
S-Fun 规则体现了函数类型子类型化的核心特征：在参数类型上是**逆变**（contravariant）的（子类型关系的箭头方向反转），而在返回类型上是**协变**（covariant）的（子类型关系箭头方向保持不变）。读者可以自己尝试一下将上文的形式语言翻译到 MoonBit 的一个谓词函数，或参考下面折叠起来的代码片段。

[+-](/blog/lti/subtype_code.md#:embed)

为了支持后续的约束求解算法，系统必须能计算任意两个类型的最小上界（join, 记作 $\lor$）和最大下界（meet, 记作 $\land$）。得益于 $\bot$ 和 $\top$ 的存在，这两个运算在本系统中是全函数（total functions），即对于任意一对类型，其界都必然存在。下面我们给出这两个运算的定义：

- **最小上界 $S \vee T$**
  - 若 $S \lt: T$，则结果为 $T$。
  - 若 $T \lt: S$，则结果为 $S$。
  - 若 $S$ 和 $T$ 分别为 $\forall\overline{X}.\overline{V} \to P$ 和 $\forall\overline{X}.\overline{W} \to Q$，则结果为 $\forall\overline{X}.(\overline{V} \wedge \overline{W}) \to (P \vee Q)$。
  - 在其他所有情况下，结果为 $\top$

- **最大下界 $S \wedge T$**
  - 若 $S \lt: T$，则结果为 $S$。
  - 若 $T \lt: S$，则结果为 $T$。
  - 若 $S$ 和 $T$ 分别为 $\forall\overline{X}.\overline{V} \to P$ 和 $\forall\overline{X}.\overline{W} \to Q$，则结果为 $\forall\overline{X}.(\overline{V} \vee \overline{W}) \to (P \wedge Q)$。
  - 在其他所有情况下，结果为 $\bot$

通过简单的结构归纳法可以证明，这两个运算满足以下性质：

- $S \vee T$ 和 $S \wedge T$ 分别是 $S$ 和 $T$ 的最小上界和最大下界。
- $S \lt: U$ 且 $T \lt: U$ 则 $S \vee T \lt: U$
- $U \lt: S$ 且 $U \lt: T$ 则 $U \lt: S \wedge T$

这里同样鼓励读者自己进行代码翻译，答案可展开下面的代码片段。

[+-](/blog/lti/subtype_code2.md#:embed)