---
title: sentinel
taxon: Theorem
---
> 令 $n \ge 1$ 且令 $f : \text{Bits} \to \text{Bits}$ 是一个函数，使得
> 
> 1. $f(\text{set}(n + 1, x)) = \text{set}(n + 1, f(x))$ 对于任何 $0 \lt x \lt 2^n$ 成立，且
> 2. $f(x) \lt 2^{n+1}$ 对于任何 $0 \lt x \lt 2^n + 2^{n-1}$ 成立。
> 
> 那么对于所有 $0 \lt x \lt 2^n$，
> $$ \text{unshift}(n + 1, f(\text{shift}(n + 1, x))) = \text{atLSB}(f, x). $$

证明相当繁琐但并非特别具有启发性，因此我们省略它（一个包含完整证明的扩展版本可以在作者的[网站](http://ozark.hendrix.edu/~yorgey/pub/Fenwick-ext.pdf)上找到）。然而，我们确实注意到 `inc` 和 `dec` 都符合 $f$ 的标准：只要 $n \ge 1$，对某个 $0 \lt x \lt 2^n$ 进行递增或递减不会影响第 $(n+1)$ 位，并且对一个小于 $2^n + 2^{n-1}$ 的数进行递增或递减的结果将是一个小于 $2^{n+1}$ 的数。我们现在可以将所有部分组合起来，证明在每一步加上 LSB 是实现 `update` 的正确方法。