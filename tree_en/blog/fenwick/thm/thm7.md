---
title: sentinel
taxon: Theorem
---
> Let $n \ge 1$ and let $f : \text{Bits} \to \text{Bits}$ be a function such that
> 
> 1. $f(\text{set}(n + 1, x)) = \text{set}(n + 1, f(x))$ holds for any $0 \lt x \lt 2^n$, and  
> 2. $f(x) \lt 2^{n+1}$ holds for any $0 \lt x \lt 2^n + 2^{n-1}$.
> 
> Then for all $0 \lt x \lt 2^n$,  
> $$ \text{unshift}(n + 1, f(\text{shift}(n + 1, x))) = \text{atLSB}(f, x). $$

The proof is rather tedious and not particularly enlightening, so we omit it (an extended version containing the full proof is available on the author's [website](http://ozark.hendrix.edu/~yorgey/pub/Fenwick-ext.pdf)). However, we note that both `inc` and `dec` satisfy the criteria for $f$: as long as $n \ge 1$, incrementing or decrementing some $0 \lt x \lt 2^n$ does not affect the $(n+1)$-th bit, and incrementing or decrementing a number less than $2^n + 2^{n-1}$ will yield a result less than $2^{n+1}$. We can now combine all parts to prove that adding the LSB at each step is the correct way to implement `update`.