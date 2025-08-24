---
title: Validating Constraints on Algebraic Structures 
collect: true
---

When it comes to validating the axioms of algebraic structures, we are not without recourse. Although it's impossible to exhaust all possible validation scenarios from a completeness perspective, through carefully constructed test case collections, we can systematically verify the validity of axioms on specific instances. Leveraging [QuickCheck](https://github.com/moonbitlang/quickcheck.git), a powerful property-based testing framework, we achieve a paradigm shift from abstract algebraic axioms to executable specifications. In this process, the fundamental axioms of algebraic structures serve as the theoretical foundation guiding property formulation. Combined with automatically generated test data, this enables statistical validation of type implementations.

[+](/blog/lunaflow/quickcheck.md#:embed)

Property construction occupies a central position in the QuickCheck testing system. For algebraic structures, their axiomatic systems inherently possess verifiable characteristics: we can establish rigorous verification mechanisms in concrete implementations by directly mapping mathematical axioms to test properties. Consider a representative example from the [Linear-Algebra](https://github.com/Luna-Flow/linear-algebra) codebase: when defining the `Vector[T]` type representing vectors and its addition operation `op_add`, as a fundamental requirement of vector spaces, the addition operation must strictly satisfy commutativity and associativity. Specifically, for arbitrarily chosen vectors $\vec{u}, \vec{v}, \vec{w} \in V$, the following mathematical constraints must hold:

$$
\begin{align*}
\vec{u} + \vec{v} &= \vec{v} + \vec{u} \quad \text{(commutativity)} \\
\vec{u} + (\vec{v} + \vec{w}) &= (\vec{u} + \vec{v}) + \vec{w} \quad \text{(associativity)}
\end{align*}
$$

At the implementation level, this translates to the following test verification (note: here we assume the `Vector` type has correctly implemented the `Arbitrary` trait):

```moonbit
test "algebraic laws" {
    fn prop(a : Vector[Int], b) { a + b == b + a }
    fn prop(a : Vector[Int], b, c) { a + (b + c) == (a + b) + c }
    quick_check_fn!(fn {
        ((a : Vector[Int]), (b : Vector[Int])) => {
        guard a.length() == b.length() else { true }
        prop(a, b)
        }
    })
    quick_check_fn!(fn {
        ((a : Vector[Int]), (b : Vector[Int]), (c : Vector[Int])) => {
        guard a.length() == b.length() && b.length() == c.length() else { true }
        prop(a, b, c)
        }
    })
}
```

This paradigm of mechanically transforming mathematical axioms into executable verification mechanisms enables LunaFlow to leverage mathematical axiomatic systems, providing robust testing guarantees for implementation correctness.
