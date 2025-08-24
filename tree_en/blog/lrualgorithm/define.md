---
title: Defining Basic Data Structures
collect: true
---

Before implementing the LRU cache, we first need to define some basic data structures. As mentioned earlier, we'll combine a hash table and a doubly linked list to achieve an efficient LRU cache.

**Node Structure**

We start by defining the node structure for the doubly linked list. Each node needs to store a key-value pair and contain references to its previous and next nodes:

```moonbit
// Define Node struct for doubly linked list
struct Node[K, V] {
  key : K
  mut value : V
  mut pre : Node[K, V]?  // Previous node
  mut next : Node[K, V]? // Next node
}

// Node constructor
fn new_node[K, V](k : K, v : V) -> Node[K, V] {
  { key: k, value: v, pre: None, next: None }
}
```

Several interesting MoonBit features in this node structure deserve attention:

- **Generic parameters** `[K, V]`: This allows our LRU cache to work with any key and value types, providing great flexibility.

- **Mutable fields** `mut`: The `value`, `pre`, and `next` fields are marked as `mut`, meaning they can be modified after creation. This is essential for our LRU cache which requires frequent adjustments to the linked list structure.

- **Optional types** `?`: The `pre` and `next` fields are optional types, indicating they might be `None`. This provides natural handling for nodes at both ends of the linked list.

- **Simple constructor**: The `new_node` function helps create a new node where both predecessor and successor are initialized to `None`.

**LRU Cache Structure**

Next, we define the main structure for the LRU cache:

```moonbit
// LRU cache struct
struct LRUCache[K, V] {
  capacity : Int // Capacity
  dummy : Node[K, V] // Sentinel node for marking head and tail of doubly linked list
  key_to_node : Map[K, Node[K, V]] // Mapping from key to node
}
```

This structure contains three critical fields:

- **capacity**: Defines the maximum number of key-value pairs the cache can store.

- **dummy**: A special sentinel node that doesn't store actual key-value pairs, used to simplify linked list operations. Using a sentinel node is a common programming technique that helps avoid handling edge cases for empty lists and boundary conditions.

- **key_to_node**: A mapping from keys to nodes, enabling O(1) lookup time to find the corresponding node by key.

**Why Use a Sentinel Node?**

The use of a sentinel node is an elegant design choice. We'll implement a circular structure where the sentinel node simultaneously serves as both the "head" and "tail" of the linked list:

- `dummy.next` points to the most recently used node (the actual first node)
- `dummy.pre` points to the least recently used node (the actual last node)

This design ensures uniform and clear code logic when handling node insertions and deletions, eliminating special cases for empty lists.

With these two fundamental data structures, we've laid the groundwork for implementing an efficient LRU cache. In the next section, we'll implement the LRU cache constructor and core operations.
```
