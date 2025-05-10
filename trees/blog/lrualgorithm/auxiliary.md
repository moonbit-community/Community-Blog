---
title: 辅助操作 - push_front 和 remove
collect: true
---

在上一部分中，我们实现了 LRU 缓存的核心操作 `get` 和 `put`，但它们都依赖于两个关键的辅助方法：`push_front` 和 `remove`。这两个方法负责维护双向链表的结构，是整个 LRU 算法能够正常工作的基础。

**push_front 方法实现**

`push_front` 方法用于将一个节点插入到链表的最前端（即最近使用的位置）：

```moonbit
fn push_front[K, V](self : LRUCache[K, V], node : Node[K, V]) -> Unit {
  node.next = self.dummy.next
  node.pre = Some(self.dummy)
  if node.pre is Some(pre) {
    pre.next = Some(node)
  }
  if node.next is Some(next) {
    next.pre = Some(node)
  }
}
```

这个方法的逻辑虽然只有几行，但需要仔细理解：

1. 将新节点的 `next` 指向原来的第一个节点（即 `dummy.next`）
2. 将新节点的 `pre` 指向哑元节点
3. 更新哑元节点的 `next` 指向新节点
4. 更新原第一个节点的 `pre` 指向新节点

通过这四步，我们完成了在链表头部插入新节点的操作。注意我们使用了 `is Some` 模式匹配来安全地处理可选值，这是 MoonBit 处理空值的一种优雅方式。

**remove 方法实现**

`remove` 方法用于从链表中删除一个节点：

```moonbit
fn remove[K, V](self : LRUCache[K, V], node : Node[K, V]) -> Unit {
  if node.pre is Some(pre) {
    pre.next = node.next
  }
  if node.next is Some(next) {
    next.pre = node.pre
  }
}
```

这个方法的实现非常直观：

1. 将节点的前一个节点的 `next` 指向节点的下一个节点
2. 将节点的下一个节点的 `pre` 指向节点的前一个节点

通过这两步，节点就从链表中"断开"了，不再是链表的一部分。

**为什么这两个操作如此重要？**

这两个看似简单的操作是整个 LRU 缓存算法的关键：

- `push_front` 确保最近访问的项总是位于链表的前端
- `remove` 用于两个场景：
  1. 将节点从当前位置移除，然后重新插入到链表前端（更新使用顺序）
  2. 淘汰最久未使用的节点（当缓存超出容量时）

通过这两个基本操作，我们能够维护一个按照"最近使用"到"最久未使用"排序的双向链表，从而实现 LRU 缓存的核心功能。

**双向链表操作的细节**

在处理双向链表时，容易出现的错误是指针操作顺序不当导致链表断裂或形成环。我们的实现避免了这些问题：

- 在 `push_front` 中，我们先设置新节点的指针，再更新相邻节点的指针
- 在 `remove` 中，我们直接更新相邻节点的指针，跳过要删除的节点

这种实现方式确保了链表操作的安全性和正确性。

**使用哑元节点的优势**

回顾一下我们设计中使用的哑元节点（dummy node），它带来了以下优势：

- 简化了链表为空的处理
- 统一了节点插入和删除的逻辑
- 提供了稳定的"头"和"尾"引用点

有了这些辅助操作，我们的 LRU 缓存算法就更加完整了。接下来，我们会添加一些额外的实用方法，让我们的 LRU 缓存更加易用。