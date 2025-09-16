---
title: 本周官方重要动态
---

- MoonBit 官方发布了[月报 Vol.03](https://www.moonbitlang.cn/weekly-updates/2025/09/08/index)，包含多项重要语言更新：

  **语言更新**：
  - 新增 Bitstring pattern 支持，用于在模式匹配 `Bytes` 或 `BytesView` 过程中匹配特定宽度的 bits，支持 `u<width>be` 或 `u<width>le` 语法指定大端或小端序，宽度范围 `[1, 64]`
  - 允许直接用构造器进行模式匹配，表示只匹配 enum 的 tag
  - 新增 `#callsite(migration)` 属性，用于对可选参数进行代码迁移
  - 新增 `#skip` 属性用于跳过测试，`#as_free_fn` 属性替代 `fnalias` 功能
  - `#alias` 和 `#as_free_fn` 增加可见性控制
  - 异步函数默认 raise，使代码更加简洁
  - FFI 声明中指针参数必须标注 `#borrow` 或 `#owned`，修改了 `FuncRef[_]` 的调用约定

  **工具链更新**：
  - IDE 支持了对 mbti 文件的 hover 和 gotodef 等功能

- MoonBit 官方的 Pearls 系列文章更新了第十、十一篇文章：[《MoonBit Pearls Vol.10: prettyprinter：使用函数组合解决结构化数据打印问题》](https://mp.weixin.qq.com/s/pMplne_nay4vHUHSmhSBTQ)、[《MoonBit Pearls Vol.11: 正则表达式引擎的两种实现方法：导数与 Thompson 虚拟机》](https://mp.weixin.qq.com/s/4uvF0KAPDfhkjiAl7mtNrg)，分别探讨了基于函数组合的 prettyprinter 实现和两种正则表达式引擎的性能对比。
- MoonBit 再次走进清华大学：张宏波受邀参加「思源计划」与「程序设计训练课」。[《MoonBit 再次走进清华：张宏波受邀参加「思源计划」与「程序设计训练课」》](https://mp.weixin.qq.com/s/d7vODHcDOD2-6Orsd1LzyQ) 报道了 2025/9/7 日～ 2025/9/9 日期间，MoonBit 平台负责人张宏波受邀出席清华思源导师团信息技术组 VibeCoding 夏季活动和清华大学计算机系的程序设计训练课，分享了 MoonBit 的"双向可读性"设计理念和 AI 原生编程语言的发展趋势。
- MoonBit 官方发布了重要技术博客[《性能超 Rust 约 33%，10 行代码解析 IP 包》](https://www.moonbitlang.cn/blog/moonbit-value-type)（CSDN 也有类似推文，在此不重复转发相似内容，介绍了 Beta 版本中引入的两大新特性：

  **Value Type（值类型）**：
  - 通过 `#valtype` 标注，让 `struct` 和 `tuple struct` 以值类型形式存储
  - 避免额外的堆分配和 GC 压力，提升运行效率
  - 在 FFT（快速傅立叶变换）性能测试中表现优异：相比 Rust 有 **33% 的性能提升**，相比 Swift 有 **133% 的性能提升**

  **Bitstring Pattern（位串模式）**：
  - 允许在模式匹配中直接提取任意长度的比特片段，支持大端或小端拼接
  - 特别适合网络协议解析和字节序列处理
  - 仅用 10 行代码即可解析 IP 包，代码更贴近协议规范描述

  这些新特性使得 MoonBit 在处理底层数据和计算密集型任务时展现出媲美甚至超越主流编程语言的性能潜力。
