---
taxon: Theorem
---

> Subtracting the LSB is the correct method to move the Fenwick tree upward to the active node covering the previous segment before the current segment.
$$\begin{align*} & \text{prevSegmentFenwick}(x) \\ &= \text{b2f}(n, \text{prevSegmentBinary}(\text{f2b}(n, x))) \\ &= \text{subtract}(x, \text{lsb}(x)) \end{align*} $$
> This holds everywhere on the interval $[1, 2^n)$.

**Proof**

$$
\begin{aligned}
& \text{b2f}(n, \text{prevSegmentBinary}(\text{f2b}(n, x))) \\
  & \{ \text{Expand definition} \} \\
= & \text{unshift}(n + 1, \underline{\text{inc}(\text{dec}}(\text{while}(\text{even}, \text{shr}, \text{dec}(\text{shift}(n + 1, x)))))) \\
  & \{ \text{Lemma (while-inc-dec)} \} \\
= & \underline{\text{unshift}(n + 1}, \text{while}(\text{even}, \text{shr}, \text{dec}(\text{shift}(n + 1, x)))) \\
  & \{ \text{unshift} \} \\
= & \text{clear}(n + 1, \underline{\text{while}(\text{not}(\text{test}(n + 1, \cdot)), \text{shl}  , \text{while}(\text{even}, \text{shr}}, \text{dec}(\text{shift}(n + 1, x)))))) \\
  & \{ \text{Lemma (shl-shr)} \} \\
= & \underline{\text{clear}(n + 1, \text{while}(\text{not}(\text{test}(n + 1, \cdot)), \text{shl}}, \text{dec}(\text{shift}(n + 1, x)))) \\
  & \{ \text{unshift} \} \\
= & \text{unshift}(n + 1, \text{dec}(\text{shift}(n + 1, x))) \\
  & \{ \text{Lemma (sentinel)} \} \\
= & \text{atLSB}(\text{dec}, x) \\
  & \{ \text{Lemma (add-lsb)} \} \\
= & \text{subtract}(x, \text{lsb}(x)) \\
\end{aligned}
$$
```