---
title: 本周官方重要动态
---

- Meetup 成都站

  4 月 26 日，MoonBit 成功在四川成都集火实验室举办 Meetup！本次活动聚焦[AI 时代下的基础软件](https://mp.weixin.qq.com/s/Z27YZ00FVWsMivety3-IUg)，邀请了多位行业专家，共同探讨前沿技术与发展趋势。
  
  活动议程精彩纷呈，四位专家带来了精彩的技术分享：
  
  - 张宏波（IDEA 研究院首席科学家 & MoonBit 团队负责人）剖析国产编程语言现状及 AI 潮流下的机遇；
  - 马发俊（麒麟软件教授级高工 & openKylin 社区生态合作负责人）带来面向 AIPC 的智能操作系统技术及实践分享；
  - 费浩祥（MoonBit 核心工程师）讲述 MoonBit 在 AI Agent 上的创新优势；
  - 董鹏飞（重庆唯哲科技创始人 CEO）探索人工智能背景下编程语言的未来方向。

  本次活动不仅展示了 MoonBit 的最新技术进展，也为社区员提供了深入交流的平台，
  现场观众提出的精准问题引发了广泛讨论，促进了开发者社区的活跃互动与技术共享。
  
- MoonBit 官方在 4.21 发布了一次[官方周报](https://www.moonbitlang.cn/weekly-updates/2025/04/21/index)，主要聚焦在语言更新方面：
  - `async` 函数采用新语法 `f!(..)`，原 `f!!(..)` 将触发警告。
  - 运算符重载迁移至基于 `trait`，旧方法仍可用但会收到编译器警告，迁移仅需将 `op_xxx` 改为对应 `trait` 的 `impl`。
  - `trait` 方法默认实现：新增 `= _` 标记，提升源码可读性。
  - `String` 类型转换：现支持隐式转为 `@string.View`，并恢复 `[:]` 取完整 view。
  - `Core API` 改动：`@string` 包参数类型迁至 `@string.View`，返回值类型相应调整。
  - 工具链优化：IDE 支持 `.mbt.md` 文件 debug 断点设置，`moon.mod.json` 新增构建脚本字段。