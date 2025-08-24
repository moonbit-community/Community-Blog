---
title: 内部迭代器和外部迭代器
collect: true
---

- Internal iterators: the iteration process is **indivisible**.
- External iterators: the iteration process is **divisible**.

The `Iter[A]` in the Moonbit standard library is an internal iterator.  
There is no way to split `iter` into `(first: A?)` and `(rest: Iter[A])`.

Therefore, it is impossible to implement interfaces like:  
`fn uncons[A](xs: Iter[A]) -> (A, Iter[A])?`

It is also impossible to implement interfaces like:  
`fn next[A](self: Iter[A]) -> A?`

```moonbit
test "split internal iterator" {
  let xs = [1,2,3,4,5]
  let iter = xs.iter().drop(4)
  // 这里的 drop 只是修饰器，改变迭代的行为
  inspect!(xs.iter().last(), content="Some(5)")
  // 但是迭代过程还是 xs.iter()
  inspect!(iter.head(), content="Some(5)")
  // xs.iter().last() 仍然需要迭代5次
```

Immutable external iterators can naturally implement `uncons`.

Mutable external iterators can implement `next`.
