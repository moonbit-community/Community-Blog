---
title: 本周官方重要动态
---

- MoonBit 支持国产芯片开发--性能媲美 C
  
  MoonBit 凭借 Native 后端，[成功打破 WebAssembly 依赖，实现代码原生运行于嵌入式硬件之上。](https://www.moonbitlang.cn/blog/moonbit-esp32#%E5%9C%A8-esp32-c3-%E4%B8%8A%E5%AE%9E%E7%8E%B0%E7%94%9F%E5%91%BD%E6%B8%B8%E6%88%8F)以 ESP32-C3 芯片上的 "康威生命游戏" 为例，MoonBit 不仅展现与 C 语言匹敌的速度，更凭借模式匹配、标签参数等现代语言特性，极大增强代码可读性和开发体验，提供了一种将原生级执行效率与现代化开发体验相结合的高效解决方案。

  值得注意的是本案例使用了官方同学[lijunchen](https://github.com/lijunchen)开发的[moonbit-esp32](https://github.com/moonbit-community/moonbit-esp32) 包，作为关键桥梁角色，专门负责提供 MoonBit 语言到 ESP-IDF 中各种核心组件功能的绑定。