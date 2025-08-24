---
title: Deriving Fenwick operations
collect: true
---

We can now finally derive the operations needed to move in the Fenwick array indices by starting from the operations on the binary index tree and transforming them via the conversion to Fenwick indices. First, to fuse away the resulting conversions, we need a few lemmas.

[+](/blog/fenwick/thm/thm3.md#:embed)
[+](/blog/fenwick/thm/thm4.md#:embed)

Finally, we need a lemma about shifting zeros in and out to the right of a value.

[+](/blog/fenwick/thm/thm5.md#:embed)

With these lemmas in hand, let's see how to move in the Fenwick array to implement `update` and `query`; we'll start with `update`. When implementing the `update` operation, we need to start from a leaf node and follow the path up to the root, updating all active nodes along the way. In fact, for any given leaf node, its nearest active parent node is precisely the node stored in the slot that historically corresponded to that leaf (see Figure 13). Therefore, to update index $i$, we simply start from index $i$ in the Fenwick array, then repeatedly find the nearest active parent node, updating as we go. Recall that the imperative code for `update` does exactly this by adding the current index's LSB at each step to find the nearest active parent:

![update](moonbit/src//fenwick/fenwick.mbt#:include)

Let's see how to derive this behavior.  
To find a node's nearest active parent under the binary indexing scheme, we first move up to the direct parent (by dividing the index by two, i.e., performing a right shift); then continue moving up to the next direct parent as long as the current node is a right child (i.e., the index is odd). This yields the following definition:

![active_parent_binary](moonbit/src//fenwick/segment_tree.mbt#:include)

This is why we used the slightly odd indexing scheme with the root at index 2 — otherwise this definition wouldn't work for any node whose active parent is the root!

Now, to derive the corresponding operation on Fenwick indices, we conjugate via the conversion to Fenwick indices, computing as follows. To make the calculation more readable, the rewritten parts in each step are underlined.

$$
\begin{align*}
& \underline{\text{b2f}(n, \text{activeParentBinary}(\text{f2b}(n, \cdot)))} \\ & \{ \text{expand definitions} \}  \\ 
= & \text{unshift}(n + 1, \underline{\text{inc}(\text{while}(\text{odd}, \text{shr}}, \text{shr}(\text{dec}(\text{shift}(n + 1, \cdot)))))) \\ & \{ \text{lemma (while-inc-dec)} \} \\
= & \text{unshift}(n + 1, \text{while}(\text{even}, \text{shr}, \text{inc}(\underline{\text{shr}(\text{dec}}(\text{shift}(n + 1, \cdot)))))) \\ & \{ \text{lemma (shr-inc-dec); shift(n+1, x) is always odd} \} \\
= & \text{unshift}(n + 1, \text{while}(\text{even}, \text{shr}, \underline{\text{inc}(\text{shr}}(\text{shift}(n + 1, \text{dec}(\cdot)))))) \\ & \{ \text{lemma (shr-inc-dec)} \} \\
= & \text{unshift}(n + 1, \underline{\text{while}(\text{even}, \text{shr}, \text{shr}}(\text{inc}(\text{shift}(n + 1, \cdot))))) \\ & \{ \text{while(even, shr, shr(x)) = while(even, shr, x) on even inputs} \}  \\
= & \underline{\text{unshift}(n + 1}, \text{while}(\text{even}, \text{shr}, \text{inc}(\text{shift}(n + 1, \cdot)))) \\ & \{ \text{unshift} \}  \\
= & \text{clear}(n + 1, \underline{\text{while}(\text{not}(\text{test}(n + 1, \cdot)), \text{shl}, \text{while}(\text{even}, \text{shr}}, \text{inc}(\underline{\text{shift}(n + 1, \cdot)})))) \\ & \{ \text{lemma (shl-shr); shift} \} \\
= & \text{clear}(n + 1, \text{while}(\text{not}(\text{test}(n + 1, \cdot)), \text{shl}, \text{inc}(\text{while}(\text{even}, \text{shr}, \text{set}(n + 1, \cdot))))) \\
\end{align*}
$$

In the last step, since the input $x$ satisfies $x \le 2^n$, we have $\text{inc}(\text{shift}(n + 1, x)) \lt 2^{n+2}$, so the lemma shl-shr applies.

Reading from right to left, the pipeline we just computed performs the following steps:

1. Set bit $n+1$
2. Shift out consecutive zeros until the least significant 1 is found
3. Add 1
4. Shift the zeros back in so the most significant bit returns to position $n+1$, then clear it.

Intuitively, this looks very much like adding the LSB! In general, to find the LSB, one must shift past consecutive 0 bits until the first 1 is found; the question is how to track how many 0 bits were shifted past. The `lsb` function itself uses the recursion stack to track this; after finding the first 1 bit, the stack unwinds and appends all the recursively passed 0 bits back. The pipeline above represents an alternative approach: use bit $n+1$ as a "sentinel" to track how much we shifted; right-shift until the first 1 is indeed in the units place, then add 1; then shift all the 0 bits back in by left-shifting until the sentinel bit returns to position $n+1$. An example of this process is shown in Figure 19. Of course, this only works when the value is small enough that the sentinel bit remains undisturbed throughout the operation.

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig19.png" width="50%"><figcaption>Figure 19: Using a sentinel bit and shifting to add the LSB.</figcaption></figure>

To formalize this, we first define a helper function `at_lsb` that performs an operation "at the LSB," i.e., it shifts out 0 bits until a 1 is found, applies the given function, then restores the 0 bits.

![at_lsb](moonbit/src//fenwick/segment_tree.mbt#:include)

[+](/blog/fenwick/thm/thm6.md#:embed)

We can formally relate the "shift with sentinel" scheme to `atLSB` via the following (rather complex) lemma:

[+](/blog/fenwick/thm/thm7.md#:embed)
[+](/blog/fenwick/thm/thm8.md#:embed)

We can perform a similar process to derive the implementation for prefix queries (which allegedly involves subtracting the LSB). Again, if we want to compute the sum of $[1, j]$, we start at index $j$ in the Fenwick array, which stores the sum of the unique segment ending at $j$. If the node at index $j$ stores the segment $[i, j]$, we next need to find the unique node storing the segment ending at $i-1$. We can repeat this process, accumulating the segment sums along the way.

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig20.png" width="80%"><figcaption>Figure 20: Moving up the segment tree to find consecutive prefix segments.</figcaption></figure>

Taking inspiration from Figure 20, we see that what we want to do is find the left sibling of our nearest inactive parent, that is, we move up until we find the first ancestor that is a right child, then move to its left sibling. Under the binary indexing scheme, this can be implemented simply as:

![prev_segment_binary](moonbit/src//fenwick/segment_tree.mbt#:include)

[+](/blog/fenwick/thm/thm9.md#:embed)
