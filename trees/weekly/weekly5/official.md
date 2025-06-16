---
title: 本周官方重要动态
---

- Moonbit 官方在 5 月 19 号发布了一次[官方周报](https://mp.weixin.qq.com/s/KQBsPOajuHErFFawZvHKuQ)，主要进行了语法更新和工具链更新：
  - `..`调用链末尾自动丢弃值语义变更：在  `.`/`..`  调用链末尾的最后一个  `..`  以后会自动丢弃它的值，但这也意味着直接使用  `x..f()`  的值的用法将会被废弃，需要显式保存 `x` 。
  - 字段级文档注释支持：枚举构造器和结构体的字段支持单独的文档注释，在补全时会显示相应的文档。
  - 视图类型 `@bytes.View` 和 `@string.View` 在 C 和 wasm1 后端现在会被编译成值类型，减少内存分配，性能有较大提升。
  - 特效函数调用现支持样式高亮：vscode 插件支持 semantic token , 会对有 effect 的函数调用使用不同的样式高亮。
  - 实验性支持虚拟包，接口与实现解耦：构建系统支持 virtual package 特性，通过将一个 package 声明为虚拟包，定义好一套接口，用户可选择具体使用哪一份实现，如不指定则使用该虚拟包的默认实现。
  - 单文件测试调试功能上线：支持对于单个 .mbt 和 .mbt.md 文件的 test 和 debug codelen。

- MoonBit 插件双更新！
  MoonBit 编程语言实现重大突破，现已全面支持 JetBrains 开发环境与 LeetCode 答题平台，打通了从工程实战到算法训练的学习与实用闭环。
  - MoonBit ❤ LeetCode
    MoonBit 社区用户 [A23187](https://github.com/A-23187)开发的轻量级 [Tampermonkey](https://github.com/A-23187/moonbit-leetcode) 脚本插件，让 LeetCode 编辑器新增 MoonBit 语言支持。安装后，能在 LeetCode 平台选择 MoonBit 编写、调试与提交，支持全部题库。得益于 MoonBit 的 JavaScript 后端能力，运行效率超原生 JavaScript 8 倍以上，妥妥的高效体验。
  - JetBrains 插件持续升级
    MoonBit 在 [JetBrains](https://github.com/moonbitlang/Intellij-Moonbit) 插件市场持续发力，适配 IntelliJ IDEA、CLion 等主流 IDE，语法高亮、智能补全、文件结构导航等功能均已实现，且还在不断更新迭代，为开发者提供更便捷、高效的 coding 体验。
- MoonBit 推出虚拟包特性，开发灵活性大幅提升！
  MoonBit 编程语言又添新特性 —— [virtual package](https://www.moonbitlang.cn/blog/virtual-package)！通过将包声明为虚拟包，用户可选择具体实现，若不指定则使用默认实现，极大地分离了接口与实现，开发灵活性直线上升。
  - 注意当前仍处于实验性状态。
- MoonBit 官方开启了新活动 Pearls 征稿活动，具体可以查看[活动链接](https://mp.weixin.qq.com/s/pN4YI5rGQcWknxfLr0JnNw)。而且已经发出了第一篇 Pearls 文章 [使用 MoonBit 编写 Pratt 解析器](https://mp.weixin.qq.com/s/bTxEQxIb42zATGibi1cPIg)。文章内容在 Github 仓库 [moonBit-pearls](https://github.com/moonbitlang/moonbit-pearls) 中同样可以查看。
- MoonBit 亮相美国，发表主旨演讲！🌍
  2025 年 6 月 13 号，Moonbit 在国际顶级编程大会 LambdaConf 发表了关于异步编程的主旨演讲，更将与 Jai 编程语言创始人、独立游戏大师 Jonathon Blow 等技术大咖同台交流。

  特别值得一提的是：GolemCloud 创始人 John A De Goes 在 WASM I/O 上盛赞 MoonBit，并表示将在即将到来的 LambdaConf 黑客松中亲自使用 MoonBit！

  MoonBit 创始人[张宏波老师](https://github.com/bobzhang)在 Github 开源了演讲的相关内容 [moonbit-lambdaconf](https://github.com/bobzhang/moonbit-lambdaconf) 仓库中。
