---
taxon: Theorem
title: while-inc-dec
---

> 以下两条定理对所有 Bits 值均成立：

* $\text{inc}(\text{while}(\text{odd}, \text{shr}, \cdot)) = \text{while}(\text{even}, \text{shr}, \text{inc}(\cdot))$
* $\text{dec}(\text{while}(\text{even}, \text{shr}, \cdot)) = \text{while}(\text{odd}, \text{shr}, \text{dec}(\cdot))$

**证明** 简单的 `Bits` 归纳证明。例如，对于 `inc` 的情况，两侧的函数都会丢弃连续的 1 位，然后将第一个 0 位翻转为 1。
