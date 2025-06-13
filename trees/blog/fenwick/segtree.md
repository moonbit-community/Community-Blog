---
title: Segment tree
collect: true
---

[+](/blog/fenwick/segtree_code.md#:embed)

尽管此实现简单且相对易于理解，但与仅将值序列存储于数组中相比，它引入了相当大的开销。我们可以通过将线段树的所有节点存储在一个数组中，采用如图 9 所示的标准从左至右、广度优先的索引方案，来更巧妙地利用空间（例如，这种方案或其类似方案常用于实现二叉堆）。根节点标号为 1；每当我们向下移动一层，我们就在现有二进制表示后追加一位：向左子节点移动时追加 0，向右子节点移动时追加 1。

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig9.png" width="80%"><figcaption>图 9: 索引一颗二叉树</figcaption></figure>

因此，每个节点以二进制表示的索引记录了从根节点到达该节点的路径上左右选择的序列。从一个节点移动到其子节点，只需执行一次左位移并视情况加 1 即可；从一个节点移动到其父节点，则执行一次右位移。这便定义了一个从正自然数到无限二叉树节点的双射。若我们将线段树数组标记为 $s_1 \ldots s_{2n-1}$，那么 $s_1$ 存储所有 $a_i$ 的和，$s_2$ 存储 $a_i$ 前半部分的和，$s_3$ 存储后半部分的和，依此类推。$a_1 \ldots a_n$ 本身则存储为 $s_n \ldots s_{2n-1}$。

关键在于，既然沿树递归下降对应于对索引的简单操作，我们所讨论的所有算法都可以直接转换为处理（可变）数组的代码：例如，我们不再存储指向当前子树的引用，而是存储一个整数索引；每当需要向左或向右下降时，我们只需将当前索引乘以 2，或者乘以 2 再加 1。以数组存储树节点还带来了额外的可能性：我们不必总是从根节点开始向下递归，而是可以从某个感兴趣的特定索引出发，反向沿树向上移动。

那么，我们如何从线段树过渡到芬威克树呢？我们从一个看似无关紧要的观察开始：并非所有存储在线段树中的值都是必需的。当然，从某种意义上说，所有非叶节点都是“不必要的”，因为它们代表的是可以轻易从原始序列重新计算出来的缓存区间和。这正是线段树的核心思想：缓存这些“冗余”的和，以空间换时间，使我们能够快速执行任意的更新和区间查询，代价是将所需的存储空间加倍。

但这并非我所指！实际上，存在另一组我们可以舍弃的值，并且这样做仍然能够保持更新和区间查询的对数运行时效。舍弃哪些值呢？很简单：只需舍弃每个右子节点中的数据即可。图 10 展示了我们一直在使用的示例树，但其中每个右子节点的数据已被删除。注意，“每个右子节点”既包括叶节点也包括内部节点：我们舍弃与其父节点关系为右子节点的所有节点相关联的数据。我们将数据被丢弃的节点称为非活跃（inactive）节点，其余节点（即左子节点和根节点）称为活跃（active）节点。我们亦称，以这种方式使其所有右子节点都变为非活跃状态的树为疏树（thinned trees）。

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig10.png" width="80%"><figcaption>图 10: 使线段树中的所有右子节点失效。</figcaption></figure>

更新一棵疏树颇为容易：只需像以前一样更新相同的节点，忽略对非活跃节点的任何更新即可。但我们如何应答区间查询呢？不难看出，剩余的信息足以重构被丢弃的信息（您或许愿意尝试说服自己这一点：能否在不参考任何先前图示的情况下，推断出图 10 中灰色节点应有的值？）。然而，仅此观察本身并不能为我们提供一个良好的计算区间和的算法。

关键在于考虑前缀和。正如我们在引言以及 2.1 中 `range` 函数的实现所见，如果我们能够计算任意 $k$ 的前缀和 $P_k = a_1 + \cdots + a_k$，那么我们就能通过 $P_j - P_{i-1}$ 来计算区间和 $a_i + \cdots + a_j$。

[+](/blog/fenwick/thm/thm1.md#:embed)

图 11 阐释了在线段树上执行前缀查询的过程。注意，被访问的右子节点要么是蓝色要么是灰色；唯一的绿色节点都是左子节点。

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig11.png" width="80%"><figcaption>图 11: 在线段树上进行前缀查询。</figcaption></figure>
