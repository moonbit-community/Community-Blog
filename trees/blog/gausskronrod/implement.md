---
title: Gauss-Kronrod 求积算法实现
collect: true
---

如下为 MoonBit 实现的 15 (7 + 8) 点 Gauss-Kronrod 求积算法，其中 `abscissae` 为求积节点，`weights` 为求积系数，均为取积分区间为 $[-1, 1]$，权函数 $\rho(x)=1$ 计算出来的值，可以通过查表得到。为达到精度要求，使用二分法进行递归求积。

![quad](moonbit/src//gausskronrod/quad.mbt#:include)