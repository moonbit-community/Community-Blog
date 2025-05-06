---
title: Continuation-Passing Style Transformation
collect: true
---

面对这个看似棘手的控制流问题，我们稍作停顿。
考虑引入“延续” (continuation) 这一关键概念——其本质是对程序剩余计算过程的抽象建模。
具体而言，对于表达式 $1 + 2 * 3 + 4$ 的求值过程：当计算 $2 * 3$ 时，其延续即为带洞表达式 $1 + \square + 4$ 所表征的后续计算。
形式化地，我们可以将延续定义为高阶函数 $\lambda x. 1 + x + 4$，
该函数接收当前计算结果并执行剩余计算过程。

延续传递形式 (Continuation-Passing Style，CPS) 的核心范式在于：
所有函数均不直接返回结果，而是通过将中间值传递给延续函数来实现控制流转移。
以树的前序遍历为例，当第一个 `pre_order(left, f)` 调用执行时，
其延续正是 `fn (_) { pre_order(right, f) }` 表征的右子树遍历过程。
我们通过扩展函数签名引入延续参数，重构后的实现显式地将计算结果注入到延续中：

![pre_order_cps](moonbit/src/defunc/cps.mbt:#include)

通过严格的 CPS 变换，程序的控制流获得了显式的过程化表征。
基于此，我们可进一步实施**延续的去函数化**，即将高阶函数表示转化为数据结构表示。
观察到延续包含两种形态：递归处理函数 `go(tree, cont)` 与恒等函数 `fn { x => x }`，我们将其编码为代数数据类型：

![tree_cont](moonbit/src/defunc/cps.mbt:#include)

重构后的实现将函数调用转化为对延续结构的模式匹配，引入辅助函数 `run_cont` 实现之：

![pre_order_cps_defunct](moonbit/src/defunc/cps.mbt:#include)

为实现彻底的命令式转换，我们先将尾递归形式改写为显式循环结构。
通过 MoonBit 的 loop 语法，控制流的跳转关系得到直观呈现：

![pre_order_cps_defunct_loop](moonbit/src/defunc/cps.mbt:#include)

此时，向传统循环的转换已水到渠成。通过引入可变状态变量，我们获得完全命令式的实现：

![pre_order_loop](moonbit/src/defunc/cps.mbt:#include)

经仔细分析可见，延续结构 `TreeCont` 实质上模拟了栈式存储结构：`Next(right, k)` 对应入栈操作，
而模式匹配 `Next(tree, next)` 则对应出栈操作。
这一洞察使我们能直接给出基于显式栈的实现：

![pre_order_loop_stack](moonbit/src/defunc/cps.mbt:#include)

这项系统性的转换工程清晰展现了从高阶函数到数据结构，
从递归到迭代，从隐式控制流到显式状态管理的完整范式迁移路径。
