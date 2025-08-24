---
title: Auxiliary Operations - push_front and remove
collect: true
---

In the previous section, we implemented the core operations `get` and `put` for the LRU cache, but both rely on two critical auxiliary methods: `push_front` and `remove`. These two methods are responsible for maintaining the structure of the doubly linked list, forming the foundation for the proper functioning of the entire LRU algorithm.

**Implementation of push_front Method**

The `push_front` method inserts a node at the front of the linked list (i.e., the most recently used position):

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

Although this method contains only a few lines of logic, it requires careful understanding:

1. Point the new node's `next` to the original first node (i.e., `dummy.next`)
2. Point the new node's `pre` to the dummy node
3. Update the dummy node's `next` to point to the new node
4. Update the original first node's `pre` to point to the new node

These four steps complete the insertion of a new node at the head of the linked list. Note our use of `is Some` pattern matching to safely handle optional values—an elegant approach for null handling in MoonBit.

**Implementation of remove Method**

The `remove` method deletes a node from the linked list:

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

This implementation is straightforward:

1. Point the previous node's `next` to the next node of the target node
2. Point the next node's `pre` to the previous node of the target node

Through these two steps, the node is "disconnected" and no longer part of the linked list.

**Why Are These Operations So Critical?**

These seemingly simple operations are fundamental to the entire LRU cache algorithm:

- `push_front` ensures recently accessed items always reside at the front of the linked list
- `remove` serves two scenarios:
  1. Removing a node from its current position before reinserting it at the front (updating usage order)
  2. Evicting the least recently used node (when cache capacity is exceeded)

These basic operations maintain a doubly linked list sorted from "most recently used" to "least recently used," enabling the core functionality of the LRU cache.

**Details of Doubly Linked List Operations**

When manipulating doubly linked lists, common pitfalls include improper pointer handling that may cause list fragmentation or circular references. Our implementation avoids these issues:

- In `push_front`, we first set the new node's pointers before updating adjacent nodes
- In `remove`, we directly update adjacent nodes' pointers to bypass the target node

This approach ensures safe and correct linked list operations.

**Advantages of Using a Dummy Node**

Recall the dummy node in our design, which provides these benefits:

- Simplifies handling of empty lists
- Unifies insertion and deletion logic
- Provides stable reference points for "head" and "tail"

With these auxiliary operations, our LRU cache algorithm becomes more complete. Next, we'll add additional utility methods to enhance the usability of our LRU cache.
