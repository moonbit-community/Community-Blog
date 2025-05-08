---
taxon: Theorem
---

$$ \forall x : \text{Bits}. \quad \text{lsb}(x) = \text{and}(x, \text{neg}(x)) $$

**证明** 通过对 $x$ 进行归纳（译者注：为了便利证明书写，我们将 `pat_match(bs, b)` 和 `make(bs, b)` 记为 $bs : b$，运算名的 `op_` 前缀均省略。

* 首先，若 $x = \text{Rep}(\text{O})$，不难验证 $\text{lsb}(x) = \text{and}(x, \text{neg}(x)) = \text{Rep}(\text{O})$。
* 类似地，若 $x = \text{Rep}(\text{I})$，则 $\text{lsb}(x)$ 和 $\text{and}(x, \text{neg}(x))$ 均化简为 $\text{Rep}(\text{O}) : \text{I}$。
* 若 $x = xs : \text{O}$，则根据  $\text{lsb}(x) = \text{lsb}(xs : \text{O}) = \text{lsb}(xs) : \text{O}$，而
  $$
  \begin{align*}
  & \text{and}(xs : \text{O}, \text{neg}(xs : \text{O})) \\
  = & \text{and}(xs : \text{O}, \text{inc}(\text{inv}(xs : \text{O}))) & \{ \text{   neg } \} \\
  = & \text{and}(xs : \text{O}, \text{inc}(\text{inv}(xs) : \text{I})) & \{ \text{   inv 和 } \neg \} \\
  = & \text{and}(xs : \text{O}, \text{inc}(\text{inv}(xs)) : \text{O}) & \{ \text{   inc } \} \\
  = & \text{and}(xs, \text{neg}(xs)) : \text{O} & \{ \text{   } \text{and} \text{ 和 neg } \} \\
  = & \text{lsb}(xs) : \text{O} & \{ \text{ 归纳假设 } \}
  \end{align*}
  $$
* 接下来，若 $x = xs : \text{I}$，则根据  $\text{lsb}(xs : \text{I}) = \text{Rep}(\text{O}) : \text{I}$，有
  $$
  \begin{align*}
  & \text{and}(xs : \text{I}, \text{neg}(xs : \text{I})) \\
  = & \text{and}(xs : \text{I}, \text{inc}(\text{inv}(xs : \text{I}))) & \{ \text{   neg } \} \\
  = & \text{and}(xs : \text{I}, \text{inc}(\text{inv}(xs) : \text{O})) & \{ \text{   inv 和 } \neg \} \\
  = & \text{and}(xs : \text{I}, \text{inv}(xs) : \text{I}) & \{ \text{   inc } \} \\
  = & \text{and}(xs, \text{inv}(xs)) : \text{I} & \{ \text{   } \text{and} \} \\
  = & \text{Rep}(\text{O}) : \text{I} & \{ \text{ xs 与其反码的按位与为 Rep(O) } \}
  \end{align*}
  $$
  对于最后一个等式，我们需要一个引理，即 $\text{and}(xs, \text{inv}(xs)) = \text{Rep}(\text{O})$，这个引理应该很直观，并且可以通过归纳轻松证明。
