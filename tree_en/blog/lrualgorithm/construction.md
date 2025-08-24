---
title: Constructor Implementation
collect: true
---

Now that we've defined the basic data structure, we need to implement the constructor for the LRU cache. The constructor serves as the starting point for any data structure, responsible for properly initializing its internal state.

**Constructor Design**

When designing the LRU cache constructor, we need to consider:

- Initializing the maximum cache capacity
- Creating and setting up the dummy node
- Initializing an empty key-value mapping table

Let's see how to implement this constructor in MoonBit:

```moonbit
fn new[K : Hash + Eq, V](
  capacity : Int,
  default_k : K,
  default_v : V
) -> LRUCache[K, V] {
  // Create a dummy node using the provided default values
  let dummy = new_node(default_k, default_v)

  // Initialize the dummy node to point to itself, forming a ring
  dummy.next = Some(dummy)
  dummy.pre = Some(dummy)
  { capacity, dummy, key_to_node: Map::new() }
}
```

This code accomplishes several important tasks:

- **Generic Constraints**: Note the `K : Hash + Eq` constraint, indicating that our key type must support hashing and equality comparison. This is necessary because we'll use keys to create hash maps, requiring keys to be hashable and comparable.

- **Default Value Parameters**: We require `default_k` and `default_v` to initialize the dummy node. This is mandated by MoonBit's type system—even though the dummy node doesn't store actual data, we must provide valid values for it.

- **Self-Referential Ring**: We set the dummy node's `next` and `pre` to point to itself, creating an empty circular linked list. This clever technique ensures we avoid null pointer issues when the list is empty.

- **Returning Structure Instance**: Uses MoonBit's struct literal syntax `{ capacity, dummy, key_to_node: Map::new() }` to create and return an LRUCache instance.

**Why Form a Circular Structure?**

You may notice we set the dummy node's predecessor and successor to point to itself, forming a ring. This design offers several advantages:

- Eliminates edge cases for empty lists
- Uses identical logic for inserting the first node and subsequent nodes
- Uses identical logic for deleting the last node and other nodes

In an empty list, the dummy node serves as both the "head" and "tail". When we add actual nodes, they're inserted into this ring while the dummy node remains fixed, helping us locate the logical start and end of the list.

**Diagram Explanation**

Initial state of the linked list structure:

```
dummy ⟷ dummy (pointing to itself)
```

After adding node A:

```
dummy ⟷ A ⟷ dummy
```

After adding another node B (placed at the most recently used position):

```
dummy ⟷ B ⟷ A ⟷ dummy
```

In this structure, `dummy.next` points to the most recently used node (B), while `dummy.pre` points to the least recently used node (A).

This design lays the foundation for implementing core operations like `get` and `put`. Next, we'll implement these core operations to complete the LRU cache functionality.
