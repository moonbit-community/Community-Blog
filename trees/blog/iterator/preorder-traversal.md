---
title: MoonBit 实现树的先序遍历
collect: true
author: [illusory0x0](https://github.com/illusory0x0)
taxon: Blog
date: 2025-04-07
---

二叉树的定义

![define](moonbit/src/preorder_traversal.mbt:#include)

先序遍历一棵树

![preorder](moonbit/src/preorder_traversal.mbt:#include)

我们把 `Tree::preorder` 改写为手动控制栈的过程 `Tree::preorder_stack`

![preorder_stack](moonbit/src/preorder_traversal.mbt:#include)

下面的部分是用来测试**系统栈**版本和**手动控制栈**版本的一致性。

![final](moonbit/src/preorder_traversal.mbt:#include)
