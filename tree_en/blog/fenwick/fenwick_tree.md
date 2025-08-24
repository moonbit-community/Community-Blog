---
title: Fenwick trees
collect: true
---

How should we actually store a pruned segment tree in memory? If we carefully examine Figure 10, one strategy becomes apparent: simply slide each active node downward and to the right until it falls into an empty slot in the underlying array, as shown in Figure 12. This establishes a one-to-one correspondence between active nodes and indices in the range $1 \ldots n$. Another way to understand this indexing scheme is to use a post-order traversal of the tree, skipping non-active nodes, and assigning consecutive indices to the active nodes encountered during the traversal. We can also visualize this result by drawing the tree in a "right-leaning" style (Figure 13), aligning each active node vertically with the array slot where it is stored.

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig12.png" width="80%"><figcaption>Figure 12: Sliding active values downward in a pruned segment tree.</figcaption></figure>

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig13.png" width="80%"><figcaption>Figure 13: A pruned segment tree drawn in a right-leaning style, aligning nodes vertically with their storage locations.</figcaption></figure>

This method of storing active nodes from a pruned segment tree in an array is precisely what is known as a Fenwick tree. Sometimes I also refer to it as a Fenwick array, specifically to emphasize the underlying array data structure.

Admittedly, this is a clever use of space, but the key challenge lies in implementing update and range query operations. The implementations we used for segment trees—whether operating directly on the recursive data structure or performing simple index manipulations when the tree is stored in an array—relied on recursively traversing down the tree. However, when storing active nodes of the pruned tree in a Fenwick array, it is not immediately obvious which array index operations correspond to movements within the tree. To address this challenge, we first need to take a detour into a domain-specific language for handling two's complement numbers.
