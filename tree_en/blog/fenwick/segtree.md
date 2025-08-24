---
title: Segment tree
collect: true
---

[+](/blog/fenwick/segtree_code.md#:embed)

Although this implementation is simple and relatively easy to understand, it introduces considerable overhead compared to merely storing the value sequence in an array. We can utilize space more cleverly by storing all nodes of the segment tree in a single array using a standard left-to-right, breadth-first indexing scheme as shown in Figure 9 (for example, this scheme or its variants are commonly used in implementing binary heaps). The root node is labeled 1; each time we descend one level, we append a bit to the existing binary representation: append 0 when moving to the left child and 1 when moving to the right child.

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig9.png" width="80%"><figcaption>Figure 9: Indexing a binary tree</figcaption></figure>

Thus, the binary representation of each node's index records the sequence of left/right choices along the path from the root to that node. Moving from a node to its child requires a single left shift and optionally adding 1; moving to its parent requires a right shift. This defines a bijection from positive natural numbers to nodes of an infinite binary tree. If we denote the segment tree array as $s_1 \ldots s_{2n-1}$, then $s_1$ stores the sum of all $a_i$, $s_2$ stores the sum of the first half of $a_i$, $s_3$ stores the sum of the second half, and so on. The values $a_1 \ldots a_n$ themselves are stored as $s_n \ldots s_{2n-1}$.

The key insight is that since descending recursively through the tree corresponds to simple index operations, all discussed algorithms can be directly translated into code that manipulates a (mutable) array: for example, instead of storing references to subtrees, we store an integer index; whenever we need to descend left or right, we simply multiply the current index by 2, or by 2 and add 1. Storing tree nodes in an array also enables additional possibilities: we need not always start recursing downward from the root but can instead traverse upward from a specific index of interest.

So how do we transition from segment trees to Fenwick trees? We begin with a seemingly trivial observation: not all values stored in the segment tree are essential. Of course, in one sense, all non-leaf nodes are "unnecessary" because they represent cached interval sums that could be recomputed from the original sequence. This is precisely the core idea of segment trees: caching these "redundant" sums to trade space for time, enabling fast arbitrary updates and range queries at the cost of doubling storage.

But that's not what I mean! In fact, there exists another set of values we can discard while still maintaining logarithmic time complexity for updates and range queries. Which values? Simply discard the data in every right child. Figure 10 shows our example tree with data removed from all right children. Note that "every right child" includes both leaf and internal nodes: we discard data associated with all nodes that are right children relative to their parent. We call nodes with discarded data inactive nodes, and the remaining nodes (left children and the root) active nodes. We also refer to trees thinned in this manner—where all right children are made inactive—as thinned trees.

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig10.png" width="80%"><figcaption>Figure 10: Deactivating all right children in a segment tree.</figcaption></figure>

Updating a thinned tree is straightforward: update the same nodes as before, ignoring any updates to inactive nodes. But how do we answer range queries? It is not difficult to see that the remaining information suffices to reconstruct the discarded data (you might try convincing yourself: can you infer what the gray nodes in Figure 10 should be without referring to previous diagrams?). However, this observation alone does not yield an efficient algorithm for computing range sums.

The key is to consider prefix sums. As seen in the introduction and the implementation of the `range` function in Section 2.1, if we can compute the prefix sum $P_k = a_1 + \cdots + a_k$ for any $k$, then we can compute the range sum $a_i + \cdots + a_j$ via $P_j - P_{i-1}$.

[+](/blog/fenwick/thm/thm1.md#:embed)

Figure 11 illustrates the process of executing a prefix query on a segment tree. Note that the accessed right children are either blue or gray; the only green nodes are left children.

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig11.png" width="80%"><figcaption>Figure 11: Performing a prefix query on a segment tree.</figcaption></figure>
