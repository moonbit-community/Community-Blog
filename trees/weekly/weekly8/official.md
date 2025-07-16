---
title: 本周官方重要动态
---

- MoonBit 官方开源了使用 MoonBit 编写的编译器前端 [parser](https://github.com/moonbitlang/parser)，基于 [moonlex](https://github.com/moonbitlang/moonlex) 与[moonyacc](https://github.com/moonbitlang/moonyacc)。证明 MoonBit 当前的编译器前端已经完成了自举，也证明了 MoonBit 在符号计算相关领域的优势。
- MoonBit 官方开源了异步基础设施 [async](https://github.com/moonbitlang/async)，目前可以确保在 Linux/macOS 的 Native/LLVM 后端上正常运行。库的功能非常完善，支持结构化并发、优秀的错误传播和任务取消。未来将会支持比如 Windows 支持之类的更多功能。
- MoonBit 官方开源了使用 WasmOfOCaml 编译的跨平台 MoonBit 编译器 [moonc_wasm](https://github.com/moonbitlang/moonc_wasm)，采用 Wasm 文件发行，可以解决很多小众平台的 MoonBit 发行问题。
- MoonBit 官方的 Pearls 系列文章更新了第三、四篇文章[《MoonBit Pearls Vol.03：算法竞赛经典：背包问题》](https://mp.weixin.qq.com/s/9bey04RiYhvTj2x8ZD268Q)、[《MoonBit Pearls Vol.04：用 MoonBit 探索协同式编程（上）》](https://mp.weixin.qq.com/s/Uc6uZuIIbOapOaVyZZ1ong)，分别讨论了 MoonBit 与动态规划和协同式编程的的话题。
- MoonBit 官方在 Beta 阶段的双周报正式改为月报，7 月 15 日发布了一次[月报](https://mp.weixin.qq.com/s/253cG9u57B1B0LVavgE2zQ)，有以下内容：
    
  - 支持 `!expr` 语法。对布尔表达式取反现在可以直接使用 `!` 符号，不一定要使用 `not` 函数。
  - `try .. catch .. else ..` 语法中的 `else` 关键字被替换为 `noraise`，原因是 `try .. catch .. else .. `中的`else` 后是模式匹配而非代码块，和其他地方的 `else` 不一致。旧的写法将被废弃，编译器会提出警告。
  - 允许函数返回值标记 `noraise`，一方面可以使类型签名中提供更清晰的文档信息，另一方可以用于防止在一些情况下编译器自动插入 `raise` 标记，比如：
    ```mbt
    fn h(f: () -> Int raise) -> Int { ... }

    fn init {
        let _ = h(fn () { 42 }) // ok
        let _ = h(fn () noraise { 42 }) // not ok
    }
    ```
  - 允许了 ... 对模式匹配中的代码进行省略。
  - 引入 moon coverage analyze 命令，代码覆盖率一键检测、可视化未测分支。
  - 标准库更新预告：JSON 类型构造方式将发生变化，请使用推荐函数 Json::number 等构建方式
  - MoonBit 社区将以开源社区合作伙伴的身份参展 2025 中国 RISC-V 峰会，本届峰会预计将吸引超过 1000 名国内外专业观众线下参与，欢迎感兴趣的同学在 7 月 16 - 7 月 18 日前往展台与 MoonBit 社区大使共同交流。
