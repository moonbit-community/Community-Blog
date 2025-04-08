---
title: Blog
---

社区成员可以自由贡献一些博客文章，可以是 MoonBit 的教学、杂谈、开发日记等等。
直接发起 PR 在 trees/blog 文件夹中添加文章即可，因为文章分节会需要包含多个文件，
建议写作者单独开一个文件夹来存放文章，并用一个主文件来包含其他的文件。
文章的头部需要包含一些元信息：

- `author`：作者的名字
- `date`：文章的日期，格式为 YYYY-MM-DD
- `title`：文章的标题
- `taxon`：文章的分类，通常都是 `Blog`

举个例子：

```md
---
author: CAIMEOX
date: 2025-04-01
title: MoonBit 开发日记
taxon: Blog
---
```
