---
title: Typing Rules
collect: true
---

本节是我们类型检查程序的最后一块拼图，
描述了整个双向类型检查的过程。

### 变量规则 (Variable Rules)

**1. 综合-变量 (Synthesis-Var)**

$$
\frac{}{\Gamma \vdash x \Rightarrow \Gamma(x)} \quad (\text{S-Var})
$$

这是变量的**综合**规则。如果要在综合模式下推导一个变量 $x$ 的类型，只需在当前的类型上下文 $\Gamma$ 中查找 $x$ 已经声明的类型 $\Gamma(x)$ 即可。这是最直接的类型推导形式：变量的类型就是它被定义时的类型。

---

**2. 检查-变量 (Checking-Var)**

$$
\frac{\Gamma \vdash \Gamma(x) \lt: T}{\Gamma \vdash x \Leftarrow T} \quad (\text{C-Var})
$$

这是变量的**检查**规则。要检查变量 $x$ 是否符合预期的类型 $T$，我们需要先从上下文 $\Gamma$ 中查找到 $x$ 的实际类型 $\Gamma(x)$，然后验证这个实际类型 $\Gamma(x)$ 是否是预期类型 $T$ 的一个子类型 (subtype)。这里的子类型关系用 $\Gamma \vdash \Gamma(x) \lt: T$ 表示。

---

### 函数抽象规则 (Function Abstraction Rules)

**3. 综合-抽象 (Synthesis-Abs)**

$$
\frac{\Gamma, \overline{X}, \overline{x}:\overline{S} \vdash e \Rightarrow T}{\Gamma \vdash \textbf{fun} [\overline{X}] (\overline{x}:\overline{S}) e \Rightarrow \forall \overline{X}. \overline{S} \rightarrow T} \quad (\text{S-Abs})
$$

这是针对**带有完整类型标注的函数抽象**的**综合**规则。

- 一个形式为 `fun [X] (x:S) e` 的函数，其类型参数 $\overline{X}$ 和值参数 $\overline{x}$ 的类型 $\overline{S}$ 都被明确标注了。
- 规则的前提是，在将类型变量 $\overline{X}$ 和值变量及其类型 $\overline{x}:\overline{S}$ 加入到当前上下文 $\Gamma$ 后，我们可以**综合**出函数体 $e$ 的类型为 $T$。
- 那么，整个函数表达式的类型就可以被综合为多态函数类型 $\forall \overline{X}. \overline{S} \rightarrow T$。

---

**4. 检查-无标注抽象 (Checking-Abs-Inf)**

$$
\frac{\Gamma, \overline{X}, \overline{x}:\overline{S} \vdash e \Leftarrow T}{\Gamma \vdash \textbf{fun} [\overline{X}] (\overline{x}) e \Leftarrow \forall \overline{X}. \overline{S} \rightarrow T} \quad (\text{C-Abs-Inf})
$$

这是本节的核心规则之一，用于**推断无标注匿名函数的参数类型**。

- 当我们在**检查**模式下处理一个没有值参数类型标注的函数 `fun [X] (x) e` 时，我们可以从预期的函数类型 $\forall \overline{X}. \overline{S} \rightarrow T$ 中获取信息。
- 具体来说，我们可以从预期的类型中提取出参数类型 $\overline{S}$ 和返回类型 $T$。
- 然后，我们将类型变量 $\overline{X}$ 和推断出的值参数类型 $\overline{x}:\overline{S}$ 加入上下文，并在这个新上下文中以**检查**模式验证函数体 $e$ 是否符合返回类型 $T$。如果满足，则整个无标注函数就通过了类型检查。
- 注意：$\overline{X}$ 在这个系统下是无法省略的。

---

**5. 检查-有标注抽象 (Checking-Abs)**

$$
\frac{\Gamma, \overline{X} \vdash \overline{T} \lt: \overline{S} \quad \Gamma, \overline{X}, \overline{x}:\overline{S} \vdash e \Leftarrow R}{\Gamma \vdash \textbf{fun} [\overline{X}] (\overline{x}:\overline{S}) e \Leftarrow \forall \overline{X}. \overline{T} \rightarrow R} \quad (\text{C-Abs})
$$

这是在**检查**模式下处理一个**带有类型标注的函数**的规则。

- 当一个有标注的函数 `fun [X] (x:S) e` 需要被检查是否符合某个预期类型 $\forall \overline{X}. \overline{T} \rightarrow R$ 时：
- 首先，由于函数类型的参数类型是逆变 (contravariant) 的，我们需要检查预期类型中的参数类型 $\overline{T}$ 是否是函数实际标注的参数类型 $\overline{S}$ 的子类型。
- 随后我们在扩展后的上下文中，以**检查**模式验证函数体 $e$ 是否符合预期的返回类型 $R$。

---

### 函数应用规则 (Function Application Rules)

**6. 综合-应用 (Synthesis-App)**

$$
\frac{\Gamma \vdash f \Rightarrow \forall \overline{X}. \overline{S} \rightarrow R \quad \Gamma \vdash \overline{e} \Leftarrow [\overline{T}/\overline{X}]\overline{S}}{\Gamma \vdash f [\overline{T}] (\overline{e}) \Rightarrow [\overline{T}/\overline{X}]R} \quad (\text{S-App})
$$

这是函数应用的**综合**规则。

- 首先，在**综合**模式下推断出函数 $f$ 的类型为多态函数 $\forall \overline{X}. \overline{S} \rightarrow R$。
- 然后，我们将提供的具体类型参数 $\overline{T}$ 替换掉类型变量 $\overline{X}$，得到参数的预期类型 $[\overline{T}/\overline{X}]\overline{S}$。
- 接下来，我们切换到**检查**模式，验证实际参数 $\overline{e}$ 是否符合这个预期类型。
- 如果检查通过，整个应用表达式的类型就被**综合**为将 $\overline{T}$ 代入后的返回类型 $[\overline{T}/\overline{X}]R$。

---

**7. 检查-应用 (Checking-App)**

$$
\frac{\Gamma \vdash f \Rightarrow \forall \overline{X}. \overline{S} \rightarrow R \quad \Gamma \vdash [\overline{T}/\overline{X}]R \lt: U \quad \Gamma \vdash \overline{e} \Leftarrow [\overline{T}/\overline{X}]\overline{S}}{\Gamma \vdash f [\overline{T}] (\overline{e}) \Leftarrow U} \quad (\text{C-App})
$$

这是函数应用的**检查**规则。它与综合规则非常相似，但增加了一个最终的子类型检查。

- 前两个步骤和 `S-App` 一样：综合 $f$ 的类型，并检查参数 $\overline{e}$。
- 在计算出应用的实际返回类型 $[\overline{T}/\overline{X}]R$ 后，我们还必须检查这个实际返回类型是否是整个应用表达式的预期类型 $U$ 的子类型。

---

### 结合双向检查和类型参数综合的规则

**8. 综合-应用-推断规格 (Synthesis-App-InfAlg)**

$$
\frac{
  \begin{array}{ccc}
    \Gamma \vdash f : \forall \overline{X}.\overline{T} \to R & \Gamma \vdash \overline{e} : \overline{S} & |\overline{X}| > 0 \\
    \emptyset \vdash_X \overline{S} \lt: \overline{T} \Rightarrow \overline{D} & C = \bigwedge \overline{D} & \sigma = \sigma_{CR}
  \end{array}
}{
  \Gamma \vdash f(\overline{e}) \Rightarrow \sigma R
}
\quad (\text{S-App-InfAlg})
$$

这是在**综合**模式下推断函数应用中**缺失的类型参数**的规则，这正是上文「类型参数计算」一节导出的规则。

---

**9. 检查-应用-推断规格 (Checking-App-InfAlg)**

$$
\frac{\begin{matrix} \Gamma \vdash f \Rightarrow \forall \overline{X}. \overline{T} \rightarrow R \quad \Gamma \vdash \overline{e} \Rightarrow \overline{S} \quad |\overline{X}| \gt 0 \\ \emptyset \vdash \overline{S} \lt: \overline{T} \Rightarrow C \quad \emptyset \vdash R \lt: V \Rightarrow D \quad \sigma \in \bigwedge C \wedge D \end{matrix}}{\Gamma \vdash f(\overline{e}) \Leftarrow V} \quad (\text{C-App-InfAlg})
$$

这是 `App-InfAlg` 规则的**检查**版本。

- 它描述了编译器如何通过约束求解来找到合适的类型参数。
- 步骤如下：
  1. 综合函数 $f$ 和参数 $\overline{e}$ 的类型。
  2. 生成两组约束：
     - 第一组约束 $C$ 来自于要求参数的实际类型 $\overline{S}$ 必须是函数期望的参数类型 $\overline{T}$ 的子类型。
     - 第二组约束 $D$ 来自于要求函数的实际返回类型 $R$ 必须是整个表达式的预期类型 $V$ 的子类型。
  3. 求解这两组约束的合取（$\bigwedge C \wedge D$）。如果能找到一个解（一个替换 $\sigma$），那么类型检查就成功了。
  因为这是一条检查规则，因而我们只需要知道解的存在性即可，甚至不需要求解它。

---

### 顶类型和底类型

**10. 检查-顶类型 (Checking-Top)**

$$
\frac{\Gamma \vdash e \Rightarrow T}{\Gamma \vdash e \Leftarrow \top} \quad (\text{C-Top})
$$

这是一个从检查模式切换到综合模式的规则。如果一个表达式 $e$ 被要求检查是否符合顶类型 $\top$，由于任何类型都是 $\top$ 的子类型，这个检查总是会成功。$\top$ 类型没有提供任何有用的约束信息，所以规则允许我们直接切换到**综合**模式，推导出 $e$ 的具体类型 $T$ 即可。

---

**11. 综合-应用-底类型 (Synthesis-App-Bot)**

$$
\frac{\Gamma \vdash f \Rightarrow \bot \quad \Gamma \vdash \overline{e} \Rightarrow \overline{S}}{\Gamma \vdash f [\overline{T}] (\overline{e}) \Rightarrow \bot} \quad (\text{S-App-Bot})
$$

这是处理函数类型为 $\bot$ (底类型) 时的特殊情况。$\bot$ 类型代表那些永不返回的表达式（如抛出异常）。

- 如果一个函数 $f$ 的类型被推导为 $\bot$，那么无论它被应用于何种参数，整个应用表达式的结果类型也是 $\bot$。
- 这是因为 $\bot$ 是所有类型的子类型，包括所有函数类型。因此，一个类型为 $\bot$ 的表达式可以被当作任何函数来应用。

---

**12. 检查-应用-底类型 (Checking-App-Bot)**

$$
\frac{\Gamma \vdash f \Rightarrow \bot \quad \Gamma \vdash \overline{e} \Rightarrow \overline{S}}{\Gamma \vdash f [\overline{T}] (\overline{e}) \Leftarrow R} \quad (\text{C-App-Bot})
$$

这是在**检查**模式下，函数类型为 $\bot$ 的情况。

- 同样，如果函数 $f$ 的类型为 $\bot$，那么应用的结果类型也是 $\bot$。
- 因为 $\bot$ 是任何类型 $R$ 的子类型，所以这个检查总是成功的。