---
title: This Week's Official Highlights
---

- On May 19th, MoonBit officially released a [Weekly Report](https://mp.weixin.qq.com/s/KQBsPOajuHErFFawZvHKuQ), featuring syntax and toolchain updates:
  - Semantic change for value discarding at the end of `..` call chains: The last `..` in a `.`/`..` call chain now automatically discards its value. This deprecates directly using the value of `x..f()`, requiring explicit saving of `x`.
  - Field-level documentation comment support: Enum constructors and struct fields now support individual doc comments, displayed during code completion.
  - View types `@bytes.View` and `@string.View` are now compiled as value types on C and wasm1 backends, reducing memory allocations and significantly improving performance.
  - Effect function calls now support syntax highlighting: The VSCode plugin supports semantic tokens, applying distinct highlighting styles to effect function calls.
  - Experimental support for virtual packages decoupling interfaces from implementations: The build system introduces virtual package functionality. By declaring a package as virtual and defining interfaces, users can select concrete implementations (default used if unspecified).
  - Single-file test debugging launched: Supports testing and debugging for individual `.mbt` and `.mbt.md` files via `test` and `debug codelen`.

- Dual Updates for MoonBit Plugins!  
  MoonBit achieves a major breakthrough with full support for JetBrains IDEs and LeetCode, bridging engineering practice and algorithmic training.
  - MoonBit ❤ LeetCode  
    The lightweight [Tampermonkey](https://github.com/A-23187/moonbit-leetcode) plugin by community user [A23187](https://github.com/A-23187) adds MoonBit support to LeetCode's editor. Install it to write, debug, and submit solutions in MoonBit across all problems. Leveraging MoonBit's JavaScript backend, it runs **over 8 times faster** than native JavaScript.
  - JetBrains Plugin Continues Evolving  
    The [JetBrains plugin](https://github.com/moonbitlang/Intellij-Moonbit) now supports IntelliJ IDEA, CLion, and other mainstream IDEs. Features include syntax highlighting, intelligent completion, and file structure navigation, with ongoing updates for a smoother coding experience.

- Virtual Package Feature Boosts Development Flexibility!  
  MoonBit introduces **[virtual package](https://www.moonbitlang.cn/blog/virtual-package)**! Declare packages as virtual to decouple interfaces from implementations. Users select concrete implementations or use defaults.  
  ⚠️ *Note: Currently experimental.*

- MoonBit Launches "Pearls" Article Series!  
  The official "Pearls" [call for submissions](https://mp.weixin.qq.com/s/pN4YI5rGQcWknxfLr0JnNw) is open. The inaugural article, "[Writing a Pratt Parser in MoonBit](https://mp.weixin.qq.com/s/bTxEQxIb42zATGibi1cPIg)", is available on GitHub: [moonbit-pearls](https://github.com/moonbitlang/moonbit-pearls).

- MoonBit Shines in the US with Keynote Speech! 🌍  
  On June 13, 2025, MoonBit delivered a keynote on asynchronous programming at the top-tier **LambdaConf**, sharing the stage with tech luminaries like Jonathan Blow (creator of Jai).  

  Notably, **John A De Goes** (founder of GolemCloud) praised MoonBit at WASM I/O and announced plans to use it in the upcoming LambdaConf hackathon!  

  MoonBit founder [Prof. Zhang Hongbo](https://github.com/bobzhang) open-sourced the keynote materials: [moonbit-lambdaconf](https://github.com/bobzhang/moonbit-lambdaconf).
