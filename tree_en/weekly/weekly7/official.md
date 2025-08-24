---
title: This Week's Official Highlights
---

- MoonBit has officially open-sourced the code for its official website [moonbitlang.cn](moonbitlang.cn) at [website](https://github.com/moonbitlang/website). Community members can now participate in the development of the MoonBit website.

- MoonBit has created a new repository [moonbit-evolution](https://github.com/moonbitlang/moonbit-evolution). All user-visible changes to MoonBit will be documented in this repository moving forward, enhancing transparency and traceability. Users can also discuss and propose changes here, marking a new phase of community-driven development for MoonBit.

- On June 24th, MoonBit published [an interview with Zhang Hongbo, founder of the MoonBit programming language](https://mp.weixin.qq.com/s/NSIU7Lw4_MYRAdW52HMWtw). The discussion covered MoonBit's design philosophy, development journey, core features, and industry insights. Key points include:

  - **MoonBit Overview**
    - **Core Positioning**: A new general-purpose programming language for developing websites, apps, backend services, etc. The Beta release is scheduled for June 18, 2025, transitioning from an "experimental technology" to an enterprise-ready tool.
    - **Core Philosophy**: "AI-native" – not aiming to *be* AI, but creating a language optimized for AI usage. Designed from syntax and type systems to error handling to address AI's needs in understanding, generating, and verifying code, solving pain points like code maintainability in AI programming.

  - **"AI-Native" Implementation & Design Choices**
    - **Philosophical Shift**: Less emphasis on minimizing syntax characters (as AI generates most code), focusing instead on balancing freedom (like Python/JS) and strictness (like Rust/Lean) to ensure reliability without exceeding AI's type system capabilities.
    - **Specific Designs**:
        - Uses `let x = 3` instead of Go-style `x := 3`. The `let` keyword provides a clear "new variable declaration" signal for AI, reducing ambiguity.
        - Native async and error handling mechanisms, more natural and syntactically lighter than Python, with compile-time error propagation tracking.
        - Powerful static type system. Automatically generates formal "signatures" (MBTI files) for each package, simplifying understanding and maintenance. Emphasizes "localization" to limit the impact of code changes.

  - **Comparison with AI Coding Tools & Team's AI Usage**
    - **Evaluation of General AI Tools**:
      - The team uses tools like Cursor and Copilot, finding smaller teams (e.g., Cursor) more agile and offering a better experience.
      - Believes the technical moat for such tools isn't high; real-time code completion provides more "emotional value," and conversational Agents aren't exceptionally high-barrier. Over-reliance risks creating "bottleneck" dependencies.
    - **Team's AI Usage**:
      - Uses AI extensively to boost productivity (e.g., multiple PRs per day).
      - Develops its own AI programming Agent, leveraging deep understanding of MoonBit's code structure to concurrently fix multiple bugs, outperforming general tools.

  - **MoonBit Beta & Ecosystem Strategy**
    - **Beta Significance**:
      - Rich language features covering core industrial development needs.
      - Syntax enters a stable phase, committing to avoid breaking changes.
      - Establishes formal community communication via an open RFC process.
    - **Ecosystem Cold Start Strategy**: Enables Python ecosystem reuse by compiling to C code, allowing direct calls to mature Python libraries and providing a gradual migration path.

  - **Founder Zhang Hongbo's Technical Journey**
    - 2009: Developed the "Wukong" animation language for undergrad thesis; researched "meta-programming languages" during Master's.
    - Left UPenn PhD to maintain OCaml compiler at Bloomberg. Developed BuckleScript (later ReScript) as a side project, which was deeply used by Facebook. Remotely maintained it for Facebook from 2017-2022.
    - Joined IDEA Research in 2022 and initiated the MoonBit project.

  - **Industry Perspectives & Advice**
    - **Business Model**: Short-term focus on licensing and services for large clients; long-term goal is a code delivery cloud platform delivering ready-to-use software services.
    - **Domestic Tech Environment**: Notes a lack of confidence and "talent scouts." Hopes MoonBit's success can inspire and drive industry chain development.
    - **Advice for Developers**: Intensively use AI tools while understanding their limits; encourages trying MoonBit and engaging early with its ecosystem.
    - **Advice for Young Talent in Foundational Tech**: Prepare for a long-term effort; gain substantial industry experience first.
