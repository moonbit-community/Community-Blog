
---
title: `Mat2x2[Float]`
taxon: example
author: [kokic](https://kokic.github.io)
date: 2025-10-29
---

$\gdef\spaces#1{~ #1 ~}$

作为一个小小的测试, 我们用此 [MoonBit][moonbit] 程序在 `Mat2x2[Float]` 中计算 $A^{-1}$, 这里 

$$
A \spaces= \begin{pmatrix}
1 & 2 \\ 3 & 4
\end{pmatrix}
$$

首先使 `Float` 成为 [星半环](./traits.md). 严格来说对 $q=0$ 按 $q^* = \frac{1}{1-q}$ 计算是有问题的, 我们实际上需要添加了形式无穷的紧化版本 `Float`. 这对我们试图接近的理想实数 $\R$ 也是一样, 非负扩展实数集 $\R_{\ge 0} \cup \{\infty\}$ 也即 $\R_{\ge 0}$ 的单点紧化连同实数的通常加法和乘法才能构成闭半环. 我们不在此进一步展开. 

```mbt
impl HasNil for Float with nil() {
  0
}

impl HasOne for Float with one() {
  1
}

impl Inverse for Float with inverse(x : Float) {
  1 / x
}

impl Semiring for Float

impl StarSemiring for Float with star(x : Float) {
  star(x)
}
```

现在可以用 `Mat2x2::mk(1.F, 2, 3, 4).inverse()` 计算 $A^{-1}$ 了:


```mbt
test "float matrix inverse" {
  assert_eq(Mat2x2::mk(1.F, 2, 3, 4).inverse(), Mat2x2::mk(-2, 1, 1.5, -0.5))
}
```

[moonbit]: https://www.moonbitlang.cn/
