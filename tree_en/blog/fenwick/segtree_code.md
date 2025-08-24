---
title: Simple segment tree implementation in MoonBit
collect: true
taxon: code
---

The following code shows a simple segment tree implementation in MoonBit, which uses some utility functions for handling index ranges, as shown in Figure 8. We store the segment tree as a recursive algebraic data type. We implement `update` and `rq` with code that directly corresponds to the recursive description in the previous section; then, `get` and `set` can also be implemented based on them. It is not difficult to generalize this code to a segment tree that stores values from any commutative monoid (if the `set` operation is not needed) or any abelian group (i.e., a commutative monoid with inverses, if the `set` operation is needed) — but for simplicity, we leave it as is, because such generalization does not add to our main story.

![seg_tree](moonbit/src//fenwick/segment_tree.mbt#:include)

Range utility functions:

![range](moonbit/src//fenwick/range.mbt#:include)
