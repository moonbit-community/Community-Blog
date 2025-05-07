---
taxon: Theorem
---

> 加上LSB是沿芬威克索引树向上移动到最近活跃父节点的正确方法，即
$$\begin{align*} & \text{activeParentFenwick}(x) \\ &= \text{b2f}(n, \text{activeParentBinary}(\text{f2b}(n, x))) \\ &= \text{add}(x, \text{lsb}(x)) \end{align*} $$
> 在范围 $[1, 2^n)$ 上处处成立。（我们排除了 $2^n$，因为它对应于芬威克索引方案下的树根。）

**证明**

$$
\begin{aligned}
& \text{b2f}(n, \text{activeParentBinary}(\text{f2b}'(n, x))) \\
= & \text{unshift}(n + 1, \text{inc}(\text{shift}(n + 1, x))) & \{ \text{先前的计算} \} \\
= & \text{atLSB}(\text{dec}, x) & \{ \text{引理 (sentinel)} \} \\
= & \text{add}(x, \text{lsb}(x)) & \{ \text{引理 (add-lsb)} \}
\end{aligned}
$$
