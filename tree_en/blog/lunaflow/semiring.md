---
title: Semiring
---

In abstract algebra, a **semiring** is a set $R$,
equipped with two binary operations: addition $+$ and multiplication $*$, satisfying the following properties:

- $(R, +, 0)$ is a commutative monoid, meaning it satisfies associativity, commutativity, and has an identity element.
- $(R, *, 1)$ is a monoid, meaning it satisfies associativity and has an identity element.

Additionally, it satisfies the following two properties:

- Distributive laws: $a * (b + c) = a * b + a * c$ and $(a + b) * c = a * c + b * c$.
- $0 * a = 0$ and $a * 0 = 0$, where $0$ is the additive identity element.
