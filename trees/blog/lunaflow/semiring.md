---
title: Semiring
---

在抽象代数中，一个**半环**（Semiring）是一个集合 $R$，
配备了两个二元运算：加法 $+$ 和乘法 $*$，且满足下面的性质：

- $(R, +, 0)$ 是一个交换群（Commutative Group），即满足结合律、交换律和存在单位元。
- $(R, *, 1)$ 是一个幺半群（Monoid），即满足结合律和存在单位元。

除此之外，还满足下面两条性质：

- 分配律：$a * (b + c) = a * b + a * c$ 和 $(a + b) * c = a * c + b * c$。
- $0 * a = 0$ 和 $a * 0 = 0$，其中 $0$ 是加法的单位元。
