---
title: Traverse a Tree
collect: true
---

Through the preceding discussion, readers should have established a fundamental understanding of the core concept of defunctionalization.  
This section will apply this technique to solve a more challenging problem—optimizing binary tree traversal.  
First, we present the canonical definition of a binary tree:

![define](moonbit/src/defunc/tree.mbt#:include)

Consider the basic pre-order traversal implementation:

![pre_order](moonbit/src/defunc/tree.mbt#:include)

In this function's design and implementation, we employ a recursive algorithm to systematically traverse the tree data structure.  
While this approach ensures each node is precisely processed by function `f` and strictly adheres to the established sequence of pre-order traversal, its recursive paradigm exhibits significant efficiency bottlenecks.  
Specifically, because this recursive process is not in a tail-recursion optimized form, modern compilers' tail-call optimization (TCO) mechanisms cannot automatically convert it into an equivalent iterative form.  
This characteristic inevitably leads to continuous accumulation of the call stack, thereby impairing program execution performance.  
Consequently, we must urgently apply the program transformation technique of "defunctionalization" discussed earlier to overcome this limitation.