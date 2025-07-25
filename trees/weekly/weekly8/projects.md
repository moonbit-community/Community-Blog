---
title: 本周社区新增优质项目
---

- [Golem Cloud](https://github.com/golemcloud) 编写了一个新的项目 [moonbit-component-generator](https://github.com/golemcloud/moonbit-component-generator)，是一个嵌入 MoonBit 编译器的 Rust 库，用于程序化生成 MoonBit 源代码并编译为 WebAssembly 组件。该库完全自包含，无需外部依赖，支持通过 crate 特性暴露多种用例，如生成包含任意字符串的 WASM 组件和实现类型化配置的组件。该项目是一个文档非常完善、质量非常高的开创性项目。
- MoonBit 官方同学 [NSlash951 myfreess](https://github.com/myfreess) 在 MoonBit Community 组织中编写了一个项目 [mbti_inspector](https://github.com/moonbit-community/mbti_inspector)，是一个 cli 小工具。可以根据类型在 mbti 里面查询这个类型有哪些方法和 `trait impl`，用于给 [core](https://github.com/moonbitlang/core) 的开发者提供 review 支持。 
- MoonBit 的开源之夏项目 [jade-ui](https://github.com/moonbit-community/jade-ui) 由 [oboard](https://github.com/moonbit-community/jade-ui) 同学开工，是一个基于 [rabbit-tea](https://github.com/moonbit-community/rabbit-tea) 编写的用于构建 Web 应用程序的 MoonBit UI 库。
- [Hank HCHogan](https://github.com/HCHogan) 编写了一个 [Moongle](https://github.com/HCHogan/moongle) 项目，参考了 Haskell 语言社区的著名项目 [Hoogle](https://hoogle.haskell.org)，可以对 MoonBit 包中的 API 进行搜索。目前项目还处于早期阶段。
- [Hank HCHogan](https://github.com/HCHogan) 编写了一个 Haskell 的 MoonBit Tree Sitter 绑定 [haskell-tree-sitter-moonbit](https://github.com/HCHogan/haskell-tree-sitter-moonbit)，可以更方便的在 Haskell 中解析 MoonBit 代码。
- [zhangweijun Zhang-WJ](https://github.com/Zhang-WJ) 采用 [cmark.mbt](https://github.com/moonbit-community/cmark.mbt) 编写了一个简单的前端例子 [cmark-frontend-example](https://github.com/Zhang-WJ/cmark-frontend-example)，展示了如何使用 cmark.mbt 或 OCaml 编写前端应用。
- [Morphir](https://github.com/finos/morphir) 是一个种可以抽象业务逻辑的 IR 和周边工具链和框架，[Eleven19](https://github.com/Eleven19) 编写了一个 Morphir 的 [MoonBit 实现](https://github.com/Eleven19/morphir-moonbit)，目前还处于初期阶段，但是这一工作非常有趣。
- [Congcong Cai HerrCai0907](https://github.com/HerrCai0907) 进行了一个针对 OOP 情况下 MoonBit/AssemblyScript/Native(C++) 三种语言的 [Benchmark](https://github.com/HerrCai0907/moonbit-for-OO-bench)。结果显示 MoonBit 仅在很少的情况下比 AssemblyScript 的结果更优秀，在 Binaryen + WasmGC 的情况下可以与 AssemblyScript 达到基本持平的性能。
- [Gasai ジェリー gasacchi](https://github.com/gasacchi) 用 MoonBit 编写了一个名为 [Glimpse](https://github.com/gasacchi/glimpse) 的编程语言，目前已经完成了 Lexer 部分。
