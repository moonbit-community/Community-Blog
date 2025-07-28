---
title: Calculating Type Arguments
collect: true
---

通过前述的约束生成步骤，我们已经成功地将一个非构造性的最优解搜索问题，
转化为了一个具体、有形的产物：一个约束集 $C$。
这个约束集，凝聚了为了使整个多态应用类型正确，所有待定类型参数 $\overline{X}$ 必须满足的全部边界条件。
对于每一个未知变量 $X_i$，我们都得到了一个形如 $S_i \lt: X_i \lt: T_i$ 的合法区间。

至此，算法的第一阶段「我们对未知数了解了什么？」已经圆满完成。
然而，我们的工作尚未结束。一个约束区间，例如 $\mathbb{Z} \lt: X \lt: \mathbb{R}$，
本身可能允许多个合法的解（如 $\mathbb{Z}$ 或 $\mathbb{R}$）。
我们最终必须为每一个 $X_i$ 挑选出一个**具体的**类型值，以完成对内核语言项的最终构造。

这就引出了算法的最后一个，也是画龙点睛的一步：**我们应依据何种准则，从每个变量的合法区间中做出最终的选择？**
答案，必须回归到我们的初衷，即 App-InfSpec 规约中所声明的**最优性**要求：
我们所做的选择，必须能使整个应用表达式获得**唯一的、最小的结果类型**。
因此，算法的最后一步，便是要设计一个选择策略，
它能利用我们已经辛勤收集到的约束集 $C$，
并结合函数原始的返回类型 $R$，
来计算出一组能最终最小化 $R$ 的具体类型参数。
这便是本节「参数计算」的核心任务。

[+](/blog/lti/polarity.md#:embed)

为了最小化返回类型 $R$，我们的选择策略变得显而易见：

- 若 $X_i$ 在 $R$ 中是**协变**的，我们应为 $X_i$ 选择其合法区间内的**最小值**，即其约束的**下界**。
- 若 $X_i$ 在 $R$ 中是**逆变**的，我们应为 $X_i$ 选择其合法区间内的**最大值**，即其约束的**上界**。
- 若 $X_i$ 在 $R$ 中是**不变**的，则为了保证结果的唯一性与可比较性，其合法区间必须是一个「点」，即其约束的**上下界必须相等**。

上述策略被形式化为一个计算**最小代换（minimal substitution）** $\sigma_{CR}$ 的算法。给定一个可满足的约束集 $C$ 和返回类型 $R$：

对于 $C$ 中的每一个约束 $S \lt: X_i \lt: T$：

- 若 $R$ 在 $X_i$ 上是**协变**或**常数**的，则 $\sigma_{CR}(X_i) = S$。
- 若 $R$ 在 $X_i$ 上是**逆变**的，则 $\sigma_{CR}(X_i) = T$。
- 若 $R$ 在 $X_i$ 上是**不变**的，且 $S=T$，则 $\sigma_{CR}(X_i) = S$。
- 在其他所有情况下（尤其是不变变量的约束区间 $S \neq T$ 时），$\sigma_{CR}$ **未定义**。

当 $\sigma_{CR}$ 未定义时，算法宣告失败，这精确地对应了 `App-InfSpec` 中无法找到唯一最优解的情形。

[+-](/blog/lti/solve_code.md#:embed)

[+](/blog/lti/proof_eq.md#:embed)

这一核心命题证明了我们设计的这套具体算法与 `App-InfSpec` 规约之间的等价性。
它允许我们最终用一个完全算法化的规则 `App-InfAlg` 来取代那个不可执行的规约：

$$
\frac{
  \begin{array}{ccc}
    \Gamma \vdash f : \forall \overline{X}.\overline{T} \to R & \Gamma \vdash \overline{e} : \overline{S} & |\overline{X}| > 0 \\
    \emptyset \vdash_X \overline{S} \lt: \overline{T} \Rightarrow \overline{D} & C = \bigwedge \overline{D} & \sigma = \sigma_{CR}
  \end{array}
}{
  \Gamma \vdash f(\overline{e}) : \sigma R
}
\quad (\text{App-InfAlg})
$$