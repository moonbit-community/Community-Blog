---
title: Index conversion
collect: true
---

Before deriving our index conversion functions, we must address a slightly awkward fact. In the traditional binary tree indexing scheme, as shown in Figure 9, the root node has index 1, each left child has twice its parent's index, and each right child has twice its parent's index plus one. Recall that in a pruned segment tree, the root and every left child are active, while all right children are inactive. This makes the root an awkward special case—all active nodes have even indices except the root at index 1. This complicates checking whether we're at an active node—simply examining the least significant bit is insufficient.

A simple solution is to assign the root index 2 directly, then continue labeling the remaining nodes with the same scheme—each left child is twice its parent, and each right child is twice its parent plus one. This results in the indexing shown in Figure 14, as if we took the left subtree of a tree rooted at 1 and ignored the right subtree. Of course, this means approximately half the possible indices are omitted—but this isn't problematic since we'll only use these indices as intermediate steps that will eventually be fused away.

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig14.png" width="80%"><figcaption>Figure 14. Binary tree indexing rooted at 2.</figcaption></figure>

Figure 15 shows a binary tree with nodes numbered in two different ways: the left side of each node displays its binary tree index (with root index 2). The right side displays its Fenwick array index if it has one (inactive nodes are simply grayed out on the right). The table below shows the mapping from Fenwick array indices (top row) to binary tree indices (bottom row). As a larger example, Figure 16 shows the same on a binary tree one level deeper.

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig15.png" width="80%"><figcaption>Figure 15: Binary tree labeled with binary tree indices and Fenwick indices.</figcaption></figure>

<figure><img src="https://static.cambridge.org/binary/version/id/urn:cambridge.org:id:binary:20250116174732089-0720:S0956796824000169:S0956796824000169_fig16.png" width="80%"><figcaption>Figure 16. Deeper binary tree labeled with binary tree indices and Fenwick indices.</figcaption></figure>

Our goal is to find a method to compute the binary tree index corresponding to a given Fenwick index, and vice versa. Examining the table in Figure 16 closely, a pattern stands out. First, all numbers in the bottom row are even, precisely because the binary tree numbering ensures all active nodes have even indices. Second, we see the even numbers $32, 34 \ldots 46$ appearing sequentially in all odd positions. These are exactly the leaf nodes of the tree; indeed, every other node in the Fenwick array comes from the original tree's leaves. Alternating with them, in the even positions, are the numbers $16, 8, 18, 4, \ldots$, which correspond to all non-leaf nodes; but these are exactly the sequence of binary tree indices from the bottom row of Figure 15's table—because the internal nodes in a tree of height 4 themselves form a tree of height 3, with nodes appearing in the same order.

[+](/blog/fenwick/interleaving.md#:embed)

These observations lead to the recurrence relation shown in 5.1 for computing the sequence $b_n$ of binary tree indices for nodes stored in a Fenwick array of length $2^n$: $b_0$ is the singleton sequence $[2]$, otherwise $b_n$ is the result of interleaving the even numbers $2^{n+1}, 2^{n+1} + 2, \ldots, 2^{n+1} + 2^n - 2$ with $b_{n-1}$ (Translator's note: code implementations use bitwise operations instead of exponentiation, and in mathematical reasoning, `interleave` is denoted as the infix operator $\curlyvee$).

We can verify that this indeed reproduces the observed sequence for $n=4$:

![b4](moonbit/src//fenwick/segment_tree.mbt#:include)

Let $s ! k$ denote the $k$-th item in list $s$ (counting from 1), written as `s.nth(k)` in code (Translator's note: this differs from MoonBit standard library's `nth`, which uses 0-based indexing). The following code illustrates two simple lemmas about the interaction of indexing and interleaving: $(xs \curlyvee ys) ! (2 \cdot j) = ys ! j$ and $(xs \curlyvee ys) ! (2 \cdot j - 1) = xs ! j$ (provided $xs$ and $ys$ have equal length).

```moonbit
// suppose xs.length() == ys.length()
interleave(xs, ys).nth(2 * j) == ys.nth(j)
interleave(xs, ys).nth(2 * j + 1) == xs.nth(j)
```

With these preparations, we define the Fenwick-to-binary index conversion function as
$$ \text{f2b}(n, k) = b_n ! k. $$

Of course, since $b_n$ has length $2^n$, this function is only defined for $k$ in $[1, 2^n]$.

We can now simplify the definition of `f2b` as follows. First, for even inputs:

$$
\begin{align*}
& \text{f2b}(n, (2 \cdot j)) \\
= & b_n ! (2 \cdot j) & \{ \text{f2b} \} \\
= & (\text{interleave}(\text{map}((2 \cdot), [2^n \ldots 2^n + 2^{n-1} - 1]), b_{n-1})) ! (2 \cdot j) & \{ \text{b} \} \\
= & b_{n-1} ! j & \{ \text{interleave-!} \text{ lemma } \} \\
= & \text{f2b}((n - 1), j). & \{ \text{f2b} \}
\end{align*}
$$

Here $(2\cdot)$ is shorthand for the function `fn { x => 2 * x }`, and $[2^n \ldots 2^n + 2^{n-1} - 1]$ is the list for the closed interval $[2^n, 2^n + 2^{n-1} - 1]$. For odd inputs:

$$
\begin{align*}
& \text{f2b}(n, (2 \cdot j - 1)) \\
= & b_n ! (2 \cdot j - 1) & \{ \text{f2b} \} \\
= & (\text{interleave}(\text{map}((2 \cdot), [2^n \ldots 2^n + 2^{n-1} - 1]), b_{n-1})) ! (2 \cdot j - 1) & \{ \text{b} \} \\
= & \text{map}((2 \cdot), [2^n \ldots 2^n + 2^{n-1} - 1]) ! j & \{ \text{interleave-!} \text{ lemma } \} \\
= & 2 \cdot (2^n + j - 1) & \{ \text{map, algebra} \} \\
= & 2^{n+1} + 2j - 2 & \{ \text{algebra} \}
\end{align*}
$$

Thus, we have

$$
\text{f2b}(n, k) =
\begin{cases}
\text{f2b}(n - 1,k / 2) & k \text{ even} \\
2^{n+1} + k - 1 & k \text{ odd}
\end{cases}
$$

Note that when $n = 0$, we must have $k = 1$, so $\text{f2b}(0, 1) = 2^{0+1} + 1 - 1 = 2$ (Translator's note: the original text stated *f2b 0 1 = $2^{0+1} + 1 - 1 = 1$*, but the calculation should yield 2 to match our new root assumption). This definition is valid for all $n \ge 0$. Now uniquely decompose $k$ as $2^a \cdot b$ where $b$ is odd. By induction we see:

$$ \text{f2b} (n, 2^a \cdot b) = \text{f2b}(n - a, b) = 2^{(n-a)+1} + b - 1. $$

In other words, computing `f2b` involves repeatedly dividing by 2 (i.e., right-shifting) as long as the input is even, then finally subtracting 1 and adding a power of two. However, knowing which power of two to add depends on how many times we shifted. A better way to think about it is to add $2^{n+1}$ at the beginning and let it shift along with all other bits. (Translator's note: the original explanation was unclear; here's a clarification: to solve $X = 2^{n-a+1} + b$, we can multiply by a factor $2^a$ to get $2^a X = 2^{n+1} + 2^ab$. The right side contains $k = 2^a \cdot b$, the function's argument. Thus $X = \dfrac{2^{n+1} + 2^a \cdot b}{2^a}$, where division can be implemented via bit shifting.) Therefore, we obtain the final definition of `f2b` using our `Bits` DSL. Defining the `shift` function separately will make some proofs more concise.

![shift](moonbit/src//fenwick/segment_tree.mbt#:include)

It's easily verified with QuickCheck that this produces identical results to the original `f2b(4, k)` for $k$ in $[1, 2^4]$.

Now we turn to deriving `b2f(n, _)`, which converts back from binary tree indices to Fenwick indices. `b2f(n, _)` should be the left inverse of `f2b(n, _)`, meaning for any $k \in [1, 2^n]$, we should have $\text{b2f}(n, \text{f2b}(n, k)) = k$.
If $k$ is an input to `f2b`, we have $k = 2^a \cdot b \le 2^n$, so $b-1 \lt 2^{n-a}$. Given the output $\text{f2b}(n, k) = m = 2^{n-a+1} + b - 1$,
the highest bit of $m$ is $2^{n-a+1}$, and the remaining bits represent $b - 1$. Therefore, generally, given some $m$ that is an output of `f2b(n, _)`, we can uniquely write it as $m = 2^c + d$ where $d \lt 2^{c-1}$; then

$$ \text{b2f} (n, 2^c + d) = 2^{n-c+1} \cdot (d + 1). $$

In other words, given input $2^c + d$, we subtract the highest bit $2^c$, add 1, then left-shift $n - c + 1$ times. Again, there's a simpler method: we can first add 1 (note that since $d \lt 2^{c-1}$, adding 1 won't interfere with the bit at $2^c$), then left-shift enough times to move the leftmost bit to position $n + 1$, and finally remove it. That is:

![unshift](moonbit/src//fenwick/segment_tree.mbt#:include)

Verification:

![test_id](moonbit/src//fenwick/segment_tree.mbt#:include)
```
