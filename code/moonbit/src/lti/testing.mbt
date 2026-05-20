///|
fn synthesis_outcome(expr : Expr, gamma : Context) -> String {
  expr.synthesis(gamma).to_string() catch {
    SynthesisError => "SynthesisError"
    CheckError => "CheckError"
    ConstraintGenerationError => "ConstraintGenerationError"
    ArgumentLengthMismatch => "ArgumentLengthMismatch"
    NotFound => "NotFound"
    _ => "UnexpectedError"
  }
}

///|
fn check_outcome(expr : Expr, ty : Type, gamma : Context) -> String {
  try {
    expr.check(ty, gamma)
    "ok"
  } catch {
    SynthesisError => "SynthesisError"
    CheckError => "CheckError"
    ConstraintGenerationError => "ConstraintGenerationError"
    ArgumentLengthMismatch => "ArgumentLengthMismatch"
    NotFound => "NotFound"
    _ => "UnexpectedError"
  }
}

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
test "subtyping and bounds" {
  let a = TyVar("a")
  let b = TyVar("b")
  assert_true(TyBot.subtype(a))
  assert_true(a.subtype(TyTop))
  assert_false(a.subtype(b))
  let narrower = TyFun([], [TyTop], a)
  let wider = TyFun([], [a], TyTop)
  assert_true(narrower.subtype(wider))
  assert_false(wider.subtype(narrower))
  inspect(narrower & wider, content="(⊤) -> a")
  inspect(narrower | wider, content="(a) -> ⊤")
}

///|
test "promotion and demotion eliminate escaped variables" {
  let y = TyVar("y")
  let id_y = TyFun([], [y], y)
  let blocked : Set[Var] = Set::from_array(["y"])
  inspect(id_y.promotion(blocked), content="(⊥) -> ⊤")
  inspect(id_y.demotion(blocked), content="(⊤) -> ⊥")
  let scoped = TyFun(["y"], [y], y)
  inspect(scoped.promotion(blocked), content="∀ [y](y) -> y")
  inspect(scoped.demotion(blocked), content="∀ [y](y) -> y")
}

///|
test "constraint solving respects result polarity" {
  let a = TyVar("a")
  let x = TyVar("x")
  let lower = { l: a, r: x }.generate(["x"], Set([]))
  let upper = { l: x, r: TyTop }.generate(["x"], Set([]))
  let both = lower.meet(upper)
  assert_true(both.satisfiable())
  match both.solve(x) {
    Some(subst) => inspect(x.apply_subst(subst), content="a")
    None => abort("expected covariant solution")
  }
  let contravariant_result = TyFun([], [x], TyBot)
  match both.solve(contravariant_result) {
    Some(subst) => inspect(x.apply_subst(subst), content="⊤")
    None => abort("expected contravariant solution")
  }
  let invariant_result = TyFun([], [x], x)
  assert_true(both.solve(invariant_result) is None)
}

///|
test "type inference" {
  let gamma = Context::empty()
  let e = EAbs(
    ["x"],
    [("f", TyFun(["z"], [TyVar("z")], TyVar("z"))), ("x", TyVar("x"))],
    EAppI(EVar("f"), [EVar("x")]),
  )
  inspect(e.synthesis(gamma), content="∀ [x](∀ [z](z) -> z, x) -> x")
  let e = EAbs(
    ["x"],
    [("f", TyFun(["z"], [TyVar("z")], TyVar("z"))), ("x", TyVar("x"))],
    EAppI(EAppI(EVar("f"), [EVar("f")]), [EVar("x")]),
  )
  inspect(e.synthesis(gamma), content="∀ [x](∀ [z](z) -> z, x) -> x")
  let e = EAbs(
    [],
    [("f", TyFun(["z"], [TyVar("z")], TyVar("z")))],
    EAppI(EVar("f"), [EVar("f")]),
  )
  inspect(e.synthesis(gamma), content="(∀ [z](z) -> z) -> ∀ [z](z) -> z")
}

///|
test "bidirectional checking infers unannotated lambda parameters" {
  let gamma = Context::empty()
  let identity = EAbsI(["x"], ["value"], EVar("value"))
  let expected = TyFun(["x"], [TyVar("x")], TyVar("x"))
  inspect(check_outcome(identity, expected, gamma), content="ok")
  let mismatched = TyFun([], [TyVar("a")], TyVar("b"))
  inspect(
    check_outcome(EAbsI([], ["value"], EVar("value")), mismatched, gamma),
    content="CheckError",
  )
}

///|
test "application arity is checked" {
  let a = TyVar("a")
  let gamma = Context::empty().bind("id", TyFun([], [a], a)).bind("x", a)
  inspect(
    synthesis_outcome(EApp(EVar("id"), [], []), gamma),
    content="ArgumentLengthMismatch",
  )
  inspect(
    synthesis_outcome(EApp(EVar("id"), [], [EVar("x"), EVar("x")]), gamma),
    content="ArgumentLengthMismatch",
  )
  let poly = Context::empty()
    .bind("id", TyFun(["x"], [TyVar("x")], TyVar("x")))
    .bind("x", a)
  inspect(
    synthesis_outcome(EAppI(EVar("id"), []), poly),
    content="ArgumentLengthMismatch",
  )
}

///|
test "bottom applications typecheck at any expected result" {
  let gamma = Context::empty().bind("panic", TyBot).bind("x", TyVar("x"))
  let app = EAppI(EVar("panic"), [EVar("x")])
  inspect(app.synthesis(gamma), content="⊥")
  inspect(check_outcome(app, TyVar("anything"), gamma), content="ok")
}

///|
test "constraint generation" {
  let cs = {
    l: TyFun(["y"], [], TyFun([], [TyVar("y")], TyVar("y"))),
    r: TyFun(["y"], [], TyVar("x")),
  }.generate(["x"], Set::from_array(["y"]))
  inspect(cs, content="{(⊥) -> ⊤ <: x <: ⊤}")
}
