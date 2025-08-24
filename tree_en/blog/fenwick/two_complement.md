---
title: Two's complement binary 
collect: true
---

The bit tricks commonly used to implement Fenwick trees rely on the two's complement representation of binary numbers, which allows for a uniform representation of both positive and negative numbers; for example, a bit string consisting of all ones represents -1. Therefore, we now turn to developing a domain-specific language embedded in MoonBit for manipulating two's complement representations.

First, we define a type `Bit` with functions for negation, logical AND, and logical OR (note: implementations of `to_enum` and `from_enum` for conversion to/from `Int` are omitted here):
![bit](moonbit/src//fenwick/bit.mbt#:include)

Next, we must define bit strings, i.e., sequences of bits. Rather than fixing a specific bit width, it would be more elegant to use infinite bit strings[^5]. Representing potentially infinite bit strings using [Lazy List](https://github.com/CAIMEOX/lazy-list) might seem tempting, but this leads to several issues. For instance, equality of infinite lists is undecidable, and there is generally no way to convert an infinite bit list back to an `Int`—how would we know when to stop? (Translator's note: Lazy Lists in MoonBit are also prone to stack overflow issues, worse than Haskell's `List` used in the original) In fact, these practical issues stem from a more fundamental problem: infinite bit lists are a poor representation for two's complement bit strings because they contain "garbage"—infinite bit lists that do not correspond to values in our intended semantic domain. For example, `cycle([I, O])` is an infinite list alternating forever between `I` and `O`, but it does not represent a valid two's complement integer encoding. Worse still are non-periodic lists, such as one with `I` at prime indices and `O` elsewhere.

What we actually desire are bit strings that are eventually constant—those that eventually settle into an infinite tail of all zeros (representing non-negative integers) or all ones (representing negative integers). Each such string has a finite representation, so directly encoding eventually constant bit strings in MoonBit not only eliminates garbage but also facilitates writing elegant, terminating algorithms.

![bits](moonbit/src//fenwick/bits.mbt#:include)

`Rep(b)` represents an infinite sequence of bit `b`, while `Snoc(bs, b)` represents the bit string `bs` followed by a trailing bit `b`. We use `Snoc` instead of `Cons` to match the conventional way of writing bit strings with the least significant bit last. Note also the strictness annotation on the `Bits` field of `Snoc`; this prevents infinite bit lists constructed solely with `Snoc`, such as `bs = Snoc(Snoc(bs, O), I)`. In other words, the only way to construct non-bottom values of type `Bits` is to have a finite sequence of `Snoc` terminated by a `Rep`.

Although we've eliminated garbage values, another issue remains: multiple distinct representations may correspond to the same value. For example, both `Snoc(Rep(O), O)` and `Rep(O)` represent the infinite bit string of all zeros. In Haskell, this could be resolved with bidirectional patterns (Pickering et al., 2016), but MoonBit lacks `ViewPatterns`, so we must manually adjust pattern matching. The `pat_match` function below matches a `Bits` into a `Bits` and a `Bit`, while `make` is its constructive dual, building a `Bits` from a `Bits` and a `Bit`.

![pattern](moonbit/src//fenwick/bits.mbt#:include)

When matching with `.pat_match()`, a `Rep` may be expanded one step into a `Snoc`, allowing us to pretend that `Bits` values are always constructed via `make`. Conversely, when constructing a `Bits` value with `make`, appending a bit `b` to an existing `Rep b` does nothing. This ensures that as long as we consistently use `make` and `pat_match` instead of directly using `Snoc`, `Bits` values will always be normalized such that the trailing `Rep(b)` is immediately preceded by a different bit.  
Readers might question the safety of the `guard` in `pat_match`, but it suffices to handle all possible inputs of type `Bits`. However, for terminating algorithms, we typically include one or more special cases for `Rep`.

Let's begin with functions for converting between `Bits` and `Int`, and for displaying `Bits` (for testing purposes only).

![conversion](moonbit/src//fenwick/bits.mbt#:include)

Implementation of the `Show` trait:

![show](moonbit/src//fenwick/bits.mbt#:include)

Let's test this using [QuickCheck](https://github.com/moonbitlang/quickcheck/) to verify our conversion functions:

![test1](moonbit/src//fenwick/bits.mbt#:include)

Now we can implement some basic operations on `Bits`. First, increment and decrement can be implemented recursively as follows:

![inc_dec](moonbit/src//fenwick/bits.mbt#:include)

The least significant bit (LSB) of a bit sequence can be defined as:

![lsb](moonbit/src//fenwick/bits.mbt#:include)

Note we added a special case for `Rep(O)` to ensure `lsb` is total. Strictly speaking, `Rep(O)` has no least significant bit, so defining `lsb(Rep(O)) = Rep(O)` seems reasonable.

![test2](moonbit/src//fenwick/bits.mbt#:include)

Bitwise AND can be straightforwardly defined. Note we only need two cases; if inputs have different finite lengths, matching with `pat_match` automatically extends the shorter one to match the longer.

![bit_and](moonbit/src//fenwick/bits.mbt#:include)

Bitwise negation is similarly obvious:

![bit_not](moonbit/src//fenwick/bits.mbt#:include)

These functions follow a familiar pattern. We could generalize them to operate on eventually constant streams of any element type and implement `land` with a generic `zipWith`, and `inv` with `map`. However, for our current purposes, this extra generality is unnecessary.

We implement addition using the standard carry propagation algorithm, with special cases for `Rep`.  
(Translator's note: The original `op_add` implementation was non-exhaustive; below is the corrected version):

![op_add](moonbit/src//fenwick/bits.mbt#:include)

It's not difficult to see that this addition definition terminates and produces correct results; but we can also gain confidence by testing it with QuickCheck:

![test_add](moonbit/src//fenwick/bits.mbt#:include)

Finally, the following negation definition will be familiar to anyone who has studied two's complement arithmetic; I leave it as an exercise for the interested reader to prove that for all `x : Bits`, $x + \text{neg } x = \text{Rep(O)}$.

![op_neg](moonbit/src//fenwick/bits.mbt#:include)

We now have the tools to unravel the first mystery in the Fenwick tree implementation.

[+](/blog/fenwick/thm/thm2.md#:embed)

Finally, to express the index transformation functions we'll develop in the next section, we need a few more elements in our DSL. First, functions to set, clear, and test individual bits:

![helpers](moonbit/src//fenwick/bits.mbt#:include)

We also need left and right shifts, and a generic `while` combinator that iterates a given function, returning the first result where the predicate becomes false.

![shift](moonbit/src//fenwick/bits.mbt#:include)

[^5]: Some readers may recognize infinite two's complement bit strings as binary numbers, i.e., the case $p=2$ of p-adic numbers, but our discussion does not rely on understanding this connection.
