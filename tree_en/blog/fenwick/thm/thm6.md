---
taxon: Theorem
title: add-lsb
---

> For all $x : \text{Bits}$, $\text{add}(x, \text{lsb}(x)) = \text{atLSB}(\text{inc}, x)$ and $\text{subtract}(x, \text{lsb}(x)) = \text{atLSB}(\text{dec}, x)$.

(Note: In the code, $\text{atLSB}$ is defined as `at_lsb`)

**Proof** By simple induction on $x$.