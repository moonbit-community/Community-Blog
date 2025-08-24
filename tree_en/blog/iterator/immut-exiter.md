---
title: Immutable External Iterator
collect: true
---

An immutable external iterator can return the first element and the remaining iteration process.

```moonbit
priv type ImmutExIter[A] () -> (A,ImmutExIter[A])?

fn ImmutExIter::uncons[A](self : ImmutExIter[A]) -> (A,ImmutExIter[A])? {
  (self._)()
}
```

Here we construct an immutable external iterator from `Array[A]`.

```moonbit
fn ImmutExIter::from_array[A](xs : Array[A]) -> ImmutExIter[A] {
  fn aux(i) -> (A,ImmutExIter[A])? {
    if (i < xs.length()) {
      Some((xs[i],fn () { aux(i + 1) } ) )
    } else {
      None
    }
  }
  fn () {
    aux(0)
  }
}
```

Testing the iteration process.

```moonbit
test "ImmutExIter::from_array" {
  let xs = [1,2,3,4,5]
  let iter = ImmutExIter::from_array(xs)

  let buf = StringBuilder::new()

  loop iter.uncons() {
    None => ()
    Some((x,xs)) => {
      buf.write_object(x)
      continue xs.uncons()
    }
  }
  inspect!(buf, content="12345")
}
```

[+](/blog/iterator/immut-exiter-tree.md#:embed)
