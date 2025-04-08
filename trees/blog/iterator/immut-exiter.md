---
title: 不可变外部迭代器
collect: true
---



不可变外部迭代器可以返回第一个元素和剩余的迭代过程

```moonbit 
priv type ImmutExIter[A] () -> (A,ImmutExIter[A])?

fn ImmutExIter::uncons[A](self : ImmutExIter[A]) -> (A,ImmutExIter[A])? {
  (self._)()
}
```


这里从`Array[A]`构造不可变外部迭代器

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


测试一下迭代过程 

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