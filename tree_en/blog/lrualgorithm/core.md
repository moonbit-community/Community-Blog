---
title: Core Operations - get and put
collect: true
---

Next, we will implement the two core operations of the LRU cache: `get` and `put`. These operations represent the essence of the LRU cache and are the most frequently used interfaces.

**get Method Implementation**

The `get` method retrieves the value associated with a key from the cache. If the key exists, it also moves the corresponding node to the "most recently used" position:

```moonbit
fn get[K : Hash + Eq, V](self : LRUCache[K, V], key : K) -> V? {
  let node = get_node(self, key)
  match node {
    Some(n) => Some(n.value)
    None => None
  }
}
```

This implementation appears simple, but it internally invokes the `get_node` method, which not only locates the node but also adjusts its position. Below is the implementation of `get_node`:

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

The `get_node` method performs several critical tasks:
1. Checks if the key exists in the hash table
2. If present, retrieves the corresponding node
3. Removes the node from its current position
4. Inserts the node at the front of the linked list (indicating most recently used)
5. Returns the found node

Here, we utilize two helper methods, `remove` and `push_front` (detailed later), which handle specific linked list operations.

**put Method Implementation**

The `put` method adds or updates a key-value pair in the cache:

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

The logic of the `put` method is divided into several parts:

1. **Check if the key exists**:
   - If present, directly update the value and adjust the position (via the `get_node` method)
   - Here, we only modify the value since `get_node` has already moved the node to the front of the linked list

2. **Create a new node**:
   - If the key doesn't exist, create a new node to store the key-value pair

3. **Add to the linked list and hash table**:
   - Insert the new node at the front of the linked list
   - Add a key-to-node mapping in the hash table

4. **Check capacity and possibly evict**:
   - If the cache size exceeds capacity, evict the least recently used item
   - The least recently used item is the node at the linked list tail (pointed to by `dummy.pre`)
   - Remove this node from both the hash table and linked list

**Core Idea of the LRU Algorithm**

Through these two methods, we observe the core principle of the LRU algorithm:
- Every time a key is accessed (via `get`) or updated (via `put`), it moves to the "most recently used" position
- When eviction is required, remove the key at the "least recently used" position

This design ensures we retain data most likely to be reaccessed while discarding the least probable data, maximizing cache hit rates.

In the next section, we'll detail the critical helper methods `push_front` and `remove`, which form the foundation of the LRU cache's linked list operations.
