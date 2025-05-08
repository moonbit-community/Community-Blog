---
title: Two's complement binary 
collect: true
---

通常用于实现芬威克树的位技巧依赖于二进制数的二进制补码表示法，该表示法允许以统一的方式表示正数和负数；例如，一个全由 1 组成的位串表示 -1。因此，我们现在转向开发一个嵌入 MoonBit 的领域特定语言，用于操作二进制补码表示。

首先，我们定义一个位 (Bit) 的类型，附带用于求反、逻辑与和逻辑或的函数（注：还有 `to_enum` 和 `from_enum` 的实现，用于实现和 `Int` 类型的互转，在此省略）:
![bit](moonbit/src//fenwick/bit.mbt:#include)

接下来，我们必须定义位串，即位的序列。与其固定一个特定的位宽，不如使用无限位串会更加优雅[^3]。使用 [Lazy List](https://github.com/CAIMEOX/lazy-list) 来表示潜在的无限位串似乎颇具诱惑力，但这会导致一系列问题。例如，无限列表的相等性是不可判定的，而且通常没有办法将一个无限的位列表转换回一个 `Int` —— 我们如何知道何时停止？(译者注：Lazy List 在 MoonBit 中也容易出现栈溢出的问题，比原文使用的 Haskell `List` 还要更坏一些) 事实上，这些实际问题源于一个更根本的问题：无限位列表对于二进制补码位串来说是一个糟糕的表示，因为它包含“垃圾”，即那些不对应于我们预期语义域中值的无限位列表。例如，`cycle([I, O])` 是一个永远在 `I` 和 `O` 之间交替的无限列表，但它并不代表一个有效的二进制补码整数编码。更糟糕的是非周期列表，比如在每个素数索引处为 `I` 而其他地方均为 `O` 的列表。

实际上，我们想要的位串是那些最终恒定的串，即那些最终趋于无限长的全零尾部（代表非负整数）或全一尾部（代表负整数）的串。每个这样的串都有一个有限的表示，因此在 MoonBit 中直接编码最终恒定的位串，不仅能去除垃圾，还能辅助编写一些优雅且停机的算法。

![bits](moonbit/src//fenwick/bits.mbt:#include)

`Rep(b)` 代表一个由无限个位 `b` 组成的序列，而 `Snoc(bs, b)` 则代表位串 `bs` 后跟一个末位 `b`。我们使用 `Snoc` 而非 `Cons`，是为了与我们通常书写位串的方式相匹配，即最低有效位在最后。另请注意在 `Snoc` 的 `Bits` 字段上使用了严格性注解；这是为了排除仅使用 `Snoc` 构成的无限位列表，例如 `bs = Snoc(Snoc(bs, O), I)`。换言之，构造类型为 `Bits` 的非底层值的唯一方法是拥有一个有限的 `Snoc` 序列，最终由一个 `Rep` 终止。

尽管我们已经消除了垃圾值，但仍存在一个问题：同一个值可能存在多个不同的表示。例如，`Snoc(Rep(O)), O)` 和 `Rep(O)` 都代表包含全零的无限位串。在 Haskell 中可以通过精心构造一个双向模式（Pickering et al., 2016）来解决这个问题，但是 MoonBit 并没有 `ViewPatterns` 的概念，所以我们必须手动调整模式匹配，下面的 `pat_match` 函数可以从一个 `Bits` 中匹配出一个 `Bits` 和一个 `Bit`，`make` 则是其构造对偶，可以从一个 `Bits` 和一个 `Bit` 中构造出一个 `Bits`。

![pattern](moonbit/src//fenwick/bits.mbt:#include)

使用 `.pat_match()` 进行匹配时，会潜在地将一个 `Rep` 展开一步成为 `Snoc`，这样我们就可以假装 `Bits` 值总是由 `make` 构造的。反之，使用 `make` 构造一个 `Bits` 值时，如果我们恰好将一个相同的位 `b` 追加到一个现有的 `Rep b` 上，它将什么也不做。这确保了只要我们坚持使用 `make` 和 `pat_match` 而从不直接使用 `Snoc`，`Bits` 值将始终被规范化，使得末端的 `Rep(b)` 立即跟随着一个不同的位。
读者可能会认为 `pat_match` 中的 `guard` 并不安全，实际上它确实足以处理 `Bits` 类型的所有可能输入。然而，为了获得能停机的算法，我们通常会包含一个或多个针对 `Rep` 的特殊情况。

让我们从一些用于在 `Bits` 和 `Int` 之间转换以及显示 `Bits`（仅用于测试目的）的函数开始。

![conversion](moonbit/src//fenwick/bits.mbt:#include)

trait `Show` 的实现：

![show](moonbit/src//fenwick/bits.mbt:#include)

让我们用 [QuickCheck](https://github.com/moonbitlang/quickcheck/) 来测试一下，验证我们的转换函数：

![test1](moonbit/src//fenwick/bits.mbt:#include)

现在我们可以开始在 `Bits` 上实现一些基本操作了。首先，递增和递减可以递归地实现如下：

![inc_dec](moonbit/src//fenwick/bits.mbt:#include)

一个位序列的最低有效位（Least Significant Bit, LSB）可以定义如下：

![lsb](moonbit/src//fenwick/bits.mbt:#include)

注意，我们为 `Rep(O)` 添加了一个特殊情况，以确保 `lsb` 是全函数。严格来说，`Rep(O)` 没有最低有效位，因此定义 `lsb(Rep(O)) = Rep(O)` 似乎是合理的。

![test2](moonbit/src//fenwick/bits.mbt:#include)

按位逻辑与可以直截了当地定义。注意，我们只需要两种情况；如果输入的有限部分长度不同，与 `pat_match` 的匹配会自动扩展较短的一个以匹配较长的那个。

![bit_and](moonbit/src//fenwick/bits.mbt:#include)

按位取反同样显然：

![bit_not](moonbit/src//fenwick/bits.mbt:#include)

上述函数遵循熟悉的模式。我们可以很容易地将它们推广到作用于任意元素类型的最终恒定流，然后用泛型的 `zipWith` 来实现 `land`，用 `map` 来实现 `inv`。然而，就目前的目的而言，我们不需要这种额外的通用性。

我们用通常的进位传播算法来实现加法，并附带一些针对 `Rep` 的特殊情况。
(译者注：原文中 `op_add` 的实现是非穷尽的，下面是修正后的版本)：

![op_add](moonbit/src//fenwick/bits.mbt:#include)

不难发现这个加法定义是能够停机并产生正确结果的；但我们也可以通过用 QuickCheck 来尝试一下，从而获得相当的信心：

![test_add](moonbit/src//fenwick/bits.mbt:#include)

最后，下面这个求反的定义对于任何学过二进制补码算术的人来说可能都很熟悉；我将其留作一个练习，供感兴趣的读者证明对于所有 `x : Bits`，都有 $x + \text{neg } x = \text{Rep(O)}$。

![op_neg](moonbit/src//fenwick/bits.mbt:#include)

现在我们拥有了揭开芬威克树实现中第一个谜团的工具。

[+](/blog/fenwick/thm/thm2.md#:embed)

最后，为了表达我们将在下一节中开发的索引转换函数，我们的 DSL 中还需要一些其他东西。首先是一些用于设置和清除单个位以及测试特定位是否已设置的函数：

![helpers](moonbit/src//fenwick/bits.mbt:#include)

我们还需要的是左移和右移，以及一个通用的 `while` 组合子，它迭代一个给定的函数，返回第一个使得谓词为假的迭代结果。

![shift](moonbit/src//fenwick/bits.mbt:#include)

[^3]: 部分读者或许能认出无限二进制补码位串即为二进数，也即 p 进数在特定情况 $p=2$ 时的形式，但我们的论述并不依赖于理解此关联。
