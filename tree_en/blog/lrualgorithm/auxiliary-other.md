---
title: Practical Auxiliary Methods
collect: true
---

We've implemented the core functionality of the LRU cache, including the basic data structure, constructor, core operations `get`/`put`, and linked list helper methods. To make our LRU cache more complete and user-friendly, let's now add some practical auxiliary methods.

**Getting Cache Size**

First, we implement a method to get the current number of elements in the cache:

```moonbit
fn size[K, V](self : LRUCache[K, V]) -> Int {
  self.key_to_node.size()
}
```

This method is straightforward—it directly returns the size of the hash table since each entry corresponds to one element in the cache.

**Checking If Cache Is Empty**

Next, we add a method to check whether the cache is empty:

```moonbit
fn is_empty[K, V](self : LRUCache[K, V]) -> Bool {
  self.key_to_node.size() == 0
}
```

This method checks if the hash table is empty to determine whether the entire cache contains no elements.

**Checking Key Existence**

Finally, we implement a method to check if a specific key exists in the cache:

```moonbit
fn contains[K : Hash + Eq, V](self : LRUCache[K, V], key : K) -> Bool {
  self.key_to_node.contains(key)
}
```

This method directly utilizes the hash table's `contains` method to quickly determine key presence.

**Significance of These Auxiliary Methods**

Although these methods appear simple, they provide substantial value for practical LRU cache usage:

- **Improved Readability**: Using `is_empty()` is more intuitive than `size() == 0`
- **Encapsulation of Implementation Details**: Users don't need to know about the internal `key_to_node` hash table
- **Interface Completeness**: Offers a comprehensive API to accommodate various usage scenarios

These helper methods embody good API design principles—simple, consistent, and easy to use. By providing them, our LRU cache implementation becomes more robust and user-friendly.

**Practical Usage Examples**

These auxiliary methods are highly useful in real-world applications, for example:

```moonbit
// Check key existence without retrieving value (avoids altering usage order)
if contains(cache, "key") {
  // Key exists, perform operations
}

// Execute specific logic when cache is empty
if is_empty(cache) {
  // Cache is empty, perform initialization or other operations
}

// Calculate cache utilization
let usage_percentage = size(cache) * 100 / cache.capacity
```

Though simple, these methods significantly enhance the LRU cache's practicality. With these auxiliary methods, our LRU cache implementation is now comprehensive and ready for real-world use.
