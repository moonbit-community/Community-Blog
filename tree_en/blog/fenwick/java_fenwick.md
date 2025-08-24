---
title: Implementing Fenwick trees with bit tricks in Java
collect: true
taxon: code
---

```java
class FenwickTree {
    private long[] a;
    public FenwickTree(int n) { a = new long[n+1]; }
    public long prefix(int i) {
        long s = 0;
        for (; i > 0; i -= LSB(i)) s += a[i]; return s;
    }
    public void update(int i, long delta) {
        for (; i < a.length; i += LSB(i)) a[i] += delta;
    }
    public long range(int i, int j) {
        return prefix(j) - prefix(i-1);
    }
    public long get(int i) { return range(i,i); }
    public void set(int i, long v) { update(i, v - get(i)); }
    private int LSB(int i) { return i & (-i); }
}
```

This section presents a typical Java implementation of a Fenwick tree. As evident, the implementation is exceptionally concise, primarily consisting of several small loops where each iteration executes only a few arithmetic and bitwise operations. However, what exactly this code accomplishes and how it works remains unclear! Upon closer inspection, the `range`, `get`, and `set` functions appear relatively intuitive, but the remaining functions are perplexing. We observe that both the `prefix` and `update` functions invoke another function named `LSB`, which somehow performs a bitwise AND operation between an integer and its negative counterpart. In reality, `LSB(x)` calculates the least significant bit (LSB) of $x$, meaning it returns the smallest $2^k$ such that the $k$-th bit of $x$ is 1. Nevertheless, the underlying principle of `LSB`'s implementation, along with how and why the least significant bit is utilized here for computing updates and prefix sums, is non-obvious.
