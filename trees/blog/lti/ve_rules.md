---
title: Promotion and Demotion Rules
collect: true
---

- **提升规则 ($S \Uparrow^V T$)**

  - 对于 $\top$ 和 $\bot$：
    $$
    \top \Uparrow^V \top \quad (\text{VU-Top})
    $$
    $$
    \bot \Uparrow^V \bot \quad (\text{VU-Bot})
    $$
  - 对于类型变量 $X$：
    - 若 $X$ 属于需要被消除的集合 $V$，则将其**提升**至 $\top$。
      $$
      \frac{X \in V}{X \Uparrow^V \top} \quad (\text{VU-Var-1})
      $$
    - 若 $X$ 不在 $V$ 中，则保持不变。
      $$
      \frac{X \notin V}{X \Uparrow^V X} \quad (\text{VU-Var-2})
      $$
  - 对于函数类型：
    - 递归地对其参数类型进行**下降**（因为参数位置是逆变的），并对其返回类型进行**提升**（因为返回位置是协变的）。
      $$
      \frac{\overline{S} \Downarrow^V \overline{U} \quad T \Uparrow^V R \quad \overline{X} \notin V}{\forall\overline{X}.\overline{S} \to T \Uparrow^V \forall\overline{X}.\overline{U} \to R} \quad (\text{VU-Fun})
      $$

- **下降规则 ($S \Downarrow^V T$)**
  - 对于 $\top$ 和 $\bot$ 的处理和提升规则一致。
  - 对于类型变量 $X$：
    - 若 $X$ 属于 $V$，则将其**下降**至 $\bot$。
      $$
      \frac{X \in V}{X \Downarrow^V \bot} \quad (\text{VD-Var-1})
      $$
    - 若 $X$ 不在 $V$ 中，则保持不变。
  - 对于函数类型：
    - 递归地对其参数类型进行**提升**，并对其返回类型进行**下降**。
      $$
      \frac{\overline{S} \Uparrow^V \overline{U} \quad T \Downarrow^V R \quad \overline{X} \notin V}{\forall\overline{X}.\overline{S} \to T \Downarrow^V \forall\overline{X}.\overline{U} \to R} \quad (\text{VD-Fun})
      $$

这可以非常直接地在 MoonBit 中实现：

![promotion_demotion](moonbit/src//lti/syntax.mbt#:include)
