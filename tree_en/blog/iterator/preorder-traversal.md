---
title: Implementing Preorder Traversal of Trees in MoonBit
collect: true
author: [illusory0x0](https://github.com/illusory0x0)
taxon: Blog
date: 2025-04-07
---

### Definition of a Binary Tree

![define](moonbit/src/preorder_traversal/preorder_traversal.mbt#:include)

### Preorder Traversal of a Tree

![preorder](moonbit/src/preorder_traversal/preorder_traversal.mbt#:include)

We rewrite `Tree::preorder` as a manually controlled stack process `Tree::preorder_stack`

![preorder_stack](moonbit/src/preorder_traversal/preorder_traversal.mbt#:include)

The following section is used to test the consistency between the **system stack** version and the **manually controlled stack** version.

![final](moonbit/src/preorder_traversal/preorder_traversal.mbt#:include)
