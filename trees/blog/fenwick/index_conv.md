---
title: Index conversion
collect: true
---

在推导我们的索引转换函数之前，我们必须处理一个略显棘手的事实。在传统的二叉树索引方案中，如图 9 所示，根节点的索引为 1，每个左子节点的索引是其父节点的两倍，每个右子节点的索引是其父节点的两倍加一。回想一下，在一棵删减后的线段树中，根节点和每个左子节点都是活跃的，而所有右子节点都是非活跃的。这使得根节点成为一个尴尬的特例——所有活跃节点都有偶数索引，除了索引为 1 的根节点。这使得检查我们是否处于一个活跃节点变得更加困难——仅仅查看最低有效位是不够的。

解决这个问题的一个简单方法是直接给根节点赋予索引 2，然后继续使用相同的方案标记其余节点——每个左子节点是其父节点的两倍，每个右子节点是其父节点的两倍加一。这导致了如图 14 所示的索引方式，就好像我们只是取了以 1 为根的树的左子树，并忽略了右子树。当然，这意味着大约一半的可能索引被省略了——但这不成问题，因为我们只会将这些索引作为中间步骤使用，最终会被融合掉。

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig14.png" width="80%"><figcaption>图 14. 以 2 为根的二叉树索引。</figcaption></figure>

图 15 展示了一棵二叉树，其中节点以两种不同的方式编号：每个节点的左侧显示其二叉树索引（根节点索引为 2）。每个节点的右侧显示其在芬威克数组中的索引，如果它有的话（非活跃节点右半部分简单地灰色显示）。下方的表格显示了从芬威克数组索引（顶行）到二叉树索引（底行）的映射。作为一个更大的例子，图 16 在更深一层的二叉树上展示了同样的事情。

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig15.png" width="80%"><figcaption>图 15: 标有二叉树索引和芬威克索引的二叉树。</figcaption></figure>

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig16.png" width="80%"><figcaption>图 16. 标有二叉树索引和芬威克索引的更深的二叉树。</figcaption></figure>

我们的目标是找到一种方法来计算给定芬威克索引对应的二叉树索引，反之亦然。仔细观察图 16 中的表格，有个模式非常突出。首先，底行的所有数字都是偶数，这恰恰是因为二叉树的编号方式使得所有活跃节点都有偶数索引。其次，我们可以看到偶数 $32, 34 \ldots 46$ 按顺序出现在所有奇数位置上。这些正是树的叶节点，实际上，芬威克数组中每隔一个节点就是来自原始树的叶节点。与它们交替出现的，在偶数位置上的，是数字 $16, 8, 18, 4, \ldots$，它们对应于所有非叶节点；但这些恰好是图 15 中表格底行的二叉树索引序列——因为高度为 4 的树中的内部节点本身构成了一个高度为 3 的树，且节点以相同的顺序出现。

[+](/blog/fenwick/interleaving.md#:embed)

这些观察引出了 5.1 中所示的递推关系，用于计算存储在长度为 $2^n$ 的芬威克数组中的节点的二叉树索引序列 $b_n$：$b_0$ 就是单元素序列 $[2]$，否则 $b_n$ 就是偶数 $2^{n+1}, 2^{n+1} + 2, \ldots, 2^{n+1} + 2^n - 2$ 与 $b_{n-1}$ 交错排列的结果（译者注：代码实现中使用位运算代替乘方运算，在数学推理中，也将 `interleave` 记为中缀运算符 $\curlyvee$）。

我们可以检验这确实重现了 $n=4$ 时观察到的序列：

![b4](moonbit/src//fenwick/segment_tree.mbt#:include)

令 $s ! k$ 表示列表 $s$ 中的第 $k$ 项（从 1 开始计数），在代码中记为 `s.nth(k)` （译者注：这和 MoonBit 标准库的 `nth` 存在差异，它是从 0 开始的索引）。下面的代码指出了两个关于索引和交错相互作用的简单引理，即 $(xs \curlyvee ys) ! (2 \cdot j) = ys ! j$ 和 $(xs \curlyvee ys) ! (2 \cdot j - 1) = xs ! j$（只要 $xs$ 和 $ys$ 长度相等）。

```moonbit
// suppose xs.length() == ys.length()
interleave(xs, ys).nth(2 * j) == ys.nth(j)
interleave(xs, ys).nth(2 * j + 1) == xs.nth(j)
```

有了这些准备，我们可以将芬威克到二叉树的索引转换函数定义为
$$ \text{f2b}(n, k) = b_n ! k. $$

当然，由于 $b_n$ 的长度为 $2^n$，这个函数仅在范围 $[1, 2^n]$ 内有定义。

我们现在可以简化 `f2b` 的定义如下。首先，对于偶数输入，我们有

$$
\begin{align*}
& \text{f2b}(n, (2 \cdot j)) \\
= & b_n ! (2 \cdot j) & \{ \text{f2b} \} \\
= & (\text{interleave}(\text{map}((2 \cdot), [2^n \ldots 2^n + 2^{n-1} - 1]), b_{n-1})) ! (2 \cdot j) & \{ \text{b} \} \\
= & b_{n-1} ! j & \{ \text{interleave-!} \text{ 引理 } \} \\
= & \text{f2b}((n - 1), j). & \{ \text{f2b} \}
\end{align*}
$$

其中 $(2\cdot)$ 是函数 `fn { x => 2 * x }` 的简写，$[2^n \ldots 2^n + 2^{n-1} - 1]$ 是闭区间 $[2^n, 2^n + 2^{n-1} - 1]$ 的列表。对于奇数输入有：

$$
\begin{align*}
& \text{f2b}(n, (2 \cdot j - 1)) \\
= & b_n ! (2 \cdot j - 1) & \{ \text{f2b} \} \\
= & (\text{interleave}(\text{map}((2 \cdot), [2^n \ldots 2^n + 2^{n-1} - 1]), b_{n-1})) ! (2 \cdot j - 1) & \{ \text{b} \} \\
= & \text{map}((2 \cdot), [2^n \ldots 2^n + 2^{n-1} - 1]) ! j & \{ \text{interleave-!} \text{ 引理 } \} \\
= & 2 \cdot (2^n + j - 1) & \{ \text{map, 代数} \} \\
= & 2^{n+1} + 2j - 2 & \{ \text{代数} \}
\end{align*}
$$

因此，我们有

$$
\text{f2b}(n, k) =
\begin{cases}
\text{f2b}(n - 1,k / 2) & k \text{ 为偶数} \\
2^{n+1} + k - 1 & k \text{ 为奇数}
\end{cases}
$$

注意，当 $n = 0$ 时，我们必须有 $k = 1$，因此 $\text{f2b}(0, 1) = 2^{0+1} + 1 - 1 = 2$，（译者注：原文写的 *Note that when n = 0, we must have k = 1, and hence, f2b 0 1 = $2^{0+1} + 1 - 1 = 1$, as required, so this definition is valid for all n ≥ 0.* 计算有误。根据推导，$f2b(0, 1) = 2 \neq 1$，等于 2 才能对应上我们新的根节点假设）所以这个定义对所有 $n \ge 0$ 都有效。现在将 $k$ 唯一地分解为 $2^a \cdot b$，其中 $b$ 是奇数。那么通过归纳我们可以看到

$$ \text{f2b} (n, 2^a \cdot b) = \text{f2b}(n - a, b) = 2^{(n-a)+1} + b - 1. $$

换句话说，计算 `f2b` 包括只要输入是偶数就重复除以 2（即右位移），然后最终减 1 并加上一个 2 的幂。然而，要知道最后要加哪个 2 的幂，取决于我们移动了多少次。思考这个问题的一个更好的方法是在开始时加上 $2^{n+1}$，然后让它随着其他所有位一起移动。（译者注：原文在这里说的并不是很清楚，在这里补充一下我的解释：我们想要求解 $X = 2^{n-a+1} + b$，可以先乘上一个因子 $2^a$ 得到 $2^a X = 2^{n+1} + 2^ab$，这样表达式中便有一个 $k = 2^a \cdot b$ 存在，它是函数的参数。这样一来等式的右边即是 $k$ 加上一个 $2^{n+1}$，而 $X = \dfrac{2^{n+1} + 2^a \cdot b}{2^a}$，除法在这里可以使用位移操作实现）因此，我们使用我们的 `Bits` DSL 得到 `f2b` 的最终定义。单独定义 `shift` 函数将使我们的一些证明更加紧凑。

![shift](moonbit/src//fenwick/segment_tree.mbt#:include)

容易使用 QuickCheck 验证这在范围 $[1, 2^4]$ 上产生与原始的 `f2b(4, k)` 相同的结果。

现在我们转向推导 `b2f(n, _)`，它将从二叉树索引转换回芬威克索引。`b2f(n, _)` 应该是 `f2b(n, _)` 的左逆，也就是说，对于任何 $k \in [1, 2^n]$，我们应该有 $\text{b2f}(n, \text{f2b}(n, k)) = k$。
如果 $k$ 是 `f2b` 的一个输入，我们有 $k = 2^a \cdot b \le 2^n$，因此 $b-1 \lt 2^{n-a}$。故给定输出 $\text{f2b}(n, k) = m = 2^{n-a+1} + b - 1$，
$m$ 的最高位是 $2^{n-a+1}$，其余位代表 $b - 1$。所以，一般地，给定某个作为 `f2b(n, _)` 输出的 $m$，我们可以唯一地将其写为 $m = 2^c + d$，其中 $d \lt 2^{c-1}$；那么

$$ \text{b2f} (n, 2^c + d) = 2^{n-c+1} \cdot (d + 1). $$

换句话说，给定输入 $2^c + d$，我们减去最高位 $2^c$，加 1，然后左移 $n - c + 1$ 次。同样，存在一个更简单的方法：我们可以先加 1（注意因为 $d \lt 2^{c-1}$，加 1 不会干扰 $2^c$ 处的位），然后左移足够多次，使最左边的位移到位置 $n + 1$，最后移除它。即：

![unshift](moonbit/src//fenwick/segment_tree.mbt#:include)

验证：

![test_id](moonbit/src//fenwick/segment_tree.mbt#:include)
