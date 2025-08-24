---
taxon: Theorem
title: shl-shr
---
> For all $0 \lt x \lt 2^{n+2}$,

$$ \text{while}(\text{not}(\text{test}(\cdot, n + 1)), \text{shl}, \text{while}(\text{even}, \text{shr}, x)) = \text{while}(\text{not}(\text{test}(\cdot, n + 1)), \text{shl}, x) $$

(Note: $\text{test}$ corresponds to `test_helper` in code, and $\cdot$ here is shorthand for the anonymous function: `fn { x => not(test_helper(x, n + 1)) }`)

**Proof** Intuitively, this indicates that if we first shift out all trailing zeros and then left-shift until the $(n+1)$-th bit is set, we can achieve the same result by entirely omitting the right-shift; shifting out zeros and then shifting them back should be an identity operation.

Formally, we prove by induction on $x$. If $x = xs : \text{I}$ is odd, the equality holds immediately since $\text{while}(\text{even}, \text{shr}, x) = x$. Otherwise, if $x = xs : \text{O}$, the trailing O is immediately discarded by $\text{shr}$ on the left-hand side. On the right-hand side, $xs : \text{O} = \text{shl}(xs)$, and since $xs \lt 2^{n+1}$, the extra $\text{shl}$ can be absorbed into the $\text{while}$ loop. The remaining cases follow from the induction hypothesis.