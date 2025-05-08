---
title: Deriving Fenwick operations
collect: true
---

我们现在终于可以推导出在芬威克数组索引上移动所需的运算了，方法是从二叉索引树上的操作开始，并通过与芬威克索引的转换进行变换。首先，为了融合掉由此产生的转换，我们需要几个引理。

[+](/blog/fenwick/thm/thm3.md#:embed)
[+](/blog/fenwick/thm/thm4.md#:embed)

最后，我们需要一个关于将零位移入和移出值右侧的引理。

[+](/blog/fenwick/thm/thm5.md#:embed)

有了这些引理在手，让我们看看如何在芬威克数组中移动以实现 `update` 和 `query`；我们先从 `update` 开始。在实现 `update` 操作时，我们需要从一个叶节点开始，沿着路径向上到达根节点，更新沿途所有活跃的节点。实际上，对于任何给定的叶节点，其最近的活跃父节点恰好是存储在过去对应于该叶节点的槽中的节点（参见图 13）。因此，要更新索引 $i$，我们只需从芬威克数组中的索引 $i$ 开始，然后重复找到最近的活跃父节点，边走边更新。回想一下，用于 `update` 的命令式代码就是这样做的，通过在每一步加上当前索引的 LSB 来找到最近的活跃父节点：

![update](moonbit/src//fenwick/fenwick.mbt#:include)

让我们看看如何推导出这种行为。
要在二叉索引方案下找到一个节点的最近活跃父节点，我们首先向上移动到直接父节点（通过将索引除以二，即执行一次右位移）；然后只要当前节点是右子节点（即索引为奇数），就继续向上移动到下一个直接父节点。这产生了如下定义：

![active_parent_binary](moonbit/src//fenwick/segment_tree.mbt#:include)

这就是为什么我们使用了根节点索引为 2 的略显奇怪的索引方案——否则这个定义对于任何活跃父节点是根节点的节点都不起作用！

现在，要推导出芬威克索引上的相应操作，我们通过与芬威克索引的转换进行共轭，计算如下。为了使计算更易读，每一步中被重写的部分都用下划线标出。

$$
\begin{align*}
& \underline{\text{b2f}(n, \text{activeParentBinary}(\text{f2b}(n, \cdot)))} \\ & \{ \text{展开定义} \}  \\ 
= & \text{unshift}(n + 1, \underline{\text{inc}(\text{while}(\text{odd}, \text{shr}}, \text{shr}(\text{dec}(\text{shift}(n + 1, \cdot)))))) \\ & \{ \text{引理 (while-inc-dec)} \} \\
= & \text{unshift}(n + 1, \text{while}(\text{even}, \text{shr}, \text{inc}(\underline{\text{shr}(\text{dec}}(\text{shift}(n + 1, \cdot)))))) \\ & \{ \text{引理 (shr-inc-dec); shift(n+1, x) 总是奇数} \} \\
= & \text{unshift}(n + 1, \text{while}(\text{even}, \text{shr}, \underline{\text{inc}(\text{shr}}(\text{shift}(n + 1, \text{dec}(\cdot)))))) \\ & \{ \text{引理 (shr-inc-dec)} \} \\
= & \text{unshift}(n + 1, \underline{\text{while}(\text{even}, \text{shr}, \text{shr}}(\text{inc}(\text{shift}(n + 1, \cdot))))) \\ & \{ \text{while(even, shr, shr(x)) = while(even, shr, x) 在偶数输入上} \}  \\
= & \underline{\text{unshift}(n + 1}, \text{while}(\text{even}, \text{shr}, \text{inc}(\text{shift}(n + 1, \cdot)))) \\ & \{ \text{unshift} \}  \\
= & \text{clear}(n + 1, \underline{\text{while}(\text{not}(\text{test}(n + 1, \cdot)), \text{shl}, \text{while}(\text{even}, \text{shr}}, \text{inc}(\underline{\text{shift}(n + 1, \cdot)})))) \\ & \{ \text{引理 (shl-shr); shift} \} \\
= & \text{clear}(n + 1, \text{while}(\text{not}(\text{test}(n + 1, \cdot)), \text{shl}, \text{inc}(\text{while}(\text{even}, \text{shr}, \text{set}(n + 1, \cdot))))) \\
\end{align*}
$$

在最后一步中，由于输入 $x$ 满足 $x \le 2^n$，我们有 $\text{inc}(\text{shift}(n + 1, x)) \lt 2^{n+2}$，因此引理 shl-shr 适用。

从右到左阅读，我们刚刚计算出的流水线执行以下步骤：

1. 设置位 $n+1$
2. 移出连续的零，直到找到最低有效位的 1
3. 加 1
4. 将零移回，使最高有效位回到位置 $n+1$，然后清除它。

直观地说，这看起来很像加上 LSB！一般来说，要找到 LSB，必须移过连续的 0 位，直到找到第一个 1；问题是如何跟踪移过了多少个 0 位。`lsb` 函数本身通过递归栈来跟踪；找到第一个 1 位后，递归栈展开并将所有递归经过的 0 位重新追加回去。上述流水线代表了一种替代方法：将位 $n+1$ 设置为“哨兵”来跟踪我们移动了多少；右移直到第一个 1 确实在个位上，此时我们加 1；然后通过左移将所有 0 位移回，直到哨兵位回到 $n+1$ 的位置。这个过程的一个例子如图 19 所示。当然，这只适用于值足够小，以至于哨兵位在整个操作过程中不会受到干扰的情况。

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig19.png" width="50%"><figcaption>图 19: 使用哨兵位和移位来加上 LSB。</figcaption></figure>

为了使这一点更形式化，我们首先定义一个辅助函数 `at_lsb`，它执行一个“在 LSB 处”的操作，即它移出 0 位直到找到一个 1，应用给定的函数，然后恢复 0 位。

![at_lsb](moonbit/src//fenwick/segment_tree.mbt#:include)

[+](/blog/fenwick/thm/thm6.md#:embed)

我们可以将“带哨兵的移位”方案与 `atLSB` 形式化地关联起来，通过以下（相当复杂的）引理：

[+](/blog/fenwick/thm/thm7.md#:embed)
[+](/blog/fenwick/thm/thm8.md#:embed)

我们可以进行类似的过程来推导前缀查询的实现（据称它涉及减去 LSB）。同样，如果我们想计算 $[1, j]$ 的和，我们可以从芬威克数组中的索引 $j$ 开始，它存储了结束于 $j$ 的唯一段的和。如果索引 $j$ 处的节点存储了段 $[i, j]$，我们接下来需要找到存储结束于 $i-1$ 的段的唯一节点。我们可以重复这样做，一路累加段的和。

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig20.png" width="80%"><figcaption>图 20: 沿着线段树向上移动，找到连续的前缀段。</figcaption></figure>

从图 20 中寻找灵感，我们可以看到我们想要做的是找到我们最近的非活跃父节点的左兄弟，也就是说，我们向上走直到找到第一个作为右子节点的祖先，然后移动到它的左兄弟。在二叉索引方案下，这可以简单地实现为：

![prev_segment_binary](moonbit/src//fenwick/segment_tree.mbt#:include)

[+](/blog/fenwick/thm/thm9.md#:embed)