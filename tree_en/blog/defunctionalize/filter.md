---
title: Defunctionalization: A Taste of the Filter DSL
collect: true
---

Let us proceed step by step.  
As a starting point, consider a typical basic example: suppose we need to implement a `filter` function that takes a list and a predicate function as input, and returns a new list consisting of all elements satisfying the predicate.  
Using a recursive strategy, we can achieve the following implementation:

![original_filter](moonbit/src/defunc/filter.mbt#:include)

Here, the higher-order nature of `pred` leads to an essential problem: in low-level compilation scenarios (e.g., when compiling MoonBit to C), functions cannot be stored and passed as conventional data structures. In other words, at the target language level, there are fundamental limitations to directly representing first-class functions.

The most intuitive solution is exhaustive enumeration—encoding all possible predicate functions by listing them. The following example demonstrates several basic predicates for integers:

![limited_filter](moonbit/src//defunc/filter.mbt#:include)

With this definition, we can refactor the filter function into a defunctionalized version:

![defunc_filter](moonbit/src//defunc/filter.mbt#:include)

However, this approach has obvious limitations.  
Indeed, the set of higher-order predicate functions is uncountably infinite, making complete enumeration theoretically impossible.  
But by leveraging the parametric nature of algebraic data types, we gain a degree of extensibility.  
For example, generalizing `IsNegative` to a parameterized `IsLessThan`:

![defunc_filter_extend](moonbit/src//defunc/filter.mbt#:include)

More significantly, we can introduce composite logical structures.  
By adding logical connectives like `And`, we enable the composition of predicate functions:

![defunc_filter_extend_compose](moonbit/src//defunc/filter.mbt#:include)

Through such layered abstraction, the `Filter` type we've constructed essentially evolves into a Domain-Specific Language (DSL).  
Interested readers are encouraged to explore implementing its Parser and Pretty Printer to enhance this DSL's serialization capabilities.

It must be noted, however, that this algebraic-data-type-based approach suffers from an inherent closed-world limitation—each new variant requires modifying all related pattern-matching logic (the `run` function in this case).  
This contrasts sharply with the innate openness of higher-order functions, which allow freely extending new functions without altering existing code.