---
title: Local Type Argument Synthesis
collect: true
---

So far, we have defined the type rules for the core language, 
but we are still far from our goal: the core language requires numerous annotations, 
including explicitly providing type arguments during polymorphic instantiation. 
Since this occurs frequently in code, it becomes the primary pain point we aim to address in this section.

This is the goal of **Local Type Argument Synthesis**: allowing programmers to safely omit type arguments when calling polymorphic functions, writing $\text{id}(3)$ instead of $\text{id}[\mathbb{Z}](3)$. However, omitting type arguments introduces a core challenge: for a given application like $\text{id}(x)$ (where $x : \mathbb{Z}$ and $\mathbb{Z} \lt: \mathbb{R}$), there are often multiple valid type argument instantiations, such as $\text{id}[\mathbb{Z}](x)$ or $\text{id}[\mathbb{R}](x)$ here. We must establish a clear criterion for selection: choose the type argument that yields the most precise (i.e., smallest) result type for the entire application expression. In the $\text{id}(x)$ example, since the result type $\mathbb{Z}$ of $\text{id}[\mathbb{Z}](x)$ is a subtype of $\mathbb{R}$ (the result type of $\text{id}[\mathbb{R}](x)$), the former is clearly the superior and more informative choice.

However, this locally optimal "best result type" strategy is not universally applicable. In some cases, a "best" solution may not exist. For example, consider a function $f$ with type $\forall X. () \to (X \to X)$. For the application $f()$, both $f[\mathbb{Z}]()$ and $f[\mathbb{R}]()$ are valid completions, yielding result types $\mathbb{Z} \to \mathbb{Z}$ and $\mathbb{R} \to \mathbb{R}$ respectively. These function types are **incomparable** under the subtype relation, so no unique minimal result type exists. In such scenarios, local synthesis fails.

Recalling our earlier core language definition, we required application constructs to take the form $e[\overline{T}](\overline{e})$, 
meaning we manually specified type arguments $\overline{T}$. Rule `App` could compute the result type based on these arguments. 
Now, to make the language simpler and more ergonomic, we allow omitting type arguments $\overline{T}$. We update the language construct as follows:

![spec](moonbit/src//lti/syntax.mbt#:include)

This introduces a new expression structure `EAppI(Expr, Array[Expr])`, corresponding to the type-argument-omitted form. 
(For later discussion convenience, we also add the `EAbsI` construct here.) 
We now require a new rule:

$$
\frac{\text{magic we don't know}}{\Gamma \vdash f (\overline{e}) : [\overline{T}/\overline{X}]R} \quad (\text{App-Magic})
$$

As humans, we can intuitively formulate rules or even design declarative rules that cannot be implemented as code, 
precisely defining "what constitutes a correct, optimal type argument inference":

$$
\frac{
    \begin{array}{l}
    \Gamma \vdash f : \forall \overline{X}. \overline{T} \to R
    \qquad \exists \overline{U}
    \\
    \Gamma \vdash \overline{e} : \overline{S}
    \qquad
    |\overline{X}| > 0
    \qquad
    \overline{S} \lt: [\overline{U}/\overline{X}]\overline{T}
    \\
    \text{forall} (\overline{V}). \overline{S} \lt: [\overline{V}/\overline{X}]\overline{T} \implies [\overline{U}/\overline{X}]R \lt: [\overline{V}/\overline{X}]R
    \end{array}
}{\Gamma \vdash f(\overline{e}) : [\overline{U}/\overline{X}]R} \quad (\text{App-InfSpec})
$$

Here we use existential quantification $\exists \overline{U}$ and require $\overline{U}$ to satisfy multiple conditions. 
For instance, $\overline{S} \lt: [\overline{U}/\overline{X}]\overline{T}$ is the validity constraint, 
ensuring that the chosen type arguments $\overline{U}$ are legal. 
Legality here means that after substituting $\overline{U}$ into the function's formal parameter types $\overline{T}$, 
the actual argument types $\overline{S}$ must be subtypes. 
Crucially, the final rule $\text{forall} (\overline{V}). \overline{S} \lt: [\overline{V}/\overline{X}]\overline{T} \implies [\overline{U}/\overline{X}]R \lt: [\overline{V}/\overline{X}]R$ 
requires considering all possible type argument tuples $\overline{V}$. 
This translates to searching through a potentially infinite space of $\overline{V}$, 
making it a classic non-constructive description that cannot be implemented in a computer.

Thus, our goal becomes clear: we need a truly executable algorithm whose results align with (App-InfSpec), 
but without requiring non-constructive search or backtracking. This is precisely the role that **constraint generation** will play. 
Its design motivation stems from an ingenious perspective shift on the problem itself.
