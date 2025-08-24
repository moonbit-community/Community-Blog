---
title: How to Read Typing Rules
collect: true
---

For readers new to programming language theory, the mathematical symbols and inference rules scattered throughout the text may appear unfamiliar and intimidating.  
Please do not worry. These formal tools are not designed to be obscure; on the contrary,  
they aim to achieve **precision** and **unambiguity** that natural language struggles to attain.  
This section provides a simple guide to reading these rules. Readers already familiar with them may skip ahead.

You can think of these rules as the fundamental "physical laws" of a programming language. In a highly rigorous manner,  
they define what programs are well-structured and meaningful, and which are not.

Most rules in this article are presented in the following form:  
$$\frac{\text{前提}_1 \quad \text{前提}_2 \quad ...}{\text{结论}} \quad (\text{规则名称})$$  
The long horizontal line is the key to understanding everything.

- **Above the line: Premises**
  - This lists a set of **conditions** or **assumptions**.
  - The rule can only be activated or used when **all** premises are satisfied.
- **Below the line: Conclusion**
  - This is the new fact we can **infer** after all premises are satisfied.
- **Right parenthesis: Rule Name**
  - This is simply a name assigned to the rule for ease of reference and discussion, such as `Var` or `App`.

In the premises and conclusions of the rules, you will repeatedly encounter a core judgment of the form $\Gamma \vdash e : T$. Let us break down each symbol:

- $\Gamma$ (Gamma): This is the **context**. It represents all known background information or assumptions during inference. Typically, it records types assigned to variables, e.g., $x : \mathbb{Z},\ f : \mathrm{Bool} \to \mathrm{Bool}$. You can interpret it as "given..." or "under the environment of...".
- $\vdash$ (Turnstile): This symbol is read as "yields" or "proves." It separates the context from the assertion being verified.
- $e$: This is the **term**—the piece of program code being analyzed. It could be a simple variable $x$, a function $\mathsf{fun}(x)\ x + 1$, or a complex expression.
- $:$ denotes "has type."
- $T$: This is the **type**, such as $\mathbb{Z}$, $\mathrm{Bool}$, $\mathrm{String} \to \mathbb{Z}$, etc.

Putting it all together, the judgment $\Gamma \vdash e : T$ plainly means:  
"Given the known conditions in context $\Gamma$, we can infer (or prove) that program term $e$ has type $T$."
