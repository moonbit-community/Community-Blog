---
title: Type Parameter Substitution
collect: true
---

A new notation $[\overline{T}/\overline{X}]R$ appears here,
representing the resulting type after substituting the type parameters $\overline{X}$ with the actual types $\overline{T}$.
This notation will appear frequently in subsequent code.
The following code defines the `mk_subst` function to generate a type substitution map,
and an `apply_subst` function that applies this map to a concrete type.
$[\overline{T}/\overline{X}]R$ is obtained through $\text{apply\_subst}(\text{mk\_subst}(\overline{X},\overline{T}), R)$.

![subst](moonbit/src//lti/syntax.mbt#:include)
