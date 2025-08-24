---
title: Levels of Abstraction
collect: true
---

LunaFlow employs a layered modular architecture, logically partitioning system components through strict levels of abstraction. Its architecture can be organized as a tree structure: at the root lies the [Luna-Generic](https://github.com/Luna-Flow/luna-generic) core module, which implements code descriptions of fundamental mathematical structures using MoonBit's trait system. Building upon this foundation, the [Luna-Utils](https://github.com/Luna-Flow/luna-utils) module serves as the primary leaf node, implementing general utility functions, while fundamental data structure packages such as [Complex](https://github.com/Luna-Flow/luna-complex) and [Quaternion](https://github.com/Luna-Flow/quaternion) form more refined leaf nodes.

[Modules](/blog/lunaflow/structure.typ#:block)

Higher-level mathematical toolkits reside at elevated tiers of the abstraction hierarchy. Current main modules include [Calculus Numerical](https://github.com/Luna-Flow/calculus-numerical), [Linear Algebra](https://github.com/Luna-Flow/linear-algebra), and [Polynomial](https://github.com/luna-flow/luna-poly). These modules invoke underlying services through explicit dependencies, demonstrating clear adherence to the Dependence Inversion Principle. Particularly ingenious is LunaFlow's architectural design, which enables users to extend custom data structures within `Luna-Generic`'s abstract framework. These user-defined types seamlessly integrate into the existing type system and achieve bidirectional interoperability with upper-level modules. Naturally, this raises a pivotal question: How to construct a general data abstraction with mathematical rigor?
