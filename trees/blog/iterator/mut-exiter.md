---
title: 可变外部迭代器
collect: true
---

可变外部迭代器，可以不断获取下一个元素的值，内部有一个可变的状态。

```moonbit 
priv type ExIter[A] () -> A?

fn ExIter::next[A](self : ExIter[A]) -> A? {
  (self._)()
}
```

```moonbit 
fn ExIter::from_array[A](xs : Array[A]) -> ExIter[A] {
  let mut i = 0 // i 是内部可变状态
  fn() {
    if i < xs.length() {
      let res = xs[i]
      i = i + 1
      Some(res)
    } else {
      None
    }
  }
}


test {
  let xs = [1, 2, 3, 4, 5]
  let iter = ExIter::from_array(xs)
  let mut sum = 0
  loop iter.next() {
    None => ()
    Some(x) => {
      sum += x
      continue iter.next()
    }
  }
  inspect!(sum, content="15")
}
```

`ExIter::from_tree` 是从 `Tree::Tree::preorder_stack` 改编而来，
`loop` 变成 `if` 迭代过程可以切分，而不是一个整体。

比如 `each` 和`eachi` 这样的内部迭代器的方法，只能一下子迭代全部元素

[- 读者可以再一次看外部迭代器的性质](/blog/iterator/internal-vs-external.md#:embed)


```moonbit 
fn ExIter::from_tree[A](root : Tree[A]) -> ExIter[A] {
  let stack = Array::new(capacity=4096) // stack 是内部可变状态
  stack.push(root)
  fn() {
    if not(stack.is_empty()) {
      let root = stack.unsafe_pop()
      match root {
        Nil => None
        Node(x, left, right) => {
          stack.push(right)
          stack.push(left)
          Some(x)
        }
      }
    } else {
      None
    }
  }
}
```


我们可以实现 `zipWith` 来同时迭代两个迭代器，
但是和不可变迭代器比，`ExIter`只能迭代一次，迭代后就使用完所有的元素。
这个和文件流的概念很相似。


```moonbit 
fn ExIter::zipWith[A,B,C](self : ExIter[A], other : ExIter[B], f : (A,B) -> C) -> ExIter[C] {
  let xs = self 
  let ys = other 
  fn () {
    match (xs.next(),ys.next() ) {
      (Some(x),Some(y)) => {
        Some(f(x,y))
      }
      (_,_) => None 
    }
  }
}

test "ExIter::zipWith" {
  let xs = ["apple", "orange", "watermetlon"]
  let ys = Tree::from_n(5)

  let xs = ExIter::from_array(xs)
  let ys = ExIter::from_tree(ys)

  let zs = xs.zipWith(ys,fn (x,y) { (x,y)})

  let b1 = StringBuilder::new()
  loop zs.next() {
    None => ()
    Some(x) => {
      b1.write_string("\{x},")
      continue zs.next()
    }
  }
  inspect!(b1, content=
    #|("apple", 0),("orange", 1),("watermetlon", 2),
  )
}

test "ExIter::from_tree" {
  let t2 = Tree::from_n(15)
  let iter = ExIter::from_tree(t2)
  let b1 = StringBuilder::new()
  loop iter.next() {
    None => ()
    Some(x) => {
      b1.write_string("\{x},")
      continue iter.next()
    }
  }
  inspect!(b1, content="0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,")
  let b2 = StringBuilder::new()
  t2.preorder(fn(x) { b2.write_string("\{x},") })
  inspect!(b2, content="0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,")
}
```