---
taxon: Theorem
---

$$ \forall x : \text{Bits}. \quad \text{lsb}(x) = \text{and}(x, \text{neg}(x)) $$

**Proof** By induction on $x$ (Translator's note: For notational convenience, we denote `pat_match(bs, b)` and `make(bs, b)` as $bs : b$, and omit the `op_` prefix of operation names).

* First, if $x = \text{Rep}(\text{O})$, it is straightforward to verify that $\text{lsb}(x) = \text{and}(x, \text{neg}(x)) = \text{Rep}(\text{O})$.
* Similarly, if $x = \text{Rep}(\text{I})$, both $\text{lsb}(x)$ and $\text{and}(x, \text{neg}(x))$ simplify to $\text{Rep}(\text{O}) : \text{I}$.
* If $x = xs : \text{O}$, then $\text{lsb}(x) = \text{lsb}(xs : \text{O}) = \text{lsb}(xs) : \text{O}$, while
  $$
  \begin{align*}
  & \text{and}(xs : \text{O}, \text{neg}(xs : \text{O})) \\
  = & \text{and}(xs : \text{O}, \text{inc}(\text{inv}(xs : \text{O}))) & \{ \text{definition of neg} \} \\
  = & \text{and}(xs : \text{O}, \text{inc}(\text{inv}(xs) : \text{I})) & \{ \text{definitions of inv and neg} \} \\
  = & \text{and}(xs : \text{O}, \text{inc}(\text{inv}(xs)) : \text{O}) & \{ \text{definition of inc} \} \\
  = & \text{and}(xs, \text{neg}(xs)) : \text{O} & \{ \text{definitions of and and neg} \} \\
  = & \text{lsb}(xs) : \text{O} & \{ \text{induction hypothesis} \}
  \end{align*}
  $$
* Next, if $x = xs : \text{I}$, then $\text{lsb}(xs : \text{I}) = \text{Rep}(\text{O}) : \text{I}$, and
  $$
  \begin{align*}
  & \text{and}(xs : \text{I}, \text{neg}(xs : \text{I})) \\
  = & \text{and}(xs : \text{I}, \text{inc}(\text{inv}(xs : \text{I}))) & \{ \text{definition of neg} \} \\
  = & \text{and}(xs : \text{I}, \text{inc}(\text{inv}(xs) : \text{O})) & \{ \text{definitions of inv and neg} \} \\
  = & \text{and}(xs : \text{I}, \text{inv}(xs) : \text{I}) & \{ \text{definition of inc} \} \\
  = & \text{and}(xs, \text{inv}(xs)) : \text{I} & \{ \text{definition of and} \} \\
  = & \text{Rep}(\text{O}) : \text{I} & \{ \text{bitwise AND of xs and its inverse is Rep(O)} \}
  \end{align*}
  $$
  For the last equality, we require a lemma stating that $\text{and}(xs, \text{inv}(xs)) = \text{Rep}(\text{O})$, which is intuitive and easily provable by induction.