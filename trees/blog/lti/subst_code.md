---
title: Type Parameter Substitution
collect: true
---

这里出现了一个新的记号 $[\overline{T}/\overline{X}]R$，
它表示将类型参数 $\overline{X}$ 替换为实际类型 $\overline{T}$ 后的结果类型。
这个记号在后续的代码中会频繁出现。
下面的代码定义 `mk_subst` 函数，用来生成一个类型替换映射，
还有一个 `apply_subst` 函数可以将这个映射应用到一个具体类型上。
$[\overline{T}/\overline{X}]R$ 就是通过 $\text{apply\_subst}(\text{mk\_subst}(\overline{X},\overline{T}), R)$ 得到的。

![subst](moonbit/src//lti/syntax.mbt#:include)