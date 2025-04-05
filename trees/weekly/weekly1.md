---
title: (未发布)Weekly1 社区周报 2025/3/24 ~ 2025/4/6
---

这里是 2025/3/24 ~ 2025/4/6 的社区周报，为双周周报。

在过去的两周中，MoonBit 官方在深圳举办了 OJ 编程大赛和 2025 年第一次 Meetup 活动。社区贡献数量显著增长，有很多质量较高、来自社区的包涌现，基本着眼于基础设施方面。同时，Community-Blog 正式建立，发出第一次 Weekly 周报。

本周官方重要动态：

- Meetup

    3 月 30 日，MoonBit 举办了 2025 年首期技术以[AI 时代下的基础软件](https://mp.weixin.qq.com/s/vDvsqxNAUzkijsPg26RIHA)为主题的 Meetup，吸引了 40 余位场开发者和近 300 名线上观众参与。
    
    活动中，四位 MoonBit 核心工程师带来了精彩技术分享：
    - 李子烨深入解析了 MoonBit 的 LLVM 后端实现原理；
    - 陈玉斌展示了基于 Rabbit-TEA UI 框架构建高效 Web 应用的方法；
    - 鲍志远详解了 MoonBit 代码的语义渲染技术；
    - 费浩祥分享了结合 tree-sitter 构建 Code Linter 的实践经验。

    此外，特邀嘉宾 ShowmeBug & Clacky CEO 李亚飞则带来了 LL3 AI Coding 发展趋势的前沿洞察和实战案例。

    本次活动不仅展示了 MoonBit 的最新技术进展，也为社区员提供了深入交流的平台，
    现场观众提出的精准问题引发了广泛讨论，促进了开发者社区的活跃互动与技术共享。

- OJ 竞赛 (TBD)

    3 月 30 日，在技术分享的热烈讨论之后，迎来了 MoonBit OJ 编程竞技赛决赛颁奖典礼[新年首场Meetup暨OJ编程竞技赛颁奖典礼](https://mp.weixin.qq.com/s/vDvsqxNAUzkijsPg26RIHA)。

    MoonBit OJ 编程竞技赛自启动以来，吸引了众多开发者的积极参与，共有300多名开发者报名，经过激烈的初赛和选拔赛，最终有200名选手脱颖而出，9位顶尖选手在决赛中进行了巅峰对决。

    在决赛中，选手们在3小时内完成了8道高难度的编程题目，展现了他们在算法设计、逻辑推理和代码实现方面的卓越能力。经过紧张而激烈的角逐，最终确定了冠亚季军。

    以下是本次比赛的获奖名单

    | 参赛者名称       |   正确题数 |   总用时 (分钟) |
    |:-----------------|-----------:|----------------:|
    | Dawn Magnet      |          8 |             960 |
    | Hao Zhang        |          6 |             514 |
    | Luyao LYU        |          5 |             310 |
    | xunyoyo          |          5 |             415 |
    | refinedheart     |          5 |             470 |
    | wangnianyi       |          4 |             369 |
    | liuly            |          3 |              70 |
    | zhristophe       |          3 |             301 |
    | Zhehao 0xFF      |          1 |              27 |

    MoonBit OJ 编程竞技赛不仅展示了开发者们的技术实力，也激发了他们对国产基础软件的热情。MoonBit 将继续为开发者们提供高质量的交流和竞技平台，推动技术生态的持续发展。
    我们期待在下一次的社区活动中，看到更多开发者的精彩表现，共同见证 MoonBit 生态的不断进步和发展。

- Mooncakes 开源
  由 MoonBit 官方的 [Yoorkin](https://github.com/Yoorkin) 领头，[Lampese](https://github.com/Lampese) 参与建设新版 mooncakes.io 网站已经[开源在 moonbitlang 组织内](https://github.com/moonbitlang/mooncakes.io)。该网站采用纯 MoonBit 基于 [rabbit-tea](https://github.com/Yoorkin/rabbit-tea) 框架与 [Tailwind CSS](https://tailwindcss.com) 构建，是采用 MoonBit 开发多网页应用的一个优秀示例。而且官方的 mooncakes.io 已经更换了这一版的实现。

本周社区动态：

- 本周由 [illusory0x0 猗露](https://github.com/illusory0x0) 维护的 [fuzz-match](https://github.com/moonbit-community/fuzzy_match) 库基本完工，现在已经成为了可靠性极高的字符串模糊匹配库，并已经被最新开源的 [mooncakes.io](https://github.com/moonbitlang/mooncakes.io) 采用作为搜索框的解决方案。

本周社区新增优质包：

- Luna Flow 组织推出了一个数据可视化库（该项目主负责人为 [yokiautummoon 结城秋月](https://github.com/yokiautummoon)），专注于提供简洁、高效的图表绘制功能库 Luna-Plot，现在已经有效果非常好的 demo。目前开源在 [MoonBit-Community](https://github.com/moonbit-community/luna-plot) 组织内。
