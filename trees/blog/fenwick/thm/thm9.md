---
taxon: Theorem
---

> 减去 LSB 是将芬威克树向上移动到覆盖当前段的之前段的活动节点的正确方法、
$$\begin{align*} & \text{prevSegmentFenwick}(x) \\ &= \text{b2f}(n, \text{prevSegmentBinary}(\text{f2b}(n, x))) \\ &= \text{subtract}(x, \text{lsb}(x)) \end{align*} $$
> 在范围 $[1, 2^n)$ 上处处成立。

**证明**

$$
\begin{aligned}
& \text{b2f}(n, \text{prevSegmentBinary}(\text{f2b}(n, x))) \\
  & \{ \text{展开定义} \} \\
= & \text{unshift}(n + 1, \underline{\text{inc}(\text{dec}}(\text{while}(\text{even}, \text{shr}, \text{dec}(\text{shift}(n + 1, x)))))) \\
  & \{ \text{引理 (while-inc-dec)} \} \\
= & \underline{\text{unshift}(n + 1}, \text{while}(\text{even}, \text{shr}, \text{dec}(\text{shift}(n + 1, x)))) \\
  & \{ \text{unshift} \} \\
= & \text{clear}(n + 1, \underline{\text{while}(\text{not}(\text{test}(n + 1, \cdot)), \text{shl}  , \text{while}(\text{even}, \text{shr}}, \text{dec}(\text{shift}(n + 1, x)))))) \\
  & \{ \text{引理 (shl-shr)} \} \\
= & \underline{\text{clear}(n + 1, \text{while}(\text{not}(\text{test}(n + 1, \cdot)), \text{shl}}, \text{dec}(\text{shift}(n + 1, x)))) \\
  & \{ \text{unshift} \} \\
= & \text{unshift}(n + 1, \text{dec}(\text{shift}(n + 1, x))) \\
  & \{ \text{引理 (sentinel)} \} \\
= & \text{atLSB}(\text{dec}, x) \\
  & \{ \text{引理 (add-lsb)} \} \\
= & \text{subtract}(x, \text{lsb}(x)) \\
\end{aligned}
$$