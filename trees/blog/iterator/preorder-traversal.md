---
title: MoonBit 实现树的先序遍历
collect: true
author: [illusory0x0](https://github.com/illusory0x0)
taxon: Blog
date: 2025-04-07
---


二叉树的定义

```moonbit
priv enum Tree[A] {
  Nil
  Node(A, Tree[A], Tree[A])
}
```

先序遍历一棵树

```moonbit
fn Tree::preorder[A](self : Tree[A], f : (A) -> Unit) -> Unit {
  fn dfs(root) {
    match root {
      Nil => ()
      Node(x, left, right) => {
        f(x)
        dfs(left)
        dfs(right)
      }
    }
  }

  dfs(self)
}
```

我们把 `Tree::preorder` 改写为手动控制栈的过程 `Tree::preorder_stack`

```moonbit
fn Tree::preorder_stack[A](self : Tree[A], f : (A) -> Unit) -> Unit {
  let stack = Array::new(capacity=4096)
  stack.push(self)
  while not(stack.is_empty()) {
    let root = stack.unsafe_pop()
    match root {
      Nil => ()
      Node(x, left, right) => {
        f(x)
        stack.push(right) // 先进后出， 先被压入后处理
        stack.push(left) // 先处理左节点
      }
    }
  }
}
```

下面的部分是用来测试**系统栈**版本和**手动控制栈**版本的一致性。


```moonbit 
fn Tree::from_n(n : Int) -> Tree[Int] {
  let mut i = 0
  fn dfs() {
    if i < n {
      let x = i
      i += 1
      let res = Node(x, dfs(), dfs())
      res
    } else {
      Nil
    }
  }

  dfs()
}

fn test_preorder(root : Tree[Int]) -> Unit! {
  let b1 = StringBuilder::new()
  let b2 = StringBuilder::new()
  root.preorder(fn(x) { b1.write_object(x) })
  root.preorder_stack(fn(x) { b2.write_object(x) })
  assert_eq!(b1.to_string(), b2.to_string())
}

test "preorder/preorder_stack" {
  let t1 = Node(
    1,
    Node(2, Nil, Nil),
    Node(3, Node(4, Nil, Nil), Node(5, Nil, Nil)),
  )
  let mut sum = 0
  t1.preorder(fn(x) { sum += x })
  inspect!(sum, content="15")
  let t2 = Tree::from_n(15)
  test_preorder!(t2)
}
```