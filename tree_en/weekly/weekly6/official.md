---
title: This Week's Official Highlights
---

- On June 16, MoonBit officially released an [official weekly report](https://mp.weixin.qq.com/s/QNYVLKpVRCLAJ0EuwzzxHA). This marks the final update before the beta version, indicating the syntax is approaching stabilization. Key updates include:

  - The `!` syntax for errors is replaced by the `raise` keyword to denote errors.
  - The syntax for defining error types `type! T ..` is changed to `suberror T ..`. Migration can be automated via the formatter.
  - For functions, the `f!(..)/f?(..)` syntax will be deprecated. The type parameter syntax for functions also changes from `fn f[..](..)` to `fn[..] f(..)`.
  - `typealias`/`traitalias` syntax update: `=` is replaced with `as`. This migration can be automated via the formatter.
  - Deprecation of multi-argument `loop` in favor of tuple parameters to align with `match`. Multi-argument `loop` should use tuples to ensure pattern matching consistency.
  - New rule for explicit trait implementation: `impl` is required even with default methods. For types needing only default implementations, use `impl Trait for Type`.
  - Deprecation of dot-calling for external type `impl`, replaced by local method extensions. This complex change is detailed in the original report:
    Previously, `impl` for external types allowed dot-calling within the current package. This was refactoring-unsafe: upstream method additions could alter downstream behavior. Thus, this feature is deprecated. Instead, MoonBit now supports locally defining new methods for external types using standard method syntax. These methods have the following characteristics:
    - They cannot be `pub` to prevent cross-package conflicts.
    - Compiler warns if upstream (the type's package) defines a same-named method.
    - Local methods have the highest priority in method resolution.
    Resolution rules for `x.f(..)` now follow (highest to lowest priority):
    - Local methods
    - Methods from the type's package
    - `impl` from the type's package

  - `Json` literals now automatically invoke `ToJson::to_json`, simplifying code:
    ```mbt
    let x = 42
    // Previously
    let _ : Json = { "x": x.to_json() }
    // Now
    let _ : Json = { "x": x }
    ```
  - Virtual packages now support abstract types: interface declarations with customizable multi-implementation types.
  - Added warnings for reserved words that may become keywords in the future.
  - New arrow function syntax `(..) => expr` simplifies simple anonymous functions:
    ```mbt
    test {
        let arr = [ 1, 2, 3 ]
        arr
        .map(x => x + 1) // Parentheses optional for single parameters
        .iter2()
        .each((i, x) => println("\{i}: \{x}"))
    }
    ```
  - Matrix functions are deprecated to streamline syntax. Matrix functions like `fn { .. => expr }` should use arrow functions; others should use explicit `fn` and `match`.
  - The `xx._` syntax for converting new types to their underlying representation is deprecated due to visual ambiguity with partial application (`_.f(..)`). Instead, each new type now auto-generates a `.inner()` method. Migration can be automated via the formatter.
  - MoonBit now warns for ambiguous operator precedence combinations (e.g., `<<` and `+`). Add parentheses manually or via the formatter to resolve warnings.
  - New `letrec` and `and` keywords for local mutually recursive functions:
    ```mbt
    fn main {
        letrec even = fn (x: Int) { ... } // anonymous function
        and odd = x => ...                // arrow function
    }
    ```
    Right-hand sides must be function values (anonymous or arrow functions). Implicit mutual recursion via `fn` is deprecated, though self-recursion remains valid.
  - `fnalias` can no longer create aliases for non-function values. Use `let` for non-function type aliases.
  - Leveraging new error polymorphism, standard library higher-order functions like `Array::each` now support error-throwing callbacks.
  - `main` package testing support: `moon test` runs tests, `moon run` executes the main program (previously tests were prohibited in `main` packages).
  - IDE codelens now supports running tests in documentation.
  - `moon test` and `moon check` now include tests in documentation by default.

- MoonBit was featured at two major tech events from June 13-15, 2025: the 3rd INNOTECH Innovation Carnival hosted by HKUST(GZ), and the 12th GIAC (Global Internet Architecture Conference) by msup. At GIAC, Zhang Hongbo, Chief Scientist of the Basic Software Center at IDEA Research Institute and Head of the MoonBit Platform, delivered a keynote titled "Vertical Integration of AI Programming in MoonBit".
- On June 18, 2025, CSDN published an article titled "20 Years in the Making: China's First Industrial-Grade Programming Language Enters Beta Version", detailing MoonBit's progress and marking its official beta release.
- MoonBit's Pearls series updated with its second article: [MoonBit Pearls Vol.02: Object-Oriented Programming in MoonBit](https://mp.weixin.qq.com/s/mDsY4fnGmggk9JSH1sLE2g). Written by Liu Ziyue from the MoonBit team, it explores OOP through an RPG game development example.
