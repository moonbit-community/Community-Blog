---
title: Mutable External Iterator
collect: true
---

A mutable external iterator can continuously retrieve the next element's value and maintains an internal mutable state.

```moonbit
priv type ExIter[A] () -> A?

fn ExIter::next[A](self : ExIter[A]) -> A? {
  (self._)()
}
```

```moonbit
fn ExIter::from_array[A](xs : Array[A]) -> ExIter[A] {
  let mut i = 0 // i is internal mutable state
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

`ExIter::from_tree` is adapted from `Tree::Tree::preorder_stack`,
where `loop` becomes `if` to enable segmented iteration rather than a monolithic process.

For example, internal iterator methods like `each` and `eachi` can only iterate through all elements at once.

[- Readers can review the properties of external iterators again](/blog/iterator/internal-vs-external.md#:embed)

```moonbit
fn ExIter::from_tree[A](root : Tree[A]) -> ExIter[A] {
  let stack = Array::new(capacity=4096) // stack is internal mutable state
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

We can implement `zipWith` to iterate two iterators simultaneously,
but unlike immutable iterators, `ExIter` can only be iterated once—elements are exhausted after iteration.
This behavior resembles file stream concepts.

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
