---
taxon: Theorem
title: shl-shr
---
> 对于所有 $0 \lt x \lt 2^{n+2}$，

$$ \text{while}(\text{not}(\text{test}(\cdot, n + 1)), \text{shl}, \text{while}(\text{even}, \text{shr}, x)) = \text{while}(\text{not}(\text{test}(\cdot, n + 1)), \text{shl}, x) $$

（注：$\text{test}$ 在代码中是 `test_helper`，$\cdot$ 在此处是匿名函数简写： `fn { x => not(test_helper(x, n + 1)) }`）

**证明** 直观上，这表明如果我们先移出所有零位，然后左移直到第 $n+1$ 位被设置，这可以通过完全忘记右移来获得相同的结果；移出零位然后再将它们移回来应该是恒等操作。

形式上，证明通过对 $x$ 进行归纳。如果 $x = xs : \text{I}$ 为奇数，等式立即成立，因为 $\text{while}(\text{even}, \text{shr}, x) = x$。否则，如果 $x = xs : \text{O}$，在左侧，O 会被 $\text{shr}$ 立即丢弃，而在右侧，$xs : \text{O} = \text{shl}(xs)$，并且由于 $xs \lt 2^{n+1}$，额外的 $\text{shl}$ 可以被吸收到 $\text{while}$ 循环中。剩下的就是归纳假设。
