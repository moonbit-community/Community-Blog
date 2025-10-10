---
title: 本周社区动态
---

- OSC 开源社区在微信公众号发表了文章[《MoonBit 异步网络库发布：落地智能体应用场景》](https://mp.weixin.qq.com/s/R3FFIC_08tx-OffhGz2Waw)，宣布补齐关键特性的「最后一块拼图」——异步编程与网络库，标志其正式迈入可支撑大规模云服务、高并发应用以及 AI Agent 平台的新阶段。文章详细介绍了三大核心创新：无需 await 的异步调用机制、基于任务树的自动取消机制，以及单线程多任务模型 + epoll/kqueue 事件驱动的性能架构，在 200-1000 并发连接测试中吞吐量超越 Node.js/Go，延迟低至 4.43ms，并通过智能体开发的实际案例展示了这一能力如何在实践中落地。
- [chenbimo 陈随易](https://github.com/chenbimo) 在微信公众号发表了文章[《改变世界的编程语言 MoonBit：配置系统介绍(上)》](https://mp.weixin.qq.com/s/DZBJMFutT8um9FX2SxBNHg)，详细介绍了 MoonBit 的模块配置系统。文章从学习理念出发，采用「剥洋葱」的方式层层递进，深入解析了 moon.mod.json 文件中的各项配置，包括模块基本信息、依赖管理（deps 和 bin-deps）、脚本配置（scripts）、警告控制（warn-list 和 alert-list）等核心功能，为开发者提供了全面的配置系统使用指南。
- 常驻消息：中国科学院软件所的 PLCT（Programming Language and Compiler Technology）实验室为在读学生提供了 MoonBit 实习机会，包括 J139 MoonBit 应用开发与 J147 MoonBit RISC-V 编译器开发，远程/自由度高，有兴趣的同学可以关注 [PLCT 实验室的实习生岗位信息](https://github.com/plctlab/weloveinterns/blob/master/open-internships.md)。
