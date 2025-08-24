---
title: 不可变外部迭代器和可变外部迭代器
collect: true
---

Immutable external iterators have no internal mutable state and can be iterated multiple times.

Mutable external iterators can only be iterated once. Although they cannot implement `uncons`, the process of iterating each element is still **divisible**.

After calling the `next` method, the internal state of the mutable external iterator changes, and it becomes the remaining iterator.
