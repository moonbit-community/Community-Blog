---
title: LRU 缓存简介
collect: true
---

大家好！今天我想和大家分享如何用 MoonBit 语言实现一个 LRU（Least Recently Used，最近最少使用）缓存算法。无论你是刚接触 MoonBit，还是想了解 LRU 算法的实现细节，这篇文章都会带你深入了解这个经典而实用的算法。

**什么是 LRU 缓存？**

LRU 缓存是一种常见的缓存淘汰策略，它基于一个简单的假设：**最近访问过的数据在不久的将来很可能再次被访问**。因此，当缓存空间不足需要淘汰数据时，应该优先淘汰最长时间未被访问的数据。

**一个日常生活的例子**

想象你的书桌上只能放 5 本书。每次你需要一本新书，但书桌已满时，你会把哪本书放回书架？最合理的选择是把最久没看的那本书放回去。这就是 LRU 策略的直观体现。

**技术应用场景**

LRU 缓存在计算机系统中有广泛的应用：

- 操作系统的页面置换：当物理内存不足时，系统需要决定将哪些页面从内存换出到磁盘
- 数据库的缓存管理：数据库会在内存中缓存经常访问的数据块，提高读写性能
- Web 服务器的缓存：缓存热门的网页、图片等资源，减少服务器负载
- 浏览器的缓存机制：存储最近浏览的网页，加快重复访问的速度
- CDN 内容分发网络：根据访问频率调整内容缓存策略

**LRU 缓存的实际例子**

假设我们有一个容量为 3 的 LRU 缓存，初始为空。现在执行以下操作：

1. `put(1, "一")` → 缓存现状：[(1, "一")]
2. `put(2, "二")` → 缓存现状：[(2, "二"), (1, "一")]
3. `put(3, "三")` → 缓存现状：[(3, "三"), (2, "二"), (1, "一")]
4. `get(1)` → 返回 "一"，缓存现状：[(1, "一"), (3, "三"), (2, "二")] (注意 1 被移到了最前面)
5. `put(4, "四")` → 缓存已满，淘汰最久未使用的 (2, "二")，缓存现状：[(4, "四"), (1, "一"), (3, "三")]
6. `get(2)` → 返回 None (不存在)

通过这个例子，我们可以看到 LRU 缓存如何维护"最近使用"的顺序，以及如何在缓存满时进行淘汰。

**LRU 缓存的核心操作**

一个标准的 LRU 缓存需要支持以下两个核心操作：

1. **get(key)**: 获取缓存中键对应的值
   - 如果键存在，返回对应的值，并将该键值对移动到"最近使用"的位置
   - 如果键不存在，返回特殊值（如 None）

2. **put(key, value)**: 向缓存中插入或更新键值对
   - 如果键已存在，更新值，并将该键值对移动到"最近使用"的位置
   - 如果键不存在，创建新的键值对，放到"最近使用"的位置
   - 如果缓存已满，先删除"最久未使用"的键值对，再添加新的键值对

这两个操作的时间复杂度都应该是 O(1)，这就需要我们精心设计数据结构。

**为什么需要特殊的数据结构？**

实现一个高效的 LRU 缓存面临两个主要挑战：

1. **快速查找**：我们需要 O(1) 时间确定一个键是否存在于缓存中
2. **顺序维护**：我们需要跟踪所有缓存项的使用顺序，以便知道哪个是"最久未使用"的

如果只用数组，查找需要 O(n) 时间；如果只用哈希表，无法跟踪使用顺序。因此，我们需要结合两种数据结构。

**实现思路：哈希表 + 双向链表**

LRU 缓存的经典实现方式是结合使用：

- **哈希表**：提供 O(1) 的查找能力，键映射到链表中的节点
- **双向链表**：维护数据的访问顺序，最近使用的在链表头，最久未使用的在链表尾

这种组合让我们能够同时满足快速查找和顺序维护的需求。

接下来，我们将用 MoonBit 语言一步步实现这个数据结构，从基础的节点定义，到完整的 LRU 缓存功能。