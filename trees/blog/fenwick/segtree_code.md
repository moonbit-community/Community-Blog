---
title: Simple segment tree implementation in MoonBit
collect: true
---

下面代码展示了一个在 MoonBit 中实现的简单线段树，其中使用了一些处理索引范围的工具函数，如图 8 所示。我们将线段树存储为一个递归的代数数据类型。
并使用与前一节中递归描述直接对应的代码实现了 `update` 和 `rq`；随后，`get` 和 `set` 亦可基于它们来实现。将此代码推广至适用于存储来自任意交换幺半群（若不需要 `set` 操作）或任意阿贝尔群（即带逆元的交换幺半群，若需要 `set` 操作）的值的线段树亦非难事——但为简单起见，我们在此保持原状，因为这种推广对我们的主线故事并无增益。

![seg_tree](moonbit/src//fenwick/segment_tree.mbt:#include)

区间工具函数：

![range](moonbit/src//fenwick/range.mbt:#include)
