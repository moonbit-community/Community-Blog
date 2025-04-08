---
title: Traverse a Tree
collect: true
---

通过前文的讨论，读者应对去函数化的核心思想建立了基本认知。
本节将运用该技术解决更具挑战性的问题——二叉树遍历优化。首先给出二叉树的规范定义：

```moonbit
enum Tree[T] {
  Leaf(T)
  Node(T, Tree[T], Tree[T])
}
```

考虑基础的前序遍历实现：

```moonbit
fn pre_order[T : Show](tree : Tree[T], f : (T) -> Unit) -> Unit {
  match tree {
    Leaf(x) => f(x)
    Node(x, left, right) => {
      f(x)
      pre_order(left, f)
      pre_order(right, f)
    }
  }
}
```

在该函数的设计实现中，我们采用递归算法对树形数据结构进行系统性遍历，
这种方法虽能确保每个节点都受到函数 `f` 的精确，
且严格遵循前序遍历（pre-order traversal）的既定顺序，但其递归范式存在显著的效率瓶颈。
具体而言，由于该递归过程并非尾递归（tail recursion）的优化形态，
导致现代编译器的尾调用优化（TCO）机制无法将其自动转换为等价的迭代形式，
这种特性必然造成调用栈的持续累积，进而影响程序的执行效能。
有鉴于此，我们亟需运用前文阐述的「去函数化」（defunctionalization）这一程序变换技术来突破此局限。

