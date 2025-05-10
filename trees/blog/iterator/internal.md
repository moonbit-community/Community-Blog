---
title: MoonBit 实现内部迭代器
collect: true
author: [illusory0x0](https://github.com/illusory0x0)
taxon: Blog
date: 2025-04-08
---

本文实现的内部迭代器参考 [OCaml iter](https://github.com/c-cube/iter)。

```moonbit
priv type InIter[A] ((A) -> Unit) -> Unit

fn InIter::run[A](self : InIter[A], f : (A) -> Unit) -> Unit {
  (self._)(f)
}
```

这里的 `InIter::from_array` 相当于 `OCaml` 的柯里化。

```moonbit
fn InIter::from_array[A](xs : Array[A]) -> InIter[A] {
  fn(k) { xs.each(k) }
}
```

`with_index` 是装饰器，装饰 `iter` 默认的行为。

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

为了在迭代过程中停止循环，MoonBit 引入了 `IterResult`.

`yield : (A) -> IterResult` 这个回调函数可以控制循环是停止还是继续。

```moonbit
type InIter[A] ((A) -> Unit) -> Unit
type Iter[A] ((A) -> IterResult) -> IterResult
```

我们比较 `Iter[A]` 和 `InIter[A]` 的定义，

把 `Unit` 替换成 `IterResult` 之后，就和 MoonBit 内建的内部迭代器定义一样了
`InIter[A]` 返回 `Unit` 和 回调函数返回 `Unit`, 相当于一直返回 `IterResult::IterContinue`。

MoonBit 标准库中的 `Iter::take`, `Iter::drop`, `Iter::flat_map` ... 这些方法都是装饰器，用来修饰原先 `iter` 的行为。

我们来看 `core` 的 `Iter::take` 的实现，
这个 `Iter::take` 可以用来解释， `yield_` 如何控制循环的状态。

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
            // yield_ 这个回调函数，有循环的控制权
            i = i + 1
            IterContinue
          } else {
            r = IterEnd
            IterEnd // 这里 yield 让整个循环退出了
          }
        } else {
          IterEnd // i < n, 停止循环
        }
    })
    r
  }
}
```

`Iter::drop` 的实现，可以解释为什么内部迭代器是不可分割的。

```moonbit
// ref: https://github.com/moonbitlang/core/blob/main/builtin/iter.mbt


pub fn Iter::drop[T](self : Iter[T], n : Int) -> Iter[T] {
  fn(yield_) {
    let mut i = 0
    self.run(fn(a) {
      if i < n {
        i = i + 1
        IterContinue
        // 这里跳过 n 个元素， 但是这个 Iter::drop 只是装饰器，
        // 让 self 这个迭代器，不对前 n 个元素，调用 yield_ 而已
        // 即使drop 之后，i 仍然会递增 n
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
  // 这里的 drop 只是修饰器，改变迭代的行为
  inspect!(xs.iter().last(), content="Some(5)")
  // 但是迭代过程还是 xs.iter()
  inspect!(iter.head(), content="Some(5)")
  // xs.iter().last() 仍然需要迭代 5 次
  // 上面的源码解析，解释了为什么仍然需要迭代 5 次

}
```

`Iter::drop` 之后，还需要递增内部状态的 `i`, 所以说内部迭代器是不可分割的

[+-](/blog/iterator/internal-vs-external.md#:embed)
