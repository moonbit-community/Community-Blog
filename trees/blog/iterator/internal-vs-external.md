---
title: 内部迭代器和外部迭代器
collect: true
---

- 内部迭代器 迭代过程是**不可分割**的。
- 外部迭代器 迭代过程是**可分割**的。

Moonbit 标准库的 `Iter[A]` 是内部迭代器，
没有办法把`iter`切分为`(first : A?)` 和 `(rest : Iter[A])`。

所以无法实现 `fn uncons[A](xs : Iter[A]) -> (A, Iter[A])?` 这样的接口。

也无法实现 `fn next[A](self : Iter[A]) -> A?` 这样的接口。

```moonbit
test "split internal iterator" {
  let xs = [1,2,3,4,5]
  let iter = xs.iter().drop(4)
  // 这里的 drop 只是修饰器，改变迭代的行为
  inspect!(xs.iter().last(), content="Some(5)")
  // 但是迭代过程还是 xs.iter()
  inspect!(iter.head(), content="Some(5)")
  // xs.iter().last() 仍然需要迭代5次
}
```

不可变外部迭代器可以很自然的实现`uncons`。

可变外部迭代器可以实现`next`。
