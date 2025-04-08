---
title: Derive Iteration from Recursion
collect: true
author: [CAIMEOX](https://github.com/CAIMEOX)
---

<!-- Overview -->

递归和迭代是编程中两种基础的重复执行模式，它们在实现方式上有所不同，但计算能力上是等价的。
递归通过函数调用自身来分解问题，通常表达简洁，符合数学 (结构) 归纳法的思维模式；而迭代则借助循环结构 (如 `for`、`while`) 逐步更新状态，直接控制计算流程。然揆诸实现，则各具长短：

- **递归**代码短小清晰，适合解决分治问题 (如树的遍历、动态规划)，但可能导致**栈溢出** (stack overflow) 和较高的函数调用开销，尤其是深度递归时效率降低。
- **迭代**虽然执行更快，节省栈空间，但需要开发者显式管理状态 (如循环变量、临时存储、甚至需要手动维护一个栈)，逻辑可能不如递归直观。

既然两者各有优劣，是否存在一种通用方法，能够自动或半自动地将递归逻辑转换为等价的迭代实现？答案是肯定的，而这正是本文的核心概念——**去函数化 (defunctionalization)**，即将递归的函数调用关系转换为显式的栈管理结构，从而在保持正确性的同时提升运行效率。

[+](/blog/defunctionalize/filter.md#:embed)

[+](/blog/defunctionalize/tree.md#:embed)

[+](/blog/defunctionalize/cps.md#:embed)

[+](/blog/defunctionalize/review.md#:embed)