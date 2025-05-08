---
taxon: Theorem
title: add-lsb
---

> 对于所有 $x : \text{Bits}$， $\text{add}(x, \text{lsb}(x)) = \text{atLSB}(\text{inc}, x)$ 且 $\text{subtract}(x, \text{lsb}(x)) = \text{atLSB}(\text{dec}, x)$。

（注：代码中 $\text{atLSB}$ 的定义为 `at_lsb`）

**证明** 对 $x$ 进行简单的归纳即可。
