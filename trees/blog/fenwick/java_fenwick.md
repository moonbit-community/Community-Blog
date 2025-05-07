---
title: Implementing Fenwick trees with bit tricks in Java
collect: true
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

本节展示了一个典型的 Java 语言芬威克树实现。可见，其实现异常简洁，大体由若干小型循环构成，每个循环迭代仅执行少量的算术与位运算。然而，这段代码究竟在做什么、其工作原理为何，却不甚明了！稍加审视，`range`、`get` 和 `set` 函数尚属直观，但其余函数则令人困惑。我们可以观察到，`prefix` 和 `update` 函数均调用了另一个名为 `LSB` 的函数，该函数不知何故对一个整数及其负数执行了按位逻辑与运算。事实上，`LSB(x)` 计算的是 $x$ 的最低有效位（least significant bit），即它返回最小的 $2^k$，使得 $x$ 的第 $k$ 位为 1。然而，`LSB` 的实现原理，以及最低有效位在此处用于计算更新和前缀和的方式与缘由，均非显而易见。