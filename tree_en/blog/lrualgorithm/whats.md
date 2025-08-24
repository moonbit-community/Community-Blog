---
title: Introduction to LRU Cache
collect: true
---

Hello everyone! Today I'd like to share how to implement an LRU (Least Recently Used) cache algorithm using the MoonBit language. Whether you're new to MoonBit or want to understand the implementation details of the LRU algorithm, this article will guide you through this classic and practical algorithm.

**What is an LRU Cache?**

An LRU cache is a common cache eviction strategy based on a simple assumption: **recently accessed data is likely to be accessed again in the near future**. Therefore, when cache space is full and data needs to be evicted, the least recently accessed data should be prioritized for removal.

**A Real-Life Example**

Imagine your desk can only hold 5 books. Each time you need a new book but the desk is full, which book would you return to the bookshelf? The most reasonable choice is to put back the book you haven't touched for the longest time. This intuitively demonstrates the LRU strategy.

**Technical Applications**

LRU caches are widely used in computer systems:

- Operating system page replacement: When physical memory is insufficient, the system decides which pages to swap out to disk
- Database cache management: Databases cache frequently accessed data blocks in memory to improve read/write performance
- Web server caching: Caches popular resources like web pages and images to reduce server load
- Browser caching mechanisms: Stores recently visited web pages to speed up repeat access
- CDN content delivery networks: Adjusts content caching strategies based on access frequency

**A Practical Example of LRU Cache**

Suppose we have an LRU cache with capacity 3, initially empty. Now perform the following operations:

1. `put(1, "一")` → Cache state: [(1, "一")]
2. `put(2, "二")` → Cache state: [(2, "二"), (1, "一")]
3. `put(3, "三")` → Cache state: [(3, "三"), (2, "二"), (1, "一")]
4. `get(1)` → Returns "一", cache state: [(1, "一"), (3, "三"), (2, "二")] (note 1 moved to front)
5. `put(4, "四")` → Cache full, evict least recently used (2, "二"), cache state: [(4, "四"), (1, "一"), (3, "三")]
6. `get(2)` → Returns None (not found)

This example demonstrates how an LRU cache maintains "recently used" order and performs eviction when full.

**Core Operations of an LRU Cache**

A standard LRU cache must support two core operations:

1. **get(key)**: Retrieve the value associated with a key
   - If key exists, return the value and move the key-value pair to the "most recently used" position
   - If key doesn't exist, return a special value (e.g., None)

2. **put(key, value)**: Insert or update a key-value pair
   - If key exists, update the value and move the pair to the "most recently used" position
   - If key doesn't exist, create a new key-value pair and place it in the "most recently used" position
   - If cache is full, first evict the "least recently used" key-value pair before adding the new pair

Both operations should have O(1) time complexity, requiring careful data structure design.

**Why Do We Need a Special Data Structure?**

Implementing an efficient LRU cache faces two main challenges:

1. **Fast lookup**: We need O(1) time to determine if a key exists in the cache
2. **Order maintenance**: We need to track the usage order of cached items to identify the "least recently used"

Using only an array would require O(n) time for lookups; using only a hash table cannot track usage order. Therefore, we need to combine two data structures.

**Implementation Approach: Hash Table + Doubly Linked List**

The classic LRU cache implementation combines:

- **Hash table**: Provides O(1) lookup capability, mapping keys to nodes in the linked list
- **Doubly linked list**: Maintains access order with most recently used at the head and least recently used at the tail

This combination satisfies both fast lookup and order maintenance requirements.

Next, we'll implement this data structure step by step in MoonBit, starting from basic node definitions to complete LRU cache functionality.
