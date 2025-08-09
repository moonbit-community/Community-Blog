---
title: Review and Summary
collect: true
---

$$ \text{CPS} \to \text{Defunctionalization} \to \text{Inlining} \to \text{Tail Call Elimination} $$

让我们对这一系列精妙的程序转换过程进行系统性的理论总结。
整个改造工程可分解为四个阶段：

- 第 Ⅰ 阶段：控制流显式化 (CPS 变换)：
  通过引入延续传递形式，我们将原本隐含在语言运行时中的执行上下文显式提升为可操作的一等公民。
  这一关键转换使递归调用点的控制流转移过程浮出水面，为后续的机械化改造奠定了基础。

- 第 Ⅱ 阶段：去函数化：
  基于 Reynolds 提出的去函数化理论，
  我们将高阶的延续函数降维为具体的代数数据类型 `TreeCont`。
  这一转换揭示了延续本质上是对调用栈的结构化建模，
  其中 `Next` 构造子对应栈帧压入操作，对其模式匹配则是出栈，
  `Return` 则表征栈空状态。
  通过此步骤，动态的函数调用关系被静态的数据结构所替代。

- 第 Ⅲ 阶段：内联与尾递归化：
  通过将辅助函数 `run_cont` 内联到主处理流程，
  我们消除了函数间的相互递归调用，形成严格的尾递归形式。
  此时程序的执行流已呈现近线性结构，
  每个函数调用点的上下文关系完全由传入的延续对象所决定，
  这为尾调用优化提供了理想的先决条件。

- 第 Ⅳ 阶段：迭代式转换：
  最终阶段将尾递归结构转换为基于可变状态和循环命令的迭代实现。
  这一转换过程严格对应现代编译器对尾调用的优化策略：
  将递归调用点改写为带状态更新的循环跳转，将延续对象转换为显式的栈数据结构。
  值得注意的是，从 `TreeCont` 到命令式栈的转换验证了理论计算机科学中“程序即数据”的观点。

“去函数化”的确是精妙的程序转换技术，
若读者在看完本文仍意犹未尽，
希望能够深入了解其背后的理论基础和更多实现细节，
可以参考以下资源：

- [Defunctionalization: Everybody Does It, Nobody Talks About It](https://blog.sigplan.org/2019/12/30/defunctionalization-everybody-does-it-nobody-talks-about-it/)
  - [[Translation]去函数变换：一项程序员习焉而不察的技术](https://zhuanlan.zhihu.com/p/1936586173591032199)
- [Definitional interpreters for higher-order programming languages](https://dl.acm.org/doi/10.1145/800194.805852)
