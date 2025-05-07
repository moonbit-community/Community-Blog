--- 
title: You could have invented Fenwick trees
author: CAIMEOX
taxon: Blog
---

> 本文译自 Brent Yorgey 的 Functional Pearl 论文 You could have invented Fenwick trees，并做了一些解释补充，以及将原文的 Haskell 代码都翻译到了 MoonBit 代码。

芬威克树（Fenwick trees），亦称二叉索引树（binary indexed trees），是一种精巧的数据结构，旨在解决这样一个问题：如何在维护一个数值序列的同时，支持在亚线性时间内完成更新操作与区间查询。其实现简洁高效，然亦颇为费解，多由一些针对索引的、不甚直观的位运算构成。本文将从线段树（segment trees）入手——这是一种更为直接、易于验证的纯函数式解法——并运用等式推理，阐释芬威克树的实现乃是一种优化变体，此过程将借助一个 MoonBit 嵌入式领域特定语言（EDSL）来处理无限二进制补码数。

[+](/blog/fenwick/introduction.md#:embed)

