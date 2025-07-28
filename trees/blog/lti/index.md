---
title: Understanding Local Type Inference
collect: true
author: [CAIMEOX](https://github.com/CAIMEOX)
taxon: Blog
date: 2025-07-27
---

在静态类型编程语言的演进历程中，**类型推断**（type inference）机制始终扮演着至关重要的角色。
它允许程序员省略那些可由上下文导出的类型标注，从而极大地降低了代码的冗余度，
使得程序无论在阅读还是编写上都更为便捷。

在这一背景下，System $F_\leq$ 堪称一座里程碑式的理论高峰。
它优雅地统一了两种在现代编程中至关重要的概念：源自面向对象编程、
为代码复用与抽象提供极大便利的**子类型化**（subtyping），
以及作为泛型编程基石的**非直谓多态**（[impredicative polymorphism](https://www.wikiwand.com/en/articles/Parametric_polymorphism#Impredicative_polymorphism)）。
然而，一个严峻的现实阻碍了其在实践中的广泛应用：
其强大的表达能力，使得**完全类型推断**（complete type inference）被证明是**不可判定的**（undecidable）难题。

本文基于 Pierce 与 Turner 的研究 *Local Type Inference*，
但也关注工程实践。
它提出了一条迥然不同的路径：摒弃对「完全性」的执着，转而探索一种更简单、更务实的**部分类型推断**（partial type inference）。其核心理念，在于引入一个额外的简化原则 —— **局部性**（locality）。
所谓「局部」，意指任何缺失的类型标注，都应仅仅依据其在语法树上的相邻节点信息来恢复，而不引入任何长距离的约束（例如 Algorithm J 中的那种全局性的合一变量）。

[+](/blog/lti/how_to_read.md#:embed)
[+](/blog/lti/enough.md#:embed)
[+](/blog/lti/language.md#:embed)
[+](/blog/lti/explicit.md#:embed)
[+](/blog/lti/synthesis.md#:embed)
[+](/blog/lti/cg.md#:embed)
[+](/blog/lti/calc_args.md#:embed)
[+](/blog/lti/bidirectional.md#:embed)
[+](/blog/lti/conclusion.md#:embed)