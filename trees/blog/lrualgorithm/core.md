---
title: 核心操作 - get 和 put
collect: true
---

接下来我们要实现 LRU 缓存的两个核心操作：`get` 和 `put`。这两个操作是 LRU 缓存的精髓所在，也是最常用的接口。

**get 方法实现**

`get` 方法用于从缓存中获取某个键对应的值。如果键存在，它还需要将对应的节点移到"最近使用"的位置：

```moonbit
fn get[K : Hash + Eq, V](self : LRUCache[K, V], key : K) -> V? {
  let node = get_node(self, key)
  match node {
    Some(n) => Some(n.value)
    None => None
  }
}
```

这个实现看起来很简单，但它内部调用了 `get_node` 方法，这个方法不仅查找节点，还负责调整节点位置。下面是 `get_node` 的实现：

```moonbit
fn get_node[K : Hash + Eq, V](self : LRUCache[K, V], key : K) -> Node[K, V]? {
  if self.key_to_node.contains(key) {
    if self.key_to_node.get(key) is Some(node) {
      // 将节点移到链表前端
      remove(self, node)
      push_front(self, node)
      return Some(node)
    }
  }
  None
}
```

`get_node` 方法做了几件重要的事：
1. 检查键是否存在于哈希表中
2. 如果存在，获取对应的节点
3. 将节点从当前位置移除
4. 将节点插入到链表前端（表示最近使用）
5. 返回找到的节点

这里我们用到了两个辅助方法 `remove` 和 `push_front`（后面会详细介绍），它们负责链表的具体操作。

**put 方法实现**

`put` 方法用于向缓存中添加或更新键值对：

```moonbit
fn put[K : Hash + Eq, V](self : LRUCache[K, V], key : K, value : V) -> Unit {
  // 如果键已存在，更新值并移到链表前端
  let existing = get_node(self, key)
  if existing is Some(node) {
    node.value = value
    return
  }

  // 创建新节点
  let node = new_node(key, value)

  // 将新节点加入链表前端
  push_front(self, node)
  self.key_to_node.set(key, node)

  // 如果超出容量，删除最久未使用的节点
  if self.key_to_node.size() > self.capacity {
    if self.dummy.pre is Some(last_node) {
      self.key_to_node.remove(last_node.key)
      remove(self, last_node)
    }
  }
}
```

`put` 方法的逻辑分为几个部分：

1. **检查键是否已存在**：
   - 如果存在，直接更新值并调整位置（通过前面的 `get_node` 方法）
   - 这里我们只需要修改值，因为 `get_node` 已经将节点移到了链表前端

2. **创建新节点**：
   - 如果键不存在，则创建一个新的节点存储键值对

3. **添加到链表和哈希表**：
   - 将新节点插入到链表前端
   - 在哈希表中添加键到节点的映射

4. **检查容量并可能淘汰**：
   - 如果缓存大小超过了容量，需要淘汰最久未使用的项
   - 最久未使用的项就是链表尾部（`dummy.pre`）指向的节点
   - 从哈希表和链表中都删除这个节点

**LRU 算法的核心思想**

通过这两个方法，我们可以看到 LRU 算法的核心思想：
- 每次访问（get）或更新（put）一个键，都将它移到"最近使用"位置
- 当需要淘汰时，移除"最久未使用"位置的键

这种设计确保了我们总是保留最有可能再次被访问的数据，而丢弃最不可能再次被访问的数据，从而最大化缓存的命中率。

在下一部分，我们将详细介绍 `push_front` 和 `remove` 这两个关键的辅助方法，它们是实现 LRU 缓存链表操作的基础。