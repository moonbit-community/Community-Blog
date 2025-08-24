---
title: This Week's Official Highlights
---

- On May 6th, MoonBit officially released an [official weekly report](https://mp.weixin.qq.com/s/AzdB_J7dI5hzRYo0QAkA6g), featuring syntax and toolchain updates:
  - Implementation of traits will exclusively support explicit implementation via `impl T for A ...` for type `A` to implement trait `T`;
  - New syntactic sugar: Allows using `_` as a placeholder for pending parameters to simplify anonymous function creation;
  - `fnalias` supports creating aliases for methods of types and traits;
  - All pragmas have been removed, with attributes fully replacing them in the future;
  - Implemented the `#internal` attribute to provide warnings for external users of public APIs;
  - Added warnings for potentially ambiguous usage of loop arguments within `loop`;
  - Enabled implicit type conversions from `Array` to `ArrayView`, and from `Bytes` to `@bytes.View`;
  - `moon` now supports the `bench` subcommand for executing benchmark performance tests.
- On May 9th, MoonBit announced the [Open Source Summer Program](https://mp.weixin.qq.com/s/bc8xkj04cMZ9bBBc-73GbQ):
  - Program Introduction: Open Source Summer is a summer initiative launched and supported by the "Open Source Software Supply Chain Lighting Plan" of the Institute of Software, Chinese Academy of Sciences. It collaborates with global open-source communities to provide university students worldwide with open-source project tasks. Students can participate in open-source projects under the guidance of experienced developers, enhance technical skills, learn about open-source culture, and earn cash rewards and certificates of honor upon successful completion.
  - MoonBit Project List:
    - Project 1: Exploration and implementation of Qt bindings based on MoonBit;
    - Project 2: Visual Studio Code plugin for structured find/replace using tree-sitter.mbt;
    - Project 3: UI component library based on MoonBit and TEA architecture.
  - Participation Method & Timeline:
    - How to participate: Students log in to the [Open Source Summer official website](https://summer-ospp.ac.cn), browse MoonBit project listings, communicate with mentors, and submit project proposals as required. Formal participation begins after proposal approval.
    - Timeline: Project selection and proposal preparation start on May 9; Application deadline: June 9 at 18:00 UTC+8; Proposal review: June 10–29; Selected projects announced: June 30; Development period: July 1–September 30; Final review (PR/MR merging & mentor evaluation): October 1–31; Committee results review: November 1–8; Final results announced: November 9; Annual outstanding student selection: November.
- MoonBit Regional Ambassador Recruitment Launched!
  - MoonBit Regional Ambassadors serve as core bridges connecting technology and communities. As official representatives of MoonBit—a next-generation programming language for the AI era—you will maximize your influence within your region (universities, tech communities, or cities) by promoting MoonBit's technical vision, engaging local developer communities, and leading high-quality technical exchanges and collaborations.
  - Recruitment Process & Benefits:
    - Process: Application → Resume review → Package submission review → Interview → Contract signing → Training & onboarding.
    - Benefits: Officially certified ambassador credentials, continuous training and support, competitive compensation and incentives, participation in MoonBit's core ecosystem development, and opportunities to expand professional networks and influence.
- MoonBit Supports Domestic Chip Development—Performance Rivals C  
  Leveraging its Native backend, MoonBit [successfully eliminates the dependency on WebAssembly, enabling native code execution on embedded hardware](https://www.moonbitlang.cn/blog/moonbit-esp32#%E5%9C%A8-esp32-c3-%E4%B8%8A%E5%AE%9E%E7%8E%B0%E7%94%9F%E5%91%BD%E6%B8%B8%E6%88%8F). Demonstrated through "Conway's Game of Life" on the ESP32-C3 chip, MoonBit matches C in speed while significantly enhancing code readability and development experience via modern language features like pattern matching and labeled parameters. This offers an efficient solution combining native-level execution efficiency with contemporary development practices.  
  Notably, this case utilizes the [moonbit-esp32](https://github.com/moonbit-community/moonbit-esp32) package developed by contributor [lijunchen](https://github.com/lijunchen), which acts as a critical bridge providing bindings between MoonBit and core components of ESP-IDF.
