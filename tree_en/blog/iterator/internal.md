---
title: Implementing Internal Iterators in MoonBit
collect: true
author: [illusory0x0](https://github.com/illusory0x0)
taxon: Blog
date: 2025-04-08
---

The internal iterator implementation in this article references [OCaml iter](https://github.com/c-cube/iter).

```moonbit
priv type InIter[A] ((A) -> Unit) -> Unit

fn InIter::run[A](self : InIter[A], f : (A) -> Unit) -> Unit {
  (self._)(f)
}
```

Here, `InIter::from_array` corresponds to currying in OCaml.

```moonbit
fn InIter::from_array[A](xs : Array[A]) -> InIter[A] {
  fn(k) { xs.each(k) }
}
```

`with_index` is a decorator that modifies the default behavior of `iter`.

```moonbit
fn InIter::with_index[A](self : InIter[A]) -> InIter[(Int, A)] {
  let mut i = 0
  fn(k) {
    self.run(fn(x) {
      k((i, x))
      i += 1
    })
  }
}
```

```moonbit
impl[A : Show] Show for InIter[A] with output(self, logger) {
  logger.write_string("[")
  self.run(fn(x) {
    logger.write_object(x)
    logger.write_string(",")
  })
  logger.write_string("]")
}

test {
  let xs = ["apple", "orange", "strawberry"]
  let iter = InIter::from_array(xs).with_index()

  inspect!(iter.to_string(), content=#|[(0, "apple"),(1, "orange"),(2, "strawberry"),]
  )
}
```

To stop iteration mid-loop, MoonBit introduces `IterResult`.

The callback function `yield : (A) -> IterResult` controls whether to stop or continue the loop.

```moonbit
type InIter[A] ((A) -> Unit) -> Unit
type Iter[A] ((A) -> IterResult) -> IterResult
```

Comparing the definitions of `Iter[A]` and `InIter[A]`:

After replacing `Unit` with `IterResult`, it aligns with MoonBit's built-in internal iterator definition.  
`InIter[A]` returns `Unit` and its callback returns `Unit`, equivalent to always returning `IterResult::IterContinue`.

Methods like `Iter::take`, `Iter::drop`, and `Iter::flat_map` in MoonBit's standard library are decorators that modify the original `iter`'s behavior.

Consider `core`'s `Iter::take` implementation to understand how `yield_` controls loop state:

```moonbit
// ref: https://github.com/moonbitlang/core/blob/main/builtin/iter.mbt

pub fn Iter::take[T](self : Iter[T], n : Int) -> Iter[T] {
  // [..take(10,seq), next] would continue
  // even if seq has less than 10 elements
  // but `for x in [..take(10,seq), next ] { break }` would stop
  //
  fn(yield_) {
    let mut i = 0
    let mut r = IterContinue
    self.just_run(fn {
      a =>
        if i < n {
          if yield_(a) == IterContinue {
            // The yield_ callback has control over the loop
            i = i + 1
            IterContinue
          } else {
            r = IterEnd
            IterEnd // yield_ terminates the entire loop here
          }
        } else {
          IterEnd // i < n, stop iteration
        }
    })
    r
  }
}
```

`Iter::drop`'s implementation explains why internal iterators are indivisible:

```moonbit
// ref: https://github.com/moonbitlang/core/blob/main/builtin/iter.mbt


pub fn Iter::drop[T](self : Iter[T], n : Int) -> Iter[T] {
  fn(yield_) {
    let mut i = 0
    self.run(fn(a) {
      if i < n {
        i = i + 1
        IterContinue
        // This skips n elements, but Iter::drop is merely a decorator
        // that prevents calling yield_ for the first n elements.
        // i still increments by n even after drop
      } else {
        yield_(a)
      }
    })
  }
}
```

```moonbit
test "split internal iterator" {
  let xs = [1,2,3,4,5]
  let iter = xs.iter().drop(4)
  // drop here is only a decorator altering iteration behavior
  inspect!(xs.iter().last(), content="Some(5)")
  // The iteration process remains xs.iter()
  inspect!(iter.head(), content="Some(5)")
  // xs.iter().last() still requires 5 iterations
  // The source analysis above explains why 5 iterations are needed
}
```

After `Iter::drop`, the internal state `i` must still increment, demonstrating that internal iterators are indivisible.

[+-](/blog/iterator/internal-vs-external.md#:embed)
