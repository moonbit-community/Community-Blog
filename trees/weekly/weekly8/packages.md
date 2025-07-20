---
title: 本周社区新增优质包
---

- [Fangyin Cheng fangyinc](https://github.com/fangyinc) 编写了一个 MoonBit 的跨平台（后端）的网络包 [net.mbt](https://github.com/fangyinc/net.mbt)，现在已经有较为充足的文档且可以构建简单 HTTP 服务器（目前仅支持 Native 与 JavaScript 后端）。这是社区少有的比较成熟和完善的网络封装库。同时与之配套的还有针对该项目的基础设施 [socket.mbt](https://github.com/fangyinc/socket.mbt)，该包提供了 socket 绑定的支持。
- [迷渡 justjavac](https://github.com/justjavac) 编写了一个新的包 [moonbit-cache-padded](https://github.com/justjavac/moonbit-cache-padded)，是一个可以提供缓存填充的数据结构，用于减少多线程应用程序中的错误共享。目前该包的文档和代码都已经相当成熟完善了。
- [迷渡 justjavac](https://github.com/justjavac) 编写了一个改变 CPU 核心亲和力以控制线程/CPU 核心绑定的库 [moonbit-core-affinity](https://github.com/justjavac/moonbit-core-affinity)。目前该库的文档和代码相当完善，而且可以支持 Windows/Linux/macOS 等主流平台（Other Unix 属于 Limited Support）。
- [迷渡 justjavac](https://github.com/justjavac) 编写了一个 MoonBit 的 glob 处理库 [moonbit-glob](https://github.com/justjavac/moonbit-glob)，用于处理一些 glob 的模式匹配需求，支持主流的 glob 功能。该库的文档和代码都非常成熟完善。
- [迷渡 justjavac](https://github.com/justjavac) 编写了一个字符串 Case 转换库 [moonbit-case](https://github.com/justjavac/moonbit-case)，可以支持将字符串在 `camelCase`、`PascalCase`、`snake_case` 等等多种命名格式中转换。
- [AXiX AXiX-official](https://github.com/AXiX-official) 编写了一个对 MoonBit 的 Primitive Type（除 BigInt 外）以 `ArrayView[Byte]` 形式读写的支持库 [binaryPrimitives](https://github.com/AXiX-official/binaryPrimitives)，该库受启发自 C# 语言的 `System.Buffers.Binary.BinaryPrimitives`。目前的完成度较高。
- [ryota0624](https://github.com/ryota0624) 编写了一个新的包 [moonbit-mustache](https://github.com/ryota0624/moonbit-mustache)，参考自 Go 语言的 [mustache](https://github.com/alexkappa/mustache)。可以用于处理 Mustache 模板语言的工作。
