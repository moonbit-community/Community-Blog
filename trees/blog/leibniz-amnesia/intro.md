
---
title: 引入
author: [kokic](https://kokic.github.io)
date: 2025-10-29
---

本文旨在展现一种不依赖于经典自动微分程序硬编码线性性和 Leibniz 律的微分手段, 且此手段同时可用于矩阵求逆. 
我们将在 [动机](./motive.md) 部分简单地阐述此手段的数学原理, 而其他部分则不涉及任何中学以上的数学推导. 

首先回顾经典自动微分程序中对线性性和 Leibniz 律的实现, 以下 Haskell 代码片段引自 [Automatic Differentiation is Trivial in Haskell][ad-haskell]. 

```haskell
instance Num Dual where
  (+) (Dual u u') (Dual v v') = Dual (u + v) (u' + v')
  (*) (Dual u u') (Dual v v') = Dual (u * v) (u' * v + u * v')
  (-) (Dual u u') (Dual v v') = Dual (u - v) (u' - v')
  ...

instance Fractional Dual where
  (/) (Dual u u') (Dual v v') = Dual (u / v) ((u' * v - u * v') / v ** 2)
  ...
```

此实现虽然在性能和简洁方面取得了良好的平衡, 但不免使人追问: 这四条微分规则是否都必须写出? 答案自然是否定的, 不过在具体编码环节要如何实践这一点, 许多读者也许并不能立刻想到. 

另一个也常被冠以 Functional Pearl 之名的主题是, 利用[星半环](./traits.md) 的性质实现矩阵的种种运算, 如求逆. 对此不熟悉的读者可阅读 Stephen Dolan 的 [Fun with semirings: a functional pearl on the abuse of linear algebra][fun-semiring]. 

[ad-haskell]: https://www.danielbrice.net/blog/automatic-differentiation-is-trivial-in-haskell/
[fun-semiring]: https://dl.acm.org/doi/10.1145/2500365.2500613
