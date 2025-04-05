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

- Mooncakes 开源

  由 MoonBit 官方的 [Yoorkin](https://github.com/Yoorkin) 领头，[Lampese 东灯](https://github.com/Lampese) 参与建设新版 mooncakes.io 网站已经[开源在 moonbitlang 组织内](https://github.com/moonbitlang/mooncakes.io)。该网站采用纯 MoonBit 基于 [rabbit-tea](https://github.com/Yoorkin/rabbit-tea) 框架与 [Tailwind CSS](https://tailwindcss.com) 构建，是采用 MoonBit 开发多网页应用的一个优秀示例。而且官方的 mooncakes.io 已经更换了这一版的实现。

  值得注意的是这次的新版 mooncakes.io 采用了来自社区的两个仓库 [fuzz-match](https://github.com/moonbit-community/fuzzy_match) 与 [lazy](https://github.com/CAIMEOX/lazy/blob/main/src/lazy.mbt)，分别用于搜索和惰性求值。

- WASM I/O 2025
  
  本周，MoonBit 亮相巴塞罗那 [WASM I/O 大会](https://wasm.io)，并进行技术分享。本次为中国开发者平台首次登上这一国际技术峰会，展示了本土开源力量在 WASM 生态的创新成果。活动中，MoonBit 负责人张宏波 发表了主题演讲 [《MoonBit & WebAssembly》](https://2025.wasm.io/sessions/moonbit-and-webassembly-unlocking-the-true-efficiency-of-wasm)。社区对 MoonBit 的表现给予了高度评价：Kotlin/Wasm 作者 Zalim 在社交媒体上表示：“MoonBit 在 WebAssembly 平台实现了精彩的成果”，对 MoonBit 在 WASM 方向的技术成果给予认可。ZivergeTech & Golem Cloud 公司 CEO John A De Goes 也表示：“与张宏波在 WASM I/O 见面后，我对 MoonBit 未来更加充满期待！”

本周社区新增优质项目：

- 由 [Lampese 东灯](https://github.com/Lampese) 主导中科院软件所 PLCT 实验室 J139 小队基于 [Kodama](https://github.com/kokic/kodama) 搭建的 Community-Blog 本周正式开源并接受社区贡献，用于表达社区声音和促进社区发展。现在已经可以在 https://moonbit.community 访问。

- MoonBit 官方同学 [Yu Zhang](https://github.com/Yu-zh) 采用 MoonBit 编写了一个 Text Editor [Tuzi](https://github.com/Yu-zh/Tuzi)，是使用 MoonBit Native 开发 cli 应用很有意思的尝试。

- MoonBit 官方同学 [tonyfettes](https://github.com/tonyfettes) 开源了 [MoonBit Interface (.mbt) 文件的 tree-sitter 支持](https://github.com/tonyfettes/tree-sitter-mbti) 仓库，这与官方最近两周支持了该文件的高亮有关。

- MoonBit 官方同学 [tonyfettes](https://github.com/tonyfettes) 制作了 MoonBit 的 Linter 工具 [moon-lint](https://github.com/tonyfettes/moon-lint)，在 3 月 30 日的 Meetup 中也有对应介绍。该工具基于 tree-sitter，目前可以完成一些非静态语义分析的 lint 工作。

- MoonBit 官方同学 [myfreess](https://github.com/myfreess) 编写了一个针对 MoonBit 代码的 diff 工具 mbtdiff(https://github.com/myfreess/mbtdiff)。该 diff 工具基于 MoonBit native 后端编写，可以在命令行使用。将来可能为 LLM for MoonBitCode 的效果带来提升。

- [Ranhao Kang](https://github.com/RanhaoKang) 编写了一个项目 [moonbit-unity](https://github.com/RanhaoKang/moonbit-unity)，尝试在 Unity 游戏框架中采用 MoonBit 编程。编译流程为 MoonBit -> JS backend -> PuerTS -> Unity。这个项目是 MoonBit 横向探索的一个有意思的项目。

- [Oboard](https://github.com/oboard) 编写了一个 [mbx 编译器](https://github.com/oboard/mbx-compiler)，他提出了一种类似 jsx/tsx 的语法 mbx，允许 HTML 标签内嵌在 MoonBit 代码中，并且支持编译到 [rabbit-tea](https://github.com/Yoorkin/rabbit-tea) 语法。该库是采用 MoonBit 开发前端应用非常前沿的尝试。

- [colmugx](https://github.com/colmugx) 编写了一个实验性项目 [moonbit-zig-experimental](https://github.com/colmugx/moonbit-zig-experimental)，采用 Zig + MoonBit 的方式编写了一个 HTTP 客户端。

- [Hyrious](https://github.com/hyrious) 为 [Sublime](https://www.sublimetext.com) 编辑器开发了 MoonBit 的高亮和 LSP 支持，[现已在 Github 开源](https://github.com/hyrious/moonbit-syntax-highlight/)。

- [quirk-lab](https://github.com/quirk-lab) 为 MoonBit 编写了 [Zed 插件支持](https://github.com/quirk-lab/zed-moonbit)。

本周社区新增优质包：

- [Luna Flow](https://github.com/luna-flow) 组织推出了一个数据可视化库（该项目主负责人为 [yokiautummoon 结城秋月](https://github.com/yokiautummoon)），专注于提供简洁、高效的图表绘制功能库 Luna-Plot，现在已经有效果非常好的 demo。目前开源在 [MoonBit-Community](https://github.com/moonbit-community/luna-plot) 组织内。除此之外，Luna-Flow 也在着眼多条工作线，最近的两周中又新建了 [calculus-symbolic](https://github.com/Luna-Flow/calculus-symbolic) 与 [quaternion](https://github.com/luna-flow/quaternion) 两个项目，分别着眼于表达式为分和四元数计算。

- [ShellWen 颉文](https://github.com/ShellWen) 编写了一个 dotenv 文件的解析器 [dotenv-mbt](https://github.com/moonbit-community/dotenv-mbt)。该库用于解析 .env 文件，文档十分齐全，代码质量非常高，并且已经通过了 PLCT 实验室的最终产出验收。

- [ShellWen 颉文](https://github.com/ShellWen) 还编写了一个 URL Router 库 [sw-router](https://github.com/moonbit-community/sw-router)，用于解决 URL 的路由问题。该库的文档和代码质量都不错，目前已经通过 PLCT 实验室第一阶段产出验收。

- [Seedking](https://github.com/Seedking) 编写了一个语义化版本号解析器 [SemVer](https://github.com/Seedking/SemVer)，用于语义化解析和比较版本号，为后面编写一些处理版本号相关的程序创造了可能。目前已经通过 PLCT 实验室的最终产出验收。

- [CAIMEO](https://github.com/CAIMEOX) 编写了一个 [LazyList](https://github.com/CAIMEOX/lazy-list) 库，这可能为后续需要惰性列表的场景提供帮助。目前可预见的是在基于 [rabbit-tea](https://github.com/Yoorkin/rabbit-tea) 框架编写的前端应用中会有应用。目前已经通过 PLCT 实验室最终产出验收。

- [smallbearrr](https://github.com/smallbearrr) 编写了一个图论算法库 [NetworkX](https://github.com/moonbit-community/NetworkX)，目前还处于起步阶段。

本周社区项目维护动态（只会写相对重要的内容）：

- Luna-Flow (TBD)
