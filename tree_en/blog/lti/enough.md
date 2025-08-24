---
title: Just Enough Type Information
collect: true
---

After abandoning the pursuit of "complete type inference," a crucial question emerges: To what extent must a "partial" type inference algorithm infer types to be considered "enough"? A highly pragmatic answer: The core mission of a good partial type inference algorithm is to eliminate those type annotations that are both pervasive and foolish.

Here, "foolish" stands in contrast to "reasonable." "Reasonable" annotations, such as type declarations for parameters in top-level function definitions, typically serve as valuable, compiler-verified documentation that aids code comprehension. "Foolish" annotations, conversely, add nothing but syntactic noise while providing almost no useful information. Imagine in a fully explicitly-typed language, no one would want to write or read those redundant `Int` annotations in `cons[Int](3, nil[Int])`.

Pierce's study of hundreds of thousands of lines of ML code revealed three primary sources of "foolish annotations":

- **Polymorphic instantiation**: In the measured code, type applications (i.e., instantiations of polymorphic functions) were ubiquitous, occurring at least once every three lines on average. These type parameters inserted at polymorphic function call sites offer virtually no documentation value and are purely syntactic baggage.
- **Anonymous function definitions**: Adding type annotations to parameters of anonymous functions in contexts like `map(list, fun(x) x+1)` only obscures the core logic, creating unnecessary distraction.
- **Local variable bindings (Let)**: Annotating types for these short-lived intermediate variables is clearly tedious and meaningless.

Based on these quantitative observations, we can outline the contours of an "enough" partial type inference algorithm:

1. It must infer type arguments in polymorphic function applications. Meanwhile, requiring programmers to provide explicit annotations for top-level functions or relatively scarce local functions is entirely acceptable, as these annotations themselves constitute beneficial documentation.
2. To facilitate higher-order programming, the algorithm should infer types for anonymous function parameters, though this isn't strictly mandatory.
3. Local variable bindings should generally not require explicit type annotations.

[+](/blog/lti/strategies.md#:embed)
