---
title: Requirements 
---

下面是一些关于排版的简单要求，适用于 Community-Blog 中的全部文章：

- 正确使用 markdown 或者 typst 格式。
- 中文要用全角标点，末尾需要用句号，单词/公式和全角标点之间无空格。
- 中文内容与西文内容（包括单词与公式）之间需要有空格以保证美观。
- 代码内容（尤其是 MoonBit 代码）请确保格式化良好。
- **不**使用 markdown / typst 自带的标题来分级，文章分节应当划分到不同的文件，并使用 kodama 的嵌入功能包含到主文件中。
- 嵌入文件均采用绝对路径，以 `trees` 文件夹为根目录。例如本文件的路径是 `/contribution/requirement.md`。

另外，对于发出的 PR，我们希望 PR 标题可以符合 [约定式提交](https://www.conventionalcommits.org/zh-hans/v1.0.0/) 的要求，并且可以标注贡献的部分，比如：

```plaintext
feat: add a new community information for weekly
fix: fix typo for knowledge base
refactor: refactor the doc structure
```
