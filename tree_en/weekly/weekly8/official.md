---
title: This Week's Official Highlights
---

- MoonBit officially open-sourced the compiler frontend [parser](https://github.com/moonbitlang/parser) written in MoonBit, built upon [moonlex](https://github.com/moonbitlang/moonlex) and [moonyacc](https://github.com/moonbitlang/moonyacc). This demonstrates that MoonBit's compiler frontend has achieved self-hosting and showcases MoonBit's advantages in symbolic computation domains.
- MoonBit officially open-sourced the asynchronous infrastructure [async](https://github.com/moonbitlang/async), currently ensuring stable operation on Linux/macOS Native/LLVM backends. The library offers comprehensive functionality, supporting structured concurrency, robust error propagation, and task cancellation. Future updates will include features like Windows support.
- MoonBit officially open-sourced the cross-platform MoonBit compiler [moonc_wasm](https://github.com/moonbitlang/moonc_wasm), compiled via WasmOfOCaml and distributed as Wasm files. This resolves distribution challenges for MoonBit on niche platforms.
- MoonBit's Pearls article series updated with two new entries: [《MoonBit Pearls Vol.03：Algorithm Classics: The Knapsack Problem》](https://mp.weixin.qq.com/s/9bey04RiYhvTj2x8ZD268Q) and [《MoonBit Pearls Vol.04：Exploring Collaborative Programming with MoonBit (Part 1)》](https://mp.weixin.qq.com/s/Uc6uZuIIbOapOaVyZZ1ong), discussing dynamic programming and collaborative programming respectively.
- MoonBit's biweekly beta reports transitioned to monthly releases. The July 15th [monthly report](https://mp.weixin.qq.com/s/253cG9u57B1B0LVavgE2zQ) includes:  

  - Note: This update was originally scheduled for next week's report but released early due to previews of upcoming official activities.  
  - Added `!expr` syntax. Boolean negation now directly uses `!` instead of requiring the `not` function.  
  - Replaced `else` with `noraise` in `try .. catch .. else ..` syntax. This change addresses inconsistency since `else` here precedes pattern matching (not a code block). The old syntax is deprecated with compiler warnings.  
  - Enabled `noraise` return type annotations for functions. This improves type signature documentation and prevents automatic `raise` insertion in scenarios like:  
    ```mbt
    fn h(f: () -> Int raise) -> Int { ... }

    fn init {
        let _ = h(fn () { 42 }) // ok  
        let _ = h(fn () noraise { 42 }) // not ok  
    }
    ```  
  - Added `...` as a pattern matching placeholder for code omission.  
  - Introduced `moon coverage analyze` command for one-click code coverage detection and visualization of untested branches.  
  - Standard library preview: JSON type construction will be updated. Use recommended functions like `Json::number` for future compatibility.  
  - MoonBit Community will participate as an open-source partner at China RISC-V Summit 2025 (July 16-18). The event expects 1000+ professional attendees. Visit our booth to connect with MoonBit ambassadors.
