---
title: Tools
---

若是文件粒度的微小更改，可以在 Github 直接编辑文件。
如果涉及多文件等复杂情况，您可能需要在本地部署工具进行预览。
下面是将 Community-Blog 克隆到本地的命令 (我们这里使用了一些 git 子模块，比通常的 `git clone` 多一个步骤)：

```bash
git clone git@github.com:moonbit-community/community-blog.git
cd community-blog
git submodule update --init --recursive
```

确保你安装了 Rust 和 Node.js 环境，在项目根目录下运行如下指令安装必要依赖项：

```bash
cargo install --git https://github.com/kokic/kodama.git
npm i
```

实时预览只需运行 `npm run dev` ，在浏览器访问 `localhost:5173` 即可。

在提交之前我们推荐您运行 `typos`、`zhlint` 和 `autocorrect --fix` 命令来检查和修复拼写错误。
其安装可以参考下面的链接：

- [zhlint](https://github.com/zhlint-project/zhlint)
- [how to install typos](https://github.com/crate-ci/typos?tab=readme-ov-file#install)
- [how to install autocorrect](https://github.com/huacnlee/autocorrect?tab=readme-ov-file#installation)
