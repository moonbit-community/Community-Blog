---
title: Requirements 
---

Below are some simple formatting requirements applicable to all articles in Community-Blog:

- Correctly use markdown or typst formatting.
- Use full-width punctuation for Chinese, ending with a period. No space between words/formulas and full-width punctuation.
- Include a space between Chinese content and Western content (including words and formulas) for visual clarity.
- Ensure code content (especially MoonBit code) is well-formatted.
- **Do not** use markdown/typst's native headings for section hierarchy. Article sections should be split into separate files and included in the main file using kodama's embedding feature.
- Use absolute paths for embedded files, with the `trees` folder as the root directory. For example, this file's path is `/contribution/requirement.md`.
- Use absolute paths uniformly for references within kodama. Open the `community-blog/trees` directory in VsCode to enable jump and auto-completion features.

Additionally, for submitted PRs, we expect PR titles to comply with [Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/) specifications and clearly indicate the contribution type, such as:

```plaintext
feat: add a new community information for weekly
fix: fix typo for knowledge base
refactor: refactor the doc structure
```
