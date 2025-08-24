---
title: Continuation-Passing Style Transformation
collect: true
---

Facing this seemingly tricky control flow problem, we pause for a moment.  
Consider introducing the key concept of "continuation"—which essentially abstracts the remaining computation of the program.  
Specifically, for the evaluation of the expression $1 + 2 * 3 + 4$: when computing $2 * 3$, its continuation is the subsequent computation represented by the expression with a hole $1 + \square + 4$.  
Formally, we can define the continuation as a higher-order function $\lambda x. 1 + x + 4$,  
which takes the current computation result and performs the remaining computation.

The core paradigm of Continuation-Passing Style (CPS) is:  
all functions do not return results directly; instead, they transfer control by passing intermediate values to a continuation function.  
Taking the pre-order traversal of a tree as an example, when the first `pre_order(left, f)` call executes,  
its continuation is the right subtree traversal represented by `fn (_) { pre_order(right, f) }`.  
We extend the function signature to introduce a continuation parameter, and the refactored implementation explicitly injects computation results into the continuation:

![pre_order_cps](moonbit/src/defunc/cps.mbt#:include)

Through strict CPS transformation, the program's control flow gains an explicit procedural representation.  
Based on this, we can further implement **defunctionalization of continuations**, transforming higher-order function representations into data structures.  
Observing that continuations manifest in two forms: the recursive processing function `go(tree, cont)` and the identity function `fn { x => x }`, we encode them as an algebraic data type:

![tree_cont](moonbit/src/defunc/cps.mbt#:include)

The refactored implementation transforms function calls into pattern matching on the continuation structure, introducing a helper function `run_cont` to achieve this:

![pre_order_cps_defunct](moonbit/src/defunc/cps.mbt#:include)

To achieve a complete imperative transformation, we first rewrite the tail-recursive form into an explicit loop structure.  
Using MoonBit's loop syntax, the jump relationships in control flow are presented intuitively:

![pre_order_cps_defunct_loop](moonbit/src/defunc/cps.mbt#:include)

At this point, conversion to traditional loops becomes straightforward. By introducing mutable state variables, we obtain a fully imperative implementation:

![pre_order_loop](moonbit/src/defunc/cps.mbt#:include)

Careful analysis reveals that the `TreeCont` continuation structure essentially simulates a stack storage structure: `Next(right, k)` corresponds to a push operation,  
while pattern matching `Next(tree, next)` corresponds to a pop operation.  
This insight enables us to directly provide an implementation based on an explicit stack:

![pre_order_loop_stack](moonbit/src/defunc/cps.mbt#:include)

This systematic transformation project clearly demonstrates the complete paradigm migration path from higher-order functions to data structures,  
from recursion to iteration, and from implicit control flow to explicit state management.