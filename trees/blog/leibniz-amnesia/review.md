
---
title: 复健
taxon: exegesis
author: [kokic](https://kokic.github.io)
date: 2025-10-29
---

$\gdef\spaces#1{~ #1 ~}$
$\gdef\Mat{\operatorname{Mat}}$

考虑一个 $2 \times 2$ 可逆矩阵 $M \in \Mat_{2 \times 2}(R)$, 也即

$$
M \spaces= \begin{pmatrix} a & b \\ c & d \end{pmatrix}, \quad ad - bc \spaces\neq 0
$$

为了储存 $(a,b,c,d) \in R^4$ 的信息，我们可以准备一个如下形式的结构体以及一个简化的构造器 `Mat2x2::mk` $: R^4 \to \Mat_{2 \times 2}(R)$

```mbt
struct Mat2x2[R] {
  a : R
  b : R
  c : R
  d : R
} derive(Show, Eq)

fn[R] Mat2x2::mk(a : R, b : R, c : R, d : R) -> Mat2x2[R] {
  { a, b, c, d }
}
```

我们知道，为了保证 `Mat2x2[R]` 能有与我们印象中的矩阵相符的性质，此处矩阵元素类型至少是一个 [半环](./traits.md). 随后可得 $0_{\Mat_{2 \times 2}}$, $1_{\Mat_{2 \times 2}}$ 和 `Mat2x2[R]` 上典范的加法与乘法。

```mbt
impl[R : Semiring] HasNil for Mat2x2[R] with nil() {
  Mat2x2::mk(R::nil(), R::nil(), R::nil(), R::nil())
}
```

$$ 0 \in {\small 半环} ~ R \spaces\implies 0_{\Mat_{2 \times 2}} \spaces= \begin{pmatrix} 0 & 0 \\ 0 &  0 \end{pmatrix} \spaces\in \Mat_{2 \times 2}(R) $$

```
impl[R : Semiring] HasOne for Mat2x2[R] with one() {
  Mat2x2::mk(R::one(), R::nil(), R::nil(), R::one())
}
```

$$ 0,1 \in {\small 半环} ~ R \spaces\implies 1_{\Mat_{2 \times 2}} \spaces= \begin{pmatrix} 1 & 0 \\ 0 &  1 \end{pmatrix} \spaces\in \Mat_{2 \times 2}(R) $$


```mbt
impl[R : Add] Add for Mat2x2[R] with add(u : Mat2x2[R], v : Mat2x2[R]) {
  Mat2x2::mk(u.a + v.a, u.b + v.b, u.c + v.c, u.d + v.d)
}
```

$$ +: R^2 \to R \spaces\implies +_{\Mat_{2 \times 2}}: \Mat_{2 \times 2}(R)^2 \to \Mat_{2 \times 2}(R) $$

```mbt
impl[R : Add + Mul] Mul for Mat2x2[R] with mul(u : Mat2x2[R], v : Mat2x2[R]) {
  {
    a: u.a * v.a + u.b * v.c,
    b: u.a * v.b + u.b * v.d,
    c: u.c * v.a + u.d * v.c,
    d: u.c * v.b + u.d * v.d,
  }
}
```
$$ \times: R^2 \to R \spaces\implies \times_{\Mat_{2 \times 2}}: \Mat_{2 \times 2}(R)^2 \to \Mat_{2 \times 2}(R) $$

于是我们得到了一个确实可计算 $+, \times$ 的 $\Mat_{2 \times 2}(R)$ 结构，且立刻可以写下：

```mbt
impl[R : Semiring] Semiring for Mat2x2[R]
```

从而使 $\Mat_{2 \times 2}(R)$ 也构成一个 [半环](./traits.md). 我们的 [目标](./kira.md) 是使 $\Mat_{2 \times 2}(R)$ 更进一步成为 [星半环](./traits.md), 也就是配备了 Kleene 星运算的 [半环](./traits.md).
