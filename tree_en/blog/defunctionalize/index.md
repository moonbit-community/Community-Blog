---
title: Derive Iteration from Recursion
collect: true
author: [CAIMEOX](https://github.com/CAIMEOX)
taxon: Blog
date: 2025-04-07
---

<!-- Overview -->

Recursion and iteration are two fundamental repetition patterns in programming. While they differ in implementation, they are computationally equivalent. Recursion decomposes problems through self-invoking functions, typically offering concise expression aligned with mathematical (structural) induction. Iteration, conversely, progressively updates state using loop constructs (e.g., `for`, `while`) to directly control computation flow. However, each approach exhibits distinct trade-offs:

- **Recursion** yields compact, readable code ideal for divide-and-conquer problems (e.g., tree traversal, dynamic programming) but risks **stack overflow** and high function-call overhead, particularly with deep recursion.
- **Iteration** executes faster and conserves stack space but requires explicit state management (e.g., loop variables, temporary storage, or manual stack maintenance), often sacrificing intuitive logic.

Given these complementary strengths and weaknesses, can we systematically transform recursive logic into equivalent iterative implementations? The answer lies in **defunctionalization**—a core concept explored in this article. This technique converts recursive function call relationships into explicit stack-managed structures, enhancing runtime efficiency while preserving correctness.

[+](/blog/defunctionalize/filter.md#:embed)

[+](/blog/defunctionalize/tree.md#:embed)

[+](/blog/defunctionalize/cps.md#:embed)

[+](/blog/defunctionalize/review.md#:embed)