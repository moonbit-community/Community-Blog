---
title: Strategies
collect: true
---

To achieve our goals, we need to design a set of efficient strategies for handling the three type inference scenarios described above.  
The following are the two primary strategies introduced in this paper:

- **Local Synthesis of Type Arguments**: This strategy aims to automatically infer omitted type arguments in polymorphic function applications. Its core approach involves generating a set of local subtype constraints for the undetermined type parameters by comparing the expected types of function parameters with the actual argument types. Subsequently, the algorithm solves these constraints and selects a solution that yields the "best" (i.e., most precise and minimal) result type for the entire application expression.  
- **Bidirectional Propagation of Type Information**: This strategy primarily infers type annotations for bound variables in anonymous functions. It propagates type information downward from surrounding expressions (e.g., function application nodes) to their subexpressions, thereby providing an "expected type" to guide the type checking process of subexpressions.  

Both techniques adhere to the principle of **locality**, meaning all information required for inference is exchanged only between adjacent nodes in the syntax tree, without involving long-range dependencies or global unification variables.
