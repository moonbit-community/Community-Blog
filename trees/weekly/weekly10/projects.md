---
title: 本周社区新增优质项目
---

- MoonBit 官方同学 [Kaida-Amethyst](https://github.com/Kaida-Amethyst) 开发了一个 MoonBit 的 Godot 绑定 [godot.mbt](https://github.com/Kaida-Amethyst/godot.mbt)，允许开发者使用 MoonBit 语言搭配 Godot 引擎开发游戏。目前完成了 GDExtension 到 MoonBit 类型的映，进一步的抽象需要等待 MoonBit 语言功能的更新，因此项目的开发处于暂停状态。
- MoonBit 官方同学 [Milky2018](https://github.com/Milky2018) 编写了一个新的游戏框架 [selene](https://github.com/Milky2018/selene)，现在项目仍处于早期阶段。该框架将会用于 MGPIC 2025 游戏赛道的教程编写。
- [hanbings](https://github.com/hanbings) 编写了一个新的数据库项目 [chongming](https://github.com/hanbings/chongming)，是一个使用 MoonBit 编写的基于 LSM Tree 的 NoSQL 数据库。目前已完成了 xxhash 算法、murmur3 算法、布隆过滤器、跳表等基本算法和数据结构，后续将继续开发 bson 与 sql 解析，并尝试基于 Raft 算法构建分布式系统。
- [Thomas Gorny trival](https://github.com/trival) 编写了一个编译为 JavaScript 的 WebGPU 实验项目 [moon-webgpu-test](https://github.com/trival/moon-webgpu-test)。该项目演示了如何使用 MoonBit 的 FFI 功能与 WebGPU API 接口并渲染经典的 RGB 三角形。
- [Nathan Soufflet nathsou](https://github.com/nathsou) 开发了一个硬件描述语言项目 [yodl](https://github.com/nathsou/yodl)，是一个用 MoonBit 编写的另一种硬件描述语言。该项目支持 FIRRTL 导出、多端口存储器、模块参数、类型参数等高级功能，提供了完整的硬件设计工具链，包括仿真、测试台和 KiCad 原理图导出功能。
- [Nathan Soufflet nathsou](https://github.com/nathsou) 开发了一个简单的 16 位加载存储 CPU 项目 [cpu16](https://github.com/nathsou/cpu16)，包含指令集架构设计、Rust 模拟器和 Yodl 设计。该项目实现了完整的 CPU16 指令集，支持控制标志、寄存器操作、内存访问和 ALU 运算，可在 FPGA 上运行，并提供了 Nexys A7 开发板的构建支持。
- [Zhehao 0xFF KCN-judu](https://github.com/KCN-judu) 创建了一个新的项目 [luna_engine](https://github.com/KCN-judu/luna_engine)，是一个基于 [rabbit-tea](https://github.com/moonbit-community/rabbit-tea) 的 2D 游戏引擎，目前还处在初期阶段。
- [oboard](https://github.com/oboard) 开发了一个 MoonBit 的交互式解释器项目 [moonbit-repl](https://github.com/oboard/moonbit-repl)，为 MoonBit 语言提供了 REPL（Read-Eval-Print Loop）功能。该项目基于 [moonbit-eval](https://github.com/oboard/moonbit-eval) 项目构建，支持 Native 和 Node.js 两种后端。
- [papo1011](https://github.com/papo1011) 开发了一个 MoonBit 到 LLVM 编译器项目 [drakoon](https://github.com/papo1011/drakoon)，使用 Rust 语言编写。该项目支持基本数据类型（Int、Double、Unit）、数组、变量声明、常量、算术和关系运算符、控制语句（if、for、while）、函数定义等 MoonBit 语言特性，并能够输出 LLVM IR 代码。
- [schwarz](https://github.com/schwarz) 创建了一个 MoonBit 版本的 Gilded Rose Kata 重构练习项目 [gilded-rose-moonbit](https://github.com/schwarz/gilded-rose-moonbit)。这是一个经典的代码重构练习，要求开发者改进遗留代码库并添加新功能。项目包含一个商店库存管理系统，需要处理不同类型商品的质量变化规则，为 MoonBit 开发者提供了很好的练习机会。
- [moonbit-community](https://github.com/moonbit-community) 开发了 Helix 编辑器的 MoonBit 语言支持 [moonbit.helix](https://github.com/moonbit-community/moonbit.helix)，为 Helix 编辑器提供了完整的 MoonBit 语言集成。该项目包含语法高亮、语言服务器配置、代码格式化支持，使用 tree-sitter-moonbit 语法解析器，支持 `.mbt` 文件类型和 `moon.mod.json` 项目根目录识别。
- 为适应 MGPIC 2025 游戏赛道可能出现的大量游戏项目出现，从本期周报到 MGPIC 2025 比赛为止，在“本周社区新增优质项目”底部专门汇总本周出现的新游戏项目，由于编译赛道很多代码并不开源且相对来说没有很大的介绍意义，所以不开设单独的介绍板块。
    - MoonBit 官方开发了一个 2D 横版平台冒险游戏 [pixel-adventure.mbt](https://github.com/moonbitlang/pixel-adventure.mbt)，采用像素艺术风格，可在网页浏览器中运行。该游戏包含完整的游戏系统，包括角色控制、碰撞检测、关卡生成和渲染系统，为 MoonBit 游戏开发提供了完整的示例。
    - [Great Love League](https://github.com/Great-Love-League) 开发了一个 MoonBit 火柴人物理游戏 [stickman-adventure](https://github.com/Great-Love-League/stickman-adventure)。技术栈为 FFI JavaScript 接入了 Matter.js 引擎。
