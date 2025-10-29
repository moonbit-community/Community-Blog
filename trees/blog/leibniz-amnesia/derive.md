
---
title: 回到 Leibniz
taxon: exegesis
author: [kokic](https://kokic.github.io)
date: 2025-10-29
---

为了方便进行符号微分, 我们先定义一个表达式类型 `Expr`, 其数据显然是树状的, 所以我们使用 `enum` 刻画此归纳结构.

```mbt
enum Expr {
  Symbol(String)
  Const(Float)
  Neg(Expr)
  Add(Expr, Expr)
  Mul(Expr, Expr)
  Div(Expr, Expr)
} derive(Eq, Show)
```

然后为了打印和借助其他工具简化结果, 我们为 `Expr` 定义一个 `to_sexp` 方法. 

```mbt
fn Expr::to_sexp(e : Expr) -> String {
  match e {
    Symbol(x) => x
    Const(c) => c.to_string()
    Neg(a) => "(- 0 \{a.to_sexp()})"
    Add(a, b) => "(+ \{a.to_sexp()} \{b.to_sexp()})"
    Mul(a, b) => "(* \{a.to_sexp()} \{b.to_sexp()})"
    Div(a, b) => "(/ \{a.to_sexp()} \{b.to_sexp()})"
  }
}
```

与例子 [`Mat2x2[Float]`](./float.md) 类似, 可以为 `Expr` 实现 [星半环](./traits.md) 特质. 

```mbt
impl HasNil for Expr with nil() {
  Const(0)
}

impl HasOne for Expr with one() {
  Const(1)
}

impl Neg for Expr with neg(x : Expr) {
  Neg(x)
}

impl Inverse for Expr with inverse(x : Expr) {
  Div(Const(1), x)
}

impl Add for Expr with add(a : Expr, b : Expr) {
  Add(a, b)
}

impl Mul for Expr with mul(a : Expr, b : Expr) {
  Mul(a, b)
}

impl Semiring for Expr

impl StarSemiring for Expr with star(x : Expr) {
  star(x)
}
```

到这一步, 进行符号微分所需的全部定义就结束了. 以下只是一些简化调用的函数. 

```mbt
fn shear(a : Expr, b : Expr) -> Mat2x2[Expr] {
  Mat2x2::mk(a, b, Expr::nil(), a)
}

let symbol : (String) -> Mat2x2[Expr] = name => shear(Symbol(name), Const(1))

fn function(name : String) -> Mat2x2[Expr] {
  shear(Symbol(name), Symbol("\{name}'"))
}

let extract : (Mat2x2[Expr]) -> String = u => u.b.to_sexp()
```

现在, 微分的线性性和 Leibniz 律将自然地被 `Mat2x2[Expr]` 上的加法和乘法导出. 

```mbt
test "leibniz rule" {
  let (f, g) = (function("f"), function("g"))
  assert_eq(extract(f * g), "(+ (* f g') (* f' g))")
}
```

而 $(f/g)'$ 按 $(f g^{-1})'$ 计算即可. 再次强调, 此处 `f` 和 `g` 的类型是 `Mat2x2[Expr]`, 换言之 $f,g$ 实际上是两个矩阵, $g^{-1}$ 按 [前文实现的矩阵逆](./kira.md) 计算. 

```mbt
impl[R : StarSemiring + Neg] Div for Mat2x2[R] with div(
  u : Mat2x2[R],
  v : Mat2x2[R],
) {
  u * v.inverse()
}
```

```mbt
test "leibniz rule" {
  assert_eq(
    extract(f * g.inverse()),
    "(+ (* f (* (/ 1 (+ 1 (- 0 (+ (+ 1 (- 0 g)) (* (* (+ 0 (- 0 g')) (/ 1 (+ 1 (- 0 (+ 1 (- 0 g)))))) (+ 0 (- 0 0))))))) (* (+ 0 (- 0 g')) (/ 1 (+ 1 (- 0 (+ 1 (- 0 g)))))))) (* f' (+ (/ 1 (+ 1 (- 0 (+ 1 (- 0 g))))) (* (* (* (/ 1 (+ 1 (- 0 (+ 1 (- 0 g))))) (+ 0 (- 0 0))) (/ 1 (+ 1 (- 0 (+ (+ 1 (- 0 g)) (* (* (+ 0 (- 0 g')) (/ 1 (+ 1 (- 0 (+ 1 (- 0 g)))))) (+ 0 (- 0 0)))))))) (* (+ 0 (- 0 g')) (/ 1 (+ 1 (- 0 (+ 1 (- 0 g))))))))))",
  )
}
```

读者可以用 [egg][egg] 或其他符号化简工具简化此处 `extract(f * g.inverse())` 的结果, 一个可能的形式是: 

```
(+ (* f (* (- g') (pow g -2))) (* (pow g -1) f'))
```

这当然就是 $(f'g - fg')/g^2 = (f/g)'$. 此方法对多变量情形也完全适用. 

```mbt
test "differentiation" {
  let x = symbol("x")
  let y = symbol("y")
  assert_eq(extract(x), "1")
  assert_eq(extract(x - y), "(+ 1 (- 0 1))")
  assert_eq(
    extract(x / y),
    "(+ (* x (* (/ 1 (+ 1 (- 0 (+ (+ 1 (- 0 y)) (* (* (+ 0 (- 0 1)) (/ 1 (+ 1 (- 0 (+ 1 (- 0 y)))))) (+ 0 (- 0 0))))))) (* (+ 0 (- 0 1)) (/ 1 (+ 1 (- 0 (+ 1 (- 0 y)))))))) (* 1 (+ (/ 1 (+ 1 (- 0 (+ 1 (- 0 y))))) (* (* (* (/ 1 (+ 1 (- 0 (+ 1 (- 0 y))))) (+ 0 (- 0 0))) (/ 1 (+ 1 (- 0 (+ (+ 1 (- 0 y)) (* (* (+ 0 (- 0 1)) (/ 1 (+ 1 (- 0 (+ 1 (- 0 y)))))) (+ 0 (- 0 0)))))))) (* (+ 0 (- 0 1)) (/ 1 (+ 1 (- 0 (+ 1 (- 0 y))))))))))",
  )
}
```

最后的 `extract(x / y)` 可以简化为 `(+ (pow y -1) (* x (* -1 (pow y -2))))`, 即 $\frac{1}{y}-\frac{x}{y^2}$. 读者可以通过为 `Expr` 类型添加诸如 `Cos`, `Sin`, `Exp`, `Log` 此类其他构造器从而使本程序支持带有其他函数的微分运算, 这点与 [经典自动微分程序][ad-haskell] 的做法是一致的. 完整的 MoonBit 源代码可以在 [此处](https://github.com/kokic/moonbit-pearls/blob/main/trees/leibniz-amnesia/amnesia.mbt) 查看. 

[egg]: https://github.com/egraphs-good/egg
[ad-haskell]: https://www.danielbrice.net/blog/automatic-differentiation-is-trivial-in-haskell/