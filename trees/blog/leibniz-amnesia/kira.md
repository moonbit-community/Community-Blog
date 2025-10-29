
---
title: 正则魔术
taxon: exegesis
author: [kokic](https://kokic.github.io)
date: 2025-10-29
---

$\gdef\spaces#1{~ #1 ~}$
$\gdef\Mat{\operatorname{Mat}}$

大部分念过中学数学的读者想来是熟悉等比数列的，即

$$ 1 ~(= q^0), ~~ q^1, ~~ q^2, ~~ q^3, \spaces\cdots, ~ q^n  $$

此数列的和不难求出，为 $\frac{1-q^n}{1-q}$. 特别地，我们发现，只要 $|q|<1$, 那 $n \to \infty$ 时一定有 $q^n = 0$, 从而 

$$ 1 + q + q^2 + q^3 + \cdots \spaces= \frac{1}{1-q} \tag{1} $$

现在，如果读者还稍微了解过正则表达式，将 $+$ 理解为匹配中的或组合子 `|`, 将 $q$ 理解为字符 `"q"`, 那么 `"q"` 的字符闭包 `q*` 就匹配空串 `""` $(= q^0)$ 或 `"q"` 的若干次重复 `"qqq..."`. 即

```
q* := "" | q | qq | qqq | ...
```

如果我们沿用这个 Kleene 星记号，则式 $(1)$ 就重写为

$$ q^* \spaces= \frac{1}{1-q} \quad \xRightarrow{~ q ~\leadsto~ 1-q ~} \quad q^{-1} \spaces= (1-q)^* $$

请读者暂且记住 $q^{-1} = (1-q)^*$ 这样一种关系，而忽略其完全形式的推导。

对于一个矩阵 $M$, 我们已经在 [复健](./review.md) 中实现了 $+$ 和 $\times$, 为了能真正计算矩阵的  Kleene 闭包 $\square^*_{\Mat_{2 \times 2}}: \Mat_{2 \times 2}(R) \to \Mat_{2 \times 2}(R)$, 我们需要从自动机的图景中窥探 $M^*$ 之等价表达，此表达应只涉及星半环 $R$ 可提供的 $+_R, \times_R, \square^*_R$ 运算。如下所示

[State diagram $G$ for $M \to M^*$](./automata.typ#:block)

$(a,b,c,d)$ 照例是 $2 \times 2$ 矩阵 $M$ 的四个分量。固定下标 $i,j$, 分量 $(M^*)_{ij}$ 的值会等于图 $G$ 中刻画所有 $i$ 到 $j$ 的路径之正则表达式。请读者亲自动手验证：

$$
\begin{aligned}
  1 \longrightarrow 1 &: \quad (a+b d^*c)^* \\
  1 \longrightarrow 2 &: \quad (a+b d^*c)^*b d^* \\
  2 \longrightarrow 1 &: \quad d^* c(a+b d^*c)^* \\
  2 \longrightarrow 2 &: \quad d^* + d^*c(a+b d^*c)^*b d^* \\
\end{aligned}
$$

简单起见记 $\alpha = (a+b d^*c)^* \in R$, 我们毫不费力就得到 

$$
M^* \spaces= \begin{pmatrix}
\alpha & \alpha b d^* \\
d^* c \alpha & \quad d^* + d^*c \alpha b d^*
\end{pmatrix}
$$

此处对 $R$ 元素 $\square$ 进行的 Kleene 星运算都可以通过 $\frac{1}{1-\square}$ 具体算出。

```mbt
fn[R : HasOne + Add + Neg + Inverse] star(x : R) -> R {
  (R::one() + x.neg()).inverse()
}
```

顺水推舟，我们用 $R$ 上的乘法逆 $\frac{1}{\square}$ 定义了 $R$ 上的 Kleene 星 $\square^*_R$, 然后用 $R$ 上的 Kleene 星 $\square^*_R$ 定义了 $\Mat_{2 \times 2}(R)$ 上的 Kleene 星 $\square^*_{\Mat_{2 \times 2}}$, 最后用 $\Mat_{2 \times 2}(R)$ 上的 Kleene 星 $\square^*_{\Mat_{2 \times 2}}$ 定义了 $\Mat_{2 \times 2}(R)$ 上的乘法逆 $\frac{1}{\square}$. 于是我们有了一个简单的逆矩阵计算实现。

```mbt
impl[R : StarSemiring] StarSemiring for Mat2x2[R] with star(u : Mat2x2[R]) {
  let (a, b, c, d) = (u.a, u.b, u.c, u.d)
  let dalt = d.star()
  let balt = b * dalt
  let aalt = (a + balt * c).star()
  let calt = dalt * c * aalt
  Mat2x2::mk(aalt, aalt * balt, calt, dalt + calt * balt)
}

fn[R : StarSemiring + Neg] Mat2x2::inverse(u : Mat2x2[R]) -> Mat2x2[R] {
  (Mat2x2::one() + u.neg()).star()
}
```
