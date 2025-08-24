---
title: Tools
---

For minor changes at the file level, you can edit files directly on GitHub.
If you're dealing with complex scenarios involving multiple files, you may need to deploy tools locally for preview.
Below are the commands to clone Community-Blog locally (we use git submodules here, which adds an extra step compared to a regular `git clone`):

```bash
git clone git@github.com:moonbit-community/community-blog.git
cd community-blog
git submodule update --init --recursive
```

Ensure you have Rust and Node.js environments installed. Run the following commands in the project root directory to install Kodama and Node.js dependencies:

```bash
cargo install --git https://github.com/kokic/kodama.git --rev 323f97cf023c8a605f9ef986aba2fc34888abeed
npm i
```

For real-time preview, simply run `npm run dev` and visit `localhost:5173` in your browser.

Before submitting, we recommend running `typos`, `zhlint`, and `autocorrect --fix` commands to check and fix spelling errors.
Refer to the following links for installation instructions:

- [zhlint](https://github.com/zhlint-project/zhlint)
- [how to install typos](https://github.com/crate-ci/typos?tab=readme-ov-file#install)
- [how to install autocorrect](https://github.com/huacnlee/autocorrect?tab=readme-ov-file#installation)
