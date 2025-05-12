---
title: 本周官方重要动态
---
- Moonbit 官方在 5 月 6 号发布了一次[官方周报](https://mp.weixin.qq.com/s/AzdB_J7dI5hzRYo0QAkA6g)，主要进行了语法更新和工具链更新：
  - `Trait` 的实现方式将只支持通过 `impl T for A ...` 对类型 `A` 显式实现 `trait T` ；
  - 新增语法糖：允许使用 `_` 作为待定参数占位符以简化匿名函数的创建；
  - `fnalias` 支持给类型和 `trait` 的方法创建别名；
  - 移除了所有 pragmas，未来将全面使用 attributes 替代;
  - 实现了 `#internal` attribute，用于为 public API 的外部用户提供警告;
  - 对于 `loop` 中可能产生歧义的 loop argument 的使用方式新增了警告;
  - 支持了从 `Array` 到 `ArrayView` 类型、`Bytes` 到 `@bytes.View` 类型的隐式类型转换;
  - `moon` 支持 `bench` 子命令，用于执行基准性能测试。
- Moonbit 官方在 5 月 9 号发布了[开源之夏](https://mp.weixin.qq.com/s/bc8xkj04cMZ9bBBc-73GbQ)活动
  - 开源之夏活动介绍：开源之夏是由中国科学院软件研究所“源软件供应链点亮计划”发起并支持的暑期开源活动。该活动联合国内外开源社区，为全球高校学生提供开源项目任务。学生能在项目资深开发者指导下参与开源项目建设，提升技术能力、了解开源文化，成功完成项目还可获得现金奖励与荣誉证书。
  - MoonBit 项目介绍
    - 项目一：基于 MoonBit 的 Qt 绑定探索与实现；
    - 项目二：基于 tree-sitter.mbt 进行结构化查找/替换的 Visual Studio Code 插件；
    - 项目三：基于 MoonBit 和 TEA 架构的 UI 组件库。
  - 参与方式及时间节点
    - 参与方式：学生登录[开源之夏官网](https://summer-ospp.ac.cn)，进入 MoonBit 项目列表，与导师沟通并按要求提交项目方案，通过评审后正式参与。
    - 时间节点：5 月 9 日起可挑选项目、沟通并准备申请材料，6 月 9 日 18:00 报名及提交申请书截止；6 月 10 日 - 6 月 29 日项目申请审核；6 月 30 日中选公示；7 月 1 日 - 9 月 30 日项目开发；10 月 1 日 - 10 月 31 日结项审核（PR/MR 合并与导师审核）；11 月 1 日 - 11 月 8 日组委会成果审核；11 月 9 日结项公示；11 月年度优秀学生评选。
- MoonBit 地区大使招募开启！
  - MoonBit 地区大使是连接技术与社区的核心桥梁。作为 AI 时代新一代编程语言 MoonBit 的官方代表，你将立足所在区域（高校、技术社区或城市），最大化发挥你的影响力——推广 MoonBit 的技术理念、激活区域开发者群体、引领高质量的技术交流与共创。
  - 招募流程与福利：
    - 流程：报名 → 简历审核 → Package 提交审核 → 面试 → 签约 → 培训上岗。
    - 福利：官方认证大使证书、持续培训与支持、丰厚薪酬与激励、参与 MoonBit 核心生态建设、拓展前沿人脉与影响力。

- MoonBit 支持国产芯片开发--性能媲美 C
  
  MoonBit 凭借 Native 后端，[成功打破 WebAssembly 依赖，实现代码原生运行于嵌入式硬件之上。](https://www.moonbitlang.cn/blog/moonbit-esp32#%E5%9C%A8-esp32-c3-%E4%B8%8A%E5%AE%9E%E7%8E%B0%E7%94%9F%E5%91%BD%E6%B8%B8%E6%88%8F)以 ESP32-C3 芯片上的 "康威生命游戏" 为例，MoonBit 不仅展现与 C 语言匹敌的速度，更凭借模式匹配、标签参数等现代语言特性，极大增强代码可读性和开发体验，提供了一种将原生级执行效率与现代化开发体验相结合的高效解决方案。

  值得注意的是本案例使用了官方同学 [lijunchen](https://github.com/lijunchen) 开发的 [moonbit-esp32](https://github.com/moonbit-community/moonbit-esp32) 包，作为关键桥梁角色，专门负责提供 MoonBit 语言到 ESP-IDF 中各种核心组件功能的绑定。
  