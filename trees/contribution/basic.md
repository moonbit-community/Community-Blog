---
title: Basic
---

Community-Blog 基于 [Kodama](https://github.com/kokic/kodama) 框架编写，同时支持 markdown 与 typst 编写，并且有类 forest 结构。

关于该框架的具体使用方法可以参见原框架的文档，但在 Community-Blog 中，我们认为大部分情况下您只需要拥有基本的 markdown 编写知识和排版经验即可。

我们的 Github 存储库在 https://github.com/moonbit-community/community-blog，您可以前往这里对 Blog 进行贡献。

您可以这样实现 Community-Blog 的本地部署与实时预览：

```bash
cargo install --git https://github.com/kokic/kodama.git
git clone git@github.com:moonbit-community/community-blog.git
cd community-blog
npm i
npm run dev
```
