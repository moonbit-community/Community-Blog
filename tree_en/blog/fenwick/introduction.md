---
title: Introduction
collect: true
---

Suppose we have a sequence of $n$ integers $a_1, a_2, \ldots, a_n$, and we wish to arbitrarily interleave the following two operations, as shown in Figure 1:

- Increase the value at any given index [^1] $i$ by some value $v$.
- Compute the sum of all values in any given interval $[i, j]$, i.e., $a_i + a_{i+1} + \cdots + a_j$. We call this operation a range query.

Note that the update operation is phrased as increasing the existing value by $v$; we can also set the value at a given index to a new value $v$ by increasing it by $v - u$ (where $u$ is the old value).

If we simply store the integers in a mutable array, update operations take constant time, but range queries require time linear in the size of the interval, as they must traverse the entire interval $[i, j]$ to accumulate the values.

To improve the runtime of range queries, we might try caching (at least some) interval sums. However, this must be done carefully because when updating a value at some index, the relevant cached sums must also be updated. For example, a straightforward approach is to use an array $P$ where $P_i$ stores the prefix sum $a_1 + \cdots + a_i$; $P$ can be precomputed in linear time with a single scan. Then, range queries become very fast: we can obtain $a_i + \cdots + a_j$ in constant time by computing $P_j - P_{i-1}$ (for convenience, we set $P_0 = 0$ so this works even when $i=1$). Unfortunately, update operations now require linear time, because changing $a_i$ necessitates updating $P_j$ for all $j \ge i$.

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig1.png" width="80%"><figcaption>Figure 1: Update and range query operations</figcaption></figure>

Is there a data structure that allows both operations to be performed in sublinear time? (You might pause to think before reading further!) This is not merely an academic question: it originally arose in the context of arithmetic coding (Rissanen & Langdon, 1979; Bird & Gibbons, 2002), a technique for converting messages into bit sequences for storage or transmission. To minimize the number of bits required, frequent characters are typically assigned shorter bit sequences and vice versa; this necessitates maintaining a dynamic frequency table of characters. Each time a new character is processed, we update this table; and to subdivide the unit interval into contiguous segments proportional to character frequencies, we need to query the table for cumulative frequencies (Ryabko, 1989; Fenwick, 1994).

So, can both operations be performed in sublinear time? The answer is yes. A simple trick is to partition the sequence into $\sqrt{n}$ buckets, each of size $\sqrt{n}$, and create an additional array of size $\sqrt{n}$ to cache the sum of each bucket. Updates still run in $O(1)$ time since we only update the value at the given index and the sum of its bucket. Range queries now take $O(\sqrt{n})$ time: to compute $a_i + \cdots + a_j$, we manually sum the values from $a_i$ to the end of its bucket and from the start of $a_j$'s bucket to $a_j$; for all buckets in between, we can directly look up their sums.

We can further speed up range queries by adding more layers of caching, at the cost of slightly increasing update overhead. For example, we can partition the sequence into $\sqrt[3]{n}$ "large buckets," each subdivided into $\sqrt[3]{n}$ "small buckets" containing $\sqrt[3]{n}$ values each. The sum of each bucket is cached; now each update modifies three values, and range queries run in $O(\sqrt[3]{n})$ time.

Continuing this way, we eventually arrive at a method for caching interval sums based on binary partitioning, where both update and range query operations run in [^2] $O(\log n)$ time. Specifically, we can build a complete binary tree [^3] whose leaves store the sequence itself, and each internal node stores the sum of its children. (This should be familiar to functional programmers; for example, finger trees (Hinze & Paterson, 2006; Apfelmus, 2009) use similar caching.) The resulting data structure is commonly called a segment tree, [^4] likely because each internal node ultimately caches the sum of a (contiguous) segment of the underlying sequence.

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig2.png" width="80%"><figcaption>Figure 2: Segment tree</figcaption></figure>

Figure 2 shows a segment tree built from an example array of length $n=16$ (for simplicity, we assume $n$ is a power of two, though generalizing to non-powers-of-two is straightforward). Each leaf corresponds to an element of the array; each internal node has a gray bar indicating the segment of the underlying array it represents.

Let's see how to implement the two operations using a segment tree, both in logarithmic time.

- To update the value at index $i$, we must also update all cached interval sums that include this value. These are precisely the nodes along the path from the leaf at index $i$ to the root; there are $O(\log n)$ such nodes. Figure 3 illustrates an update on the example segment tree from Figure 2; updating the entry at index 5 only requires modifying the shaded nodes along the path from the root to the updated entry.
- To perform a range query, we traverse the tree top-down while tracking the interval covered by the current node.
  - If the current node's interval is entirely contained within the query interval, return its value.
  - If the current node's interval does not overlap the query interval, return 0.
  - Otherwise, recursively query both children and return the sum of the results.

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig3.png" width="80%"><figcaption>Figure 3: Updating a segment tree</figcaption></figure>

Figure 4 illustrates computing the sum for interval $[4 \ldots 11]$. Blue nodes are those we traverse recursively; green nodes are those whose intervals are entirely contained within the query interval and return their values without further recursion; gray nodes do not overlap the query interval and return zero. The final result in this example is the sum of the green node values, $1 + 1 + 5 + (-2) = 5$ (which matches the actual sum of values in $[4 \ldots 11]$).

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig4.png" width="80%"><figcaption>Figure 4: Range query on a segment tree</figcaption></figure>

In this small example, it may seem we visit a large proportion of nodes, but in general, we visit no more than about $4 \log n$ nodes. Figure 5 makes this clearer. At most one blue node per level can have two blue children, so each level of the tree has at most two blue and two non-blue nodes. We essentially perform two binary searches: one for the left endpoint of the query interval and one for the right endpoint.

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig5.png" width="80%"><figcaption>Figure 5: Range query on a larger segment tree</figcaption></figure>

Segment trees are a fine solution: as we'll see in Section 2, they fit well with functional languages; they also generalize powerfully to support lazy propagation for range updates and persistence via sharing of immutable structures (Ivanov, 2011b).

**Fenwick trees**, or **Binary Indexed Trees** (Fenwick, 1994; Ivanov, 2011a), are another solution. They are less versatile but extremely memory-efficient—requiring almost no extra space beyond the array storing the values—and very fast to implement. In other words, they are ideal for applications like low-level encoding/decoding routines that don't need the advanced features of segment trees but demand peak performance.

[+](/blog/fenwick/java_fenwick.md#:embed)

Our goal is not to write elegant functional code for this solved problem. Instead, we aim to use a functional domain-specific language for bitstrings, combined with equational reasoning, to derive and explain the puzzling imperative code from first principles—demonstrating the power of functional thinking and equational reasoning even for understanding code written in other paradigms. After building intuition for segment trees (Section 2), we'll see how Fenwick trees can be viewed as a variant (Section 3). We'll then detour through two's complement representation, develop a suitable bit-manipulation DSL, and explain the implementation of the `LSB` function (Section 4). Using this DSL, we'll derive functions to convert between Fenwick trees and standard binary trees (Section 5). Finally, we'll derive functions to navigate within a Fenwick tree: convert to a binary tree index, perform the obvious operations to achieve the desired movement in the binary tree, then convert back. Fusing away the conversions via equational reasoning will reveal the underlying `LSB` function as expected (Section 6).

[^1]: Note that this and subsequent sections use 1-based indexing, where the first element of the sequence has index 1. The rationale for this choice will be explained later.
[^2]: In this article, $\log$ denotes base-2 logarithm; the original text uses $\lg$.
[^3]: The original text says *balanced binary tree*, but to avoid ambiguity, we use *complete binary tree* here.
[^4]: There is some confusion in terminology. As of this writing, the Wikipedia entry for segment trees (Wikipedia Contributors, 2024) discusses an interval data structure for computational geometry. However, most Google results for "segment tree" come from competitive programming, where it refers to the data structure described here (e.g., see Halim et al., 2020, Section 2.8 or Ivanov, 2011b). These two data structures are essentially unrelated.
