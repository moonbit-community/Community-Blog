---
title: 本周社区新增优质包
---

- [illusory0x0 猗露](https://github.com/illusory0x0) 编写了一个基于 MoonBit 的 classic adapton 实现，支持懒惰求值和依赖图驱动的增量计算。在该系统中，set 操作不会立即触发更新，而是标记节点为 Dirty，只有在 get 时才会通过依赖图传播变更并执行必要的更新。依赖图在首次调用 Thunk::get 时自动构建，并利用全局栈追踪依赖关系。该实现也支持节点记忆化，用于应对依赖结构动态变化的场景，如电子表格应用。需要注意的是，由于当前 MoonBit 缺少弱引用相关特性，可能导致内存泄漏，尤其在启用 memoization 时更为显著。
- [kesmeey](https://github.com/kesmeey) 编写了一个库，实现了 [IndexSet](https://github.com/moonbit-community/IndexSet)、[IndexMap](https://github.com/moonbit-community/IndexMap)两个主要数据结构。它们与 [MoonBit Core](https://github.com/moonbitlang/core) 的 [HashSet 库](https://github.com/moonbitlang/core/tree/main/hashset) 和 [HashMap 库](https://github.com/moonbitlang/core/tree/main/hashmap) 的所有操作都兼容，目前可进行创建、添加、查询、排序、遍历、集合运算、索引访问等操作。该包目前已基本完成，意见。
- [GreatHank](https://github.com/GreatHank) 编写了 Mutable 版本 [BitVector 库](https://github.com/GreatHank/moonbit-BitVector)，实现了对位向量的表示、存储与常用作，包括设置/清除/翻转位、位计数、逻辑运算、范围截取与序列化等，目前已通过 PLCT 实验室的产出第一次阶段认证。
- MoonBit 官方同学 [tony-fettes](https://github.com/tonyfettes) 在 MoonBit-Community 开源了一个仓库 [uv.mbt](https://github.com/tonyfettes/uv.mbt)，是一个 MoonBit 编写的的 [libuv](https://libuv.org) 实现。
- MoonBit 的官方同学 [Yu-zh Yu Zhang](https://github.com/Yu-zh) 编写了一个终端操作库 [termbit](https://github.com/Yu-zh/termbit)，项目灵感来自 [corssterm-rs](https://github.com/crossterm-rs/crossterm)。目前该包还在开发中，仅在 Mac 芯片上测试过。
- MoonBit 的官方同学 [myfreess](https://github.com/myfreess) 编写了一个 MoonBit Native 后端的 [SQLite3 Binding](https://github.com/myfreess/sqlite3.mbt)，目前还处于早期开发阶段。
