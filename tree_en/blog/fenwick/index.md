```markdown
---
title: You could have invented Fenwick trees
author: [CAIMEOX](https://github.com/CAIMEOX)
date: 2025-05-08
taxon: Blog
---

> This article is translated from Brent Yorgey's Functional Pearl paper "You could have invented Fenwick trees", with additional explanations, error corrections, and translation of the original Haskell code into MoonBit code.

Fenwick trees, also known as binary indexed trees, are an ingenious data structure designed to solve the problem of maintaining a sequence of numerical values while supporting updates and range queries in sublinear time. Their implementation is concise and efficient yet somewhat puzzling, primarily consisting of non-intuitive bitwise operations on indices. This article will begin with segment trees—a more straightforward, easily verifiable pure functional solution—and employ equational reasoning to demonstrate that the Fenwick tree implementation is an optimized variant. This process will utilize an embedded domain-specific language (EDSL) in MoonBit to handle infinite two's complement numbers.

[+](/blog/fenwick/introduction.md#:embed)

[+](/blog/fenwick/segtree.md#:embed)

[+](/blog/fenwick/fenwick_tree.md#:embed)

[+](/blog/fenwick/two_complement.md#:embed)

[+](/blog/fenwick/index_conv.md#:embed)

[+](/blog/fenwick/deriving.md#:embed)

[+](/blog/fenwick/conclusion.md#:embed)
