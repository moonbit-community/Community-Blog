
---
title: 数学方面的动机
taxon: appendix
author: [kokic](https://kokic.github.io)
date: 2025-10-29
---

$\gdef\CC{\mathbb{C}}$

历史上 Mathworks 的创始人 Cleve Moler 曾发现过利用复数的数值微分方法, 称为 Complex step 微分法, 但其方法也完全适用于符号微分, 并且思路和现在称为 [自动微分][ad-haskell] 的做法完全相同, 都是意识到需要分离 $R^R = R \to R$ 和 $\{f' : f \in R^R \}$. 另一方面, 光滑函数 $f$ 的 Taylor 级数的有限项截断可视为多项式, 所有次数不超过 $n$ 的多项式构成的 $n+1$ 维 $k$-向量空间 $k[x]^{\le n}$, 其基为 $\{1,x,\cdots,x^n\}$, 我们取 $n=2$ 处的截断, 此多项式就是 $f$ 的切线, 已完整记录 $f$ 导数的信息, 这意味着 $f,f'$ 本就是两个维度的对象. 

Complex step 微分法依赖这样一条性质: 复数域 $\CC = \R[x]/(x^2+1)$ 可以看成维数为 $2$, 典范基为 $\{1,\sqrt{-1}\}$ 的 $\R$-向量空间. 而 [自动微分][ad-haskell] 用的是对偶数或曰抛物复数 $R[x]/(x^2) \cong R^2$. 完全相同的线性代数道理告诉我们使用双曲复数 $\R[x]/(x^2-1) \cong R^2$ 一样可以做到 [自动微分][ad-haskell]. 

Iwasawa 分解对所有半单李群有效, 所以任意实二阶可逆矩阵群 $\operatorname{GL}(2,\R)$ 被分解为 "复数部分"、"双曲部分" 和 "抛物部分", 并一齐给出了复数的矩阵表示. 完全自然地, 我们可以考虑对应着抛物部分的对偶数 $R[x]/(x^2)$ 的矩阵表示, 并通过这种矩阵表示进行符号微分. 顺着这个思路, 想必读者就能自行发现 [本文](./index.md) 的 [方法](./derive.md) 了. 

[ad-haskell]: https://www.danielbrice.net/blog/automatic-differentiation-is-trivial-in-haskell/
