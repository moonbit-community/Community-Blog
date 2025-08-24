---
title: Body
collect: true
---

Here, an immutable singly linked list is used as the stack. Each time an `ImmutExIter[A]` is returned, the entire iteration context must be saved.

- Mutable external iterators do not save the context and can only run once.
- Immutable external iterators can run multiple times but require additional storage for the iteration context.

```moonbit
typealias Stack[A] = @immut/list.T[A]

fn ImmutExIter::from_tree[A](root : Tree[A]) -> ImmutExIter[A] {

  fn aux(stack : Stack[_]) -> (A,ImmutExIter[A])? {
    match stack {
      Nil => None
      Cons(root,rest_stack) => { // pop root from stack
        match root {
          Nil => None
          Node(x,left,right) => {
            let stack = Stack::Cons(left,Stack::Cons(right,rest_stack))
            // push right into stack
            // push left into stack
            Some((x,fn () { aux(stack)}))
          }
        }
      }
    }
  }
  fn () {
    aux(@immut/list.singleton(root))
  }
}
```

Here we test the consistency between the immutable external iterator and preorder traversal.

```moonbit
test "ImmutExIter::from_tree" {
  let t2 = Tree::from_n(15)
  let iter = ImmutExIter::from_tree(t2)
  let b1 = StringBuilder::new()
  loop iter.uncons() {
    None => ()
    Some((x,rest)) => {
      b1.write_string("\{x},")
      continue rest.uncons()
    }
  }
  inspect!(b1, content="0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,")
  let b2 = StringBuilder::new()
  t2.preorder(fn(x) { b2.write_string("\{x},") })
  inspect!(b2, content="0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,")
}
```

Next, we implement `zipWith`. Here, it is no different from the ordinary `zipWith` for `List[A]`.

```moonbit
fn ImmutExIter::zipWith[A,B,C](self : ImmutExIter[A], other : ImmutExIter[B], f : (A,B) -> C) -> ImmutExIter[C] {
  let xs = self
  let ys = other

  match (xs.uncons(),ys.uncons()) {
    (Some((x,xs)),Some((y,ys))) => {
      fn () { Some((f(x,y),  ImmutExIter::zipWith(xs,ys,f)))}
    }
    (_,_) => {
      fn () { None }
    }
  }
}


test {
  let xs = ["apple", "orange", "watermetlon"]
  let ys = Tree::from_n(5)

  let xs = ImmutExIter::from_array(xs)
  let ys = ImmutExIter::from_tree(ys)

  let zs = xs.zipWith(ys,fn (x,y) { (x,y)})

  let b1 = StringBuilder::new()
  loop zs.uncons() {
    None => ()
    Some((x,rest)) => {
      b1.write_string("\{x},")
      continue rest.uncons()
    }
  }
  inspect!(b1, content=
    #|("apple", 0),("orange", 1),("watermetlon", 2),
  )
}
