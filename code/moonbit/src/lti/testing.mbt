///|
test "polarity" {
  let ty = TyFun([], [TyVar("a")], TyVar("a"))
  let ty1 = TyFun([], [TyVar("b")], TyVar("a"))
  let ty2 = TyFun([], [TyFun([], [TyVar("b")], TyVar("a"))], TyVar("b"))
  inspect(ty.variance("a"), content="Invariant")
  inspect(ty1.variance("a"), content="Covariant")
  inspect(ty1.variance("b"), content="Contravariant")
  inspect(ty1.variance("c"), content="Constant")
  inspect(ty2.variance("a"), content="Contravariant")
}

///|
test "type inference" {
  let gamma = Context::empty()
  let e = EAbs(
    ["x"],
    [("f", TyFun(["z"], [TyVar("z")], TyVar("z"))), ("x", TyVar("x"))],
    EApp(EVar("f"), [], [EVar("x")]),
  )
  inspect(e.synthesis(gamma), content="∀ [x](∀ [z](z) -> z, x) -> x")
  let e = EAbs(
    ["x"],
    [("f", TyFun(["z"], [TyVar("z")], TyVar("z"))), ("x", TyVar("x"))],
    EApp(EApp(EVar("f"), [], [EVar("f")]), [], [EVar("x")]),
  )
  inspect(e.synthesis(gamma), content="∀ [x](∀ [z](z) -> z, x) -> x")
  let e = EAbs(
    [],
    [("f", TyFun(["z"], [TyVar("z")], TyVar("z")))],
    EApp(EVar("f"), [], [EVar("f")]),
  )
  inspect(e.synthesis(gamma), content="(∀ [z](z) -> z) -> ∀ [z](z) -> z")
}

///|
test "constraint generation" {
  let cs = {
    l: TyFun(["y"], [], TyFun([], [TyVar("y")], TyVar("y"))),
    r: TyFun(["y"], [], TyVar("x")),
  }.generate(["x"], Set::from_array(["y"]))
  inspect(cs, content="{(⊥) -> ⊤ <: x <: ⊤}")
}
