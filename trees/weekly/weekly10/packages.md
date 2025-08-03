---
title: 本周社区新增优质包
---

- MoonBit 创始人[张宏波老师](https://github.com/bobzhang) 开发了一个 MoonBit 迭代器访问者模式库 [moonbit-visitors](https://github.com/bobzhang/moonbit-visitors)，展示了在 MoonBit 中优雅地遍历和处理表达式树的实现。该库提供了自动树遍历功能，允许开发者只重写需要的特定行为，实现了最小化样板代码的设计模式，包含完整的测试和文档。
- [Thomas Gorny trival](https://github.com/trival) 编写了一个用于 MoonBit 编程语言的线性代数库[moon-graphics-tests](https://github.com/trival/moon-graphics-tests)。该库提供了双实现架构，包含运行时向量数学计算和 WGSL（WebGPU 着色语言）代码生成功能。支持 Vec2 和 Vec3 向量操作，包括算术运算、点积、叉积、归一化等。
- [CGaaaaaa](https://github.com/CGaaaaaa) 编写了一个用于 MoonBit 编程语言的响应式编程库 [Reactivex](https://github.com/CGaaaaaa/reactivex)。该库提供了 Observable 序列和丰富的操作符，用于组合异步和基于事件的程序。基于 ReactiveX 规范实现，目前有使用示例但是具体的文档仍需完善。
- MoonBit 官方同学 [tonyfettes](https://github.com/tonyfettes) 编写了一个 MoonBit 的 PCRE2 绑定库 [pcre2.mbt](https://github.com/tonyfettes/pcre2.mbt)，为 MoonBit 提供了对 PCRE2 正则表达式库的访问。该库使用 FFI 技术实现了对 PCRE2 C 库的绑定，为 MoonBit 生态增加了强大的文本处理能力。
- [ZSeanYves](https://github.com/ZSeanYves) 开发了一个轻量级的 BSON 编解码库 [MoonbitBSON](https://github.com/moonbit-community/MoonbitBSON)，支持 BSON 文档、数组、字符串、整数、布尔值、空值等核心元素的序列化和反序列化。该库提供了可组合的 API 用于 BSON 构建和遍历。目前该库的 API 文档处于未编写的状态。
- [edragain](https://github.com/edragain2nd) 编写了一个用于解析和写入 BibTeX 和 BibLaTeX 文件的库 [Biblatex-moonbit](https://github.com/edragain2nd/Biblatex-moonbit)。该库基于 Rust 版本的 rust-biblatex 实现，能够将 .bib 文件中的数据解析为易于使用的结构体和枚举，如 Person 和 Date，支持作者、日期等字段的自动类型转换和别名处理。唯一的不足是 API 文档不够完善。
- [oboard](https://github.com/oboard) 开发了一个用于 MoonBit 的 readline 库 [readline](https://github.com/oboard/readline)，提供了跨后端的、基于回调的输入处理功能。
- [AXiX AXiX-official](https://github.com/AXiX-official) 编写了一个 MoonBit 的 xxHash 实现 [mbt-xxhash](https://github.com/AXiX-official/mbt-xxhash)，实现了 xxHash32/64 两种项目。目前该库仍欠缺一些文档说明。
- MoonBit 官方同学 [myfreess](https://github.com/myfreess) 开发了一个语义差异比较库 [rwsdiff.mbt](https://github.com/myfreess/rwsdiff.mbt)，用于比较和显示代码或文本的语义差异。该库目前还处于早期开发阶段。
- [Asterless](https://github.com/Asterless) 开发了一个高性能的 QOI 图像格式编解码库 [MoonQOI](https://github.com/Asterless/MoonQOI)，完全符合 QOI（Quite OK Image）格式规范。该库支持所有 QOI 操作码、RGB 和 RGBA 通道、sRGB 和线性色彩空间，提供了简单易用的 API 接口，适用于需要快速图像压缩和解压缩的场景。
- [chaijie2018](https://github.com/chaijie2018) 开发了一个布隆过滤器库 [bloom](https://github.com/chaijie2018/bloom)，灵感来源于 Go 语言的 bloom 包。该库提供了简洁的集合表示，支持成员查询功能，使用 murmurhash 哈希函数，允许用户指定期望的容量和误判率，适用于需要高效集合成员检查的场景。
- MoonBit 创始人[张宏波老师](https://github.com/bobzhang) 开发了一个 INI 配置文件解析库 [ini-parser](https://github.com/bobzhang/ini-parser)。目前 MoonBit 已经可以解析大部分熟悉的配置文件格式了。
