---
title: 本周官方重要动态
---

- MoonBit 官方在 8 月 11 日发布了[月报 Vol.02](https://www.moonbitlang.cn/weekly-updates/2025/08/11/index)，主要聚焦在语言更新和工具链更新方面：

  **语言更新**：
  - 新增条件编译属性 `#cfg`，支持根据后端等条件进行文件内的条件编译
  - 新增 `#alias` 属性，可以为方法或函数创建别名，并支持标注废弃
  - 新增 `defer` 表达式，提供基于词法作用域的资源清理功能
  - Native 后端的 `Bytes` 类型末尾现在会自动添加 `'\0'` 字节，可直接作为 C string 传递给 FFI 调用
  - 调整可选参数语法，统一了有默认值和没有默认值的可选参数语法
  - 改用 `#callsite(autofill(...))` 属性替代原有的自动填充参数语法
  - 废弃 newtype，增加 tuple struct 支持，提供更灵活的数据结构定义
  - `derive(FromJson, ToJson)` 简化格式参数，保留核心功能

  **工具链更新**：
  - 新增 `moon coverage analyze` 功能，提供更直观的覆盖率报告
  - `moon test --target js` 在 panic 时能根据 sourcemap 显示原始位置

- MoonBit 官方的 Pearls 系列文章更新了第六、七、八、九篇文章：[《MoonBit Perals Vol.06: MoonBit 与 LLVM 共舞 (上)：编译前端实现》](https://mp.weixin.qq.com/s/vX5hxp7jVDU8_KCEZlrmAg)、[《MoonBit Perals Vol.07: MoonBit C-FFI 开发指南》](https://mp.weixin.qq.com/s/F3rnGm9W94BMPDp9zuitoQ)、[《MoonBit Pearls Vol.08：MoonBit 中的错误处理》](https://mp.weixin.qq.com/s/KX41WgzgvSMoXiZbwpOlWQ)、[《MoonBit Pearls Vol.09：MoonBit 中的性能优化》](https://mp.weixin.qq.com/s/adAuAwhQC7Ot2o7xpXM78w)，分别探讨了 MoonBit 的类型系统、并发编程、错误处理和性能优化等核心主题。
- MoonBit 官方发布了全套游戏赛道官方推荐框架，包括 Pixel Adventure.mbt、WASM-4、Selene 等框架全面开放，为第二届 MoonBit 全球编程挑战赛游戏赛道的参赛者提供快速搭建创意游戏的工具支持。具体可见[官方宣发文章](https://mp.weixin.qq.com/s/CvXmINTA1DENXSmE93Yn3g)。
- MoonBit 官方发布了 2025 MGPIC 大赛游戏赛道官方教程，为参赛者提供了详细的游戏开发指导和技术支持。具体可见[官方教程](https://mp.weixin.qq.com/s/qyci1ZbZOItkmBG70RX1pg)。
- 量子位举办了 AI 沙龙活动，邀请 MoonBit、百度文心快码、硅心科技（aiXcoder）、智谱、月之暗面、海新智能、Creao AI 等多家企业共同探讨 AI Coding 的未来发展。IDEA 研究院 MoonBit AI 辅助编程工程师祝海林以 MoonBit Pilot 为例，分享了未来 AI Coding 产品的形态、产品易用性与智能能力的权衡，以及人、产品、代码之间的平衡。具体可见[回顾文章](https://mp.weixin.qq.com/s/qyci1ZbZOItkmBG70RX1pg)。
