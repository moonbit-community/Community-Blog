---
title: Review and Summary
collect: true
---

$$ \text{CPS} \to \text{Defunctionalization} \to \text{Inlining} \to \text{Tail Call Elimination} $$

Let us systematically summarize the theory behind this series of ingenious program transformations.  
The entire transformation process can be broken down into four stages:

- **Stage I: Control Flow Explicitization (CPS Transformation)**:  
  By introducing Continuation-Passing Style (CPS), we explicitly elevate the execution context—originally implicit in the language runtime—into manipulable first-class citizens.  
  This pivotal transformation surfaces the control flow transfer mechanism at recursive call sites, laying the groundwork for subsequent mechanical transformations.

- **Stage II: Defunctionalization**:  
  Based on Reynolds' defunctionalization theory,  
  we reduce higher-order continuation functions to a concrete algebraic data type `TreeCont`.  
  This transformation reveals that continuations fundamentally model the call stack structurally,  
  where the `Next` constructor corresponds to stack frame pushing, pattern matching on it represents popping,  
  and `Return` signifies the empty-stack state.  
  Through this step, dynamic function call relationships are replaced by static data structures.

- **Stage III: Inlining and Tail Recursion Transformation**:  
  By inlining the helper function `run_cont` into the main processing flow,  
  we eliminate mutual recursion between functions, resulting in a strict tail-recursive form.  
  The program's execution flow now exhibits a near-linear structure,  
  where the context at each function call site is entirely determined by the passed continuation object,  
  creating ideal preconditions for tail call optimization.

- **Stage IV: Iterative Transformation**:  
  The final stage converts the tail-recursive structure into an iterative implementation using mutable state and loop commands.  
  This transformation strictly mirrors modern compilers' tail call optimization strategy:  
  rewriting recursive call sites into state-updating loop jumps and converting continuation objects into explicit stack data structures.  
  Notably, the transition from `TreeCont` to an imperative stack validates the "programs as data" principle in theoretical computer science.

Defunctionalization is indeed an ingenious program transformation technique.  
If readers remain intrigued after this article and wish to explore its theoretical foundations and implementation details further,  
the following resources are recommended:

- [Defunctionalization: Everybody Does It, Nobody Talks About It](https://blog.sigplan.org/2019/12/30/defunctionalization-everybody-does-it-nobody-talks-about-it/)
- [[Translation] Defunctionalization: A Technique Programmers Use Without Realizing](https://zhuanlan.zhihu.com/p/1936586173591032199)
- [Definitional interpreters for higher-order programming languages](https://dl.acm.org/doi/10.1145/800194.805852)