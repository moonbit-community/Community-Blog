---
title: Levels of Abstraction
collect: true
---

LunaFlow 采用分层模块化架构，
通过严格的抽象层级将系统组件进行逻辑划分。
其架构可组织为树形结构：
位于根基位置的是 [Luna-Generic](https://github.com/Luna-Flow/luna-generic) 核心模块，
该模块借助 MoonBit 的 trait 系统实现了对基础数学结构的代码描述。
在此基础上，作为首要叶子节点的 [Luna-Utils](https://github.com/Luna-Flow/luna-utils) 模块承担了通用工具函数的实现，
而诸如 [Complex](https://github.com/Luna-Flow/luna-complex) 与 [Quaternion](https://github.com/Luna-Flow/quaternion)
等基础数据结构包则构成了更为细化的叶节点。

[Modules](/blog/lunaflow/structure.typ#:block)

高阶数学工具包被置于抽象体系的更上层级，
当前主力模块包括 [Calculus Numerical](https://github.com/Luna-Flow/calculus-numerical)、
[Linear Algebra](https://github.com/Luna-Flow/linear-algebra) 及 [Polynomial](https://github.com/luna-flow/luna-poly) 等，
这些模块通过显式的依赖关系调用底层服务，展现出清晰的依赖倒置原则（Dependence Inversion Principle）。
尤为精妙的是，LunaFlow 的架构设计允许用户在 `Luna-Generic` 的抽象框架下扩展自定义数据结构，
这些用户定义类型可无缝融入现有类型系统，并与上层模块达成双向互操作。
自然地，这引出一个关键性问题：如何构建具有数学严谨性的通用数据抽象？
