
---
title: 特质声明
taxon: appendix
asref: true
author: [kokic](https://kokic.github.io)
date: 2025-10-29
---

```mbt
trait HasNil {
  nil() -> Self
}

trait HasOne {
  one() -> Self
}

trait AddMonoid: Add + HasNil {}

trait MulMonoid: Mul + HasOne {}

trait Semiring: AddMonoid + MulMonoid {}

trait StarSemiring: Semiring {
  star(Self) -> Self
}

trait Inverse {
  inverse(Self) -> Self
}
```
