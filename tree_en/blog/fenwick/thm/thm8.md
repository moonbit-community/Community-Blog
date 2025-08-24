---
taxon: Theorem
---

> Adding the LSB is the correct method to ascend the Fenwick index tree to the nearest active parent node, i.e.,  
$$\begin{align*} & \text{activeParentFenwick}(x) \\ &= \text{b2f}(n, \text{activeParentBinary}(\text{f2b}(n, x))) \\ &= \text{add}(x, \text{lsb}(x)) \end{align*} $$
> holds everywhere on the interval $[1, 2^n)$. (We exclude $2^n$ since it corresponds to the tree root under the Fenwick indexing scheme.)

**Proof**

$$
\begin{aligned}
& \text{b2f}(n, \text{activeParentBinary}(\text{f2b}'(n, x))) \\
= & \text{unshift}(n + 1, \text{inc}(\text{shift}(n + 1, x))) & \{ \textit{Previous calculation} \} \\
= & \text{atLSB}(\text{dec}, x) & \{ \textit{Lemma (sentinel)} \} \\
= & \text{add}(x, \text{lsb}(x)) & \{ \textit{Lemma (add-lsb)} \}
\end{aligned}
$$