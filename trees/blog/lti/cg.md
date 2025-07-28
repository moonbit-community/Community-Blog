---
title: Constraint Generation
collect: true
---

与其将类型参数推断视为一个在无限可能性中「寻找并验证最优解」的搜索问题，
不妨将其重构为一个类似于解代数方程的「求解未知数边界」的问题。
我们不再去猜测类型参数 $\overline{X}$ 可能是什么，
而是通过分析子类型关系本身，去推导出 $\overline{X}$ 必须满足的条件。

观察到我们的规则存在子类型约束，不妨考虑一般情况 $S \lt: T$，
这本身就隐含着对其构成部分（包括其中的未知变量）的约束。
若 $X$ 是 $T$ 中的一个未知变量，那么 $S$ 的结构就必然会限制 $X$ 可能的形态。
我们的算法，正是要将这种隐含的、结构上的限制，转化为一组显式的、关于 $X$ 上下界的断言。

然而，在系统性地提取这些约束之前，我们必须首先面对一个与变量作用域相关的、
虽属前期准备但至关重要的挑战。若不妥善处理，我们生成的约束本身就可能是非良构的。
这一挑战，催生了算法的第一个具体操作步骤：变量消去。

[+](/blog/lti/var_elim.md#:embed)

约束生成是局部类型参数合成算法的核心引擎。
在通过变量消去确保了作用域安全之后，
此步骤的使命是将一个子类型判定问题——例如，
$S \lt: T$，其中 $S$ 或 $T$ 中含有待定的类型参数 $\overline{X}$ 转化为一组对这些未知参数 $\overline{X}$ 的显式约束。
现在我们形式化地定义代码中的约束具体是什么结构：

- **约束 (Constraint)**：在本系统中，每一个约束都具有形式 $S_i \lt: X_i \lt: T_i$，它为单个未知类型变量 $X_i$ 同时指定了一个**下界 (lower bound)** $S_i$ 和一个**上界 (upper bound)** $T_i$ 。

- **约束集 (Constraint Set)**：一个约束集 $C$ 是关于一组未知变量 $\overline{X}$ 到其对应约束的有限映射（在代码中可以实现为一个 Hash Map）。约束集的一个关键不变量是，其中任何约束的上下界（$S_i, T_i$）都不能含有任何待定的未知变量（即 $\overline{X}$ 中的变量）或任何需要被消去的局部变量（即 $V$ 中的变量）。**空约束集 ($\emptyset$)** 代表最无限制的约束，相当于为每一个 $X_i$ 指定了约束 $\bot \lt: X_i \lt: \top$ 。
- **约束集的交 ($\wedge$)** 定义为两个约束集 $C$ 和 $D$ 的交集，是通过将其对同一个变量的约束进行合并得到的。新的下界是原下界的**最小上界（join, $\vee$）**，而新的上界是原上界的**最大下界（meet, $\wedge$）** 。

[+-](/blog/lti/cg_def_code.md#:embed)

**约束生成**过程被形式化为一个推导关系 $V \vdash_{\overline{X}} S \lt: T \Rightarrow C$，其意为：在需要回避的变量集为 $V$ 的条件下，为使 $S \lt: T$ 成立，关于未知变量 $\overline{X}$ 需满足的（最弱）约束集是 $C$，这个 $C$ 可以被视为是该推导关系的输出。

算法由一组递归规则定义，其中关键规则如下 （注：我们始终假定 $\overline{X} \cap V = \emptyset$）：

- **平凡情况 (Trivial Cases)**：当子类型关系的上界是 $\top$ 或下界是 $\bot$ 时，该关系无条件成立，因此生成一个空约束集 $\emptyset$ 。
- **上界约束 (Upper Bound Constraint)**：当需要判定 $Y \lt: S$（其中 $Y \in \overline{X}$ 是未知变量，而 $S$ 是已知类型）时，算法会为 $Y$ 生成一个上界约束。
  $$
  \frac{Y \in \overline{X} \quad S \Downarrow^V T \quad \text{FV}(S) \cap \overline{X} = \emptyset}{V \vdash_{\overline{X}} Y \lt: S \Rightarrow \{ \bot \lt: Y \lt: T \}} \quad (\text{CG-Upper})
  $$
  注意，这里利用了前述的**变量消去**操作（$S \Downarrow^V T$）来确保上界 $T$ 本身是良构的 。
- **下界约束 (Lower Bound Constraint)**：对偶地，当需要判定 $S \lt: Y$ 时，算法为 $Y$ 生成一个下界约束。
  $$
  \frac{Y \in \overline{X} \quad S \Uparrow^V T \quad \text{FV}(S) \cap \overline{X} = \emptyset}{V \vdash_{\overline{X}} S \lt: Y \Rightarrow \{ T \lt: Y \lt: \top \}} \quad (\text{CG-Lower})
  $$
- **函数类型 (Function Type)**：当比较两个函数类型时，算法递归地处理其参数和返回类型，并将生成的子约束集合并。
  $$
  \frac{V \cup \{\overline{Y}\} \vdash_{\overline{X}} \overline{T} \lt: \overline{R} \Rightarrow \overline{C} \quad V \cup \{\overline{Y}\} \vdash_{\overline{X}} S \lt: U \Rightarrow D}{V \vdash_{\overline{X}} \forall \overline{Y}.\overline{R} \to S \lt: \forall \overline{Y}.\overline{T} \to U \Rightarrow (\bigwedge \overline{C}) \wedge D} \quad (\text{CG-Fun})
  $$
  这里，通过对子约束集取**交集 ($\wedge$)**，实现了约束的累积。

[+-](/blog/lti/cg_code.md#:embed)

一个至关重要的观察是，在任何一次调用 $V \vdash_{\overline{X}} S \lt: T \Rightarrow C$ 时，未知变量 $\overline{X}$ 都只会出现在 $S$ 和 $T$ 的其中一边。这使得整个过程是一个**匹配模子类型**（matching-modulo-subtyping）问题，而非一个完全的合一（unification）问题，从而保证了算法的简洁性与确定性。

<!-- 这套生成算法的正确性由两个互补的定理来保证：

- **可靠性（Soundness）**：算法是正确的。如果算法为 $S\lt:T$ 生成了约束集 $C$，那么任何一个满足 $C$ 的类型代换 $\sigma$（记作 $\sigma \in C$），都必然能使 $\sigma S \lt: \sigma T$ 成立 。
- **完备性（Completeness）**：算法是「足够好」的。反之，如果存在某个代换 $\sigma$ 使得 $\sigma S \lt: \sigma T$ 成立，那么算法必然能成功地生成一个约束集 $C$，并且 $\sigma$ 必然满足 $C$（即 $\sigma \in C$）。

这两个性质共同表明，约束生成器精确地刻画了所有可能的解，不多也不少。 -->
