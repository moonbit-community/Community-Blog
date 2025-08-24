---
taxon: Theorem
title: while-inc-dec
---

> The following two theorems hold for all Bits values:

* $\text{inc}(\text{while}(\text{odd}, \text{shr}, \cdot)) = \text{while}(\text{even}, \text{shr}, \text{inc}(\cdot))$
* $\text{dec}(\text{while}(\text{even}, \text{shr}, \cdot)) = \text{while}(\text{odd}, \text{shr}, \text{dec}(\cdot))$

**Proof** A straightforward induction proof on `Bits`. For example, in the case of `inc`, both functions discard consecutive 1 bits and then flip the first 0 bit to 1.