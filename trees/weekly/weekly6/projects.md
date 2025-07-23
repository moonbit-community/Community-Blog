---
title: 本周社区新增优质项目
---

- [AdUhTkJm Yue Huang](https://github.com/AdUhTkJm) 用 MoonBit 编写了一个 MoonBit 的编译器 [moonc](https://github.com/AdUhTkJm/moonc)。他手动开发了从 Lexer/Parser 到解释器的一系列 Pass，目前编译器可以完全解析它自己。该项目也可以作为一个 [mooncakes.io](https://mooncakes.io) 的一个软件包单独使用。
- [BigOrangeQWQ](https://github.com/BigOrangeQWQ/BigOrangeQWQ) 修改了社区中的 [wit-bindgen](https://github.com/peter-jerry-ye/wit-bindgen) 项目，作为一个新项目 [wit-cli-example](https://github.com/BigOrangeQWQ/wit-cli-example)。魔改后的 wit-bindgen 只会生成该 Package 的接口，其余的 Package 将会以依赖项的形式添加到 deps 字段里面，从而作为外部依赖项引用。由 moonbit 工具链自己管理那些未使用到的 import 函数，之后通过 export 提供出真正需要编写的函数。项目目前仍处于早期阶段。
- [FlyCloudC](https://github.com/FlyCloudC) 编写了一个 [Scheme](https://github.com/FlyCloudC/scheme) 解释器。该项目主要用于教学目的，不会添加太多优化，着重在代码的可读性上。
- [chenbimo 陈随易](https://github.com/chenbimo) 创建了一个 MoonBit 开发网 [moonbit.dev](https://moonbit.dev)，但是现在只有一个主页。Github 仓库在 [chenbimo/moonbit.dev](https://github.com/chenbimo/moonbit.dev) 中。
- MoonBit 官方同学 [NSlash951 myfreess](https://github.com/myfreess) 创建了一个 Unicode 属性表生成工具 [unicode_tablegen](https://github.com/myfreess/unicode_tablegen)。该项目用于自动生成 Unicode 字符属性判定函数和测试用例，支持通过命令行和 Python 脚本生成相关的 MoonBit 代码和数据表，方便在编译器、解释器等场景下高效处理 Unicode 字符属性。
