---
title: Understanding Local Type Inference
collect: true
author: [CAIMEOX](https://github.com/CAIMEOX)
taxon: Blog
date: 2025-07-27
---

In the evolution of statically typed programming languages, the **type inference** mechanism has consistently played a pivotal role. It allows programmers to omit type annotations that can be derived from context, significantly reducing code redundancy and making programs more convenient to both read and write.

Against this backdrop, System $F_\leq$ stands as a landmark theoretical achievement. It elegantly unifies two concepts crucial to modern programming: **subtyping**—originating from object-oriented programming and greatly facilitating code reuse and abstraction—and **impredicative polymorphism**, the cornerstone of generic programming. However, a critical limitation hinders its practical adoption: its expressive power renders **complete type inference** an **undecidable** problem.

This article builds upon Pierce and Turner's research in *Local Type Inference* while emphasizing engineering practicality. It proposes a fundamentally different approach: abandoning the pursuit of "completeness" in favor of exploring a simpler, more pragmatic **partial type inference**. The core innovation lies in introducing an additional simplifying principle—**locality**. By "locality," we mean that any missing type annotation should be reconstructed solely using information from adjacent nodes in the syntax tree, without introducing long-range constraints (such as the global unification variables in Algorithm J).

[+](/blog/lti/how_to_read.md#:embed)
[+](/blog/lti/enough.md#:embed)
[+](/blog/lti/language.md#:embed)
[+](/blog/lti/explicit.md#:embed)
[+](/blog/lti/synthesis.md#:embed)
[+](/blog/lti/cg.md#:embed)
[+](/blog/lti/calc_args.md#:embed)
[+](/blog/lti/bidirectional.md#:embed)
[+](/blog/lti/conclusion.md#:embed)
