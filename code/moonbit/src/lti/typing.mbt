// section start bidirectional

///|
pub fn synthesis(self : Expr, gamma : Context) -> Type raise {
  match self {
    EVar(v) => gamma[v]
    EAbs(xs, vs, body) => {
      let ctx = gamma.append_vars(xs).append_binds(vs)
      let body_ty = body.synthesis(ctx)
      TyFun(xs, vs.map(xS => xS.1), body_ty)
    }
    EAppI(f, e) => {
      let t = f.synthesis(gamma)
      guard !(t is TyBot) else { TyBot }
      guard t is TyFun(xs, t, r) else { raise SynthesisError }
      // guard !xs.is_empty() else { raise NotFound }
      let es = e.map(_.synthesis(gamma))
      let cs = es.zip(t).map(z => { l: z.0, r: z.1 }.generate(xs, Set::new()))
      let sigma = meets(cs).solve(r)
      sigma.map(s => r.apply_subst(s)).or_error(SynthesisError)
    }
    EApp(f, ty, e) => {
      let t = f.synthesis(gamma)
      guard !(t is TyBot) else { TyBot }
      guard t is TyFun(xs, ss, r) else { raise SynthesisError }
      let subst = mk_subst(xs, ty)
      e.zip(ss).each(es => es.0.check(es.1.apply_subst(subst), gamma))
      r.apply_subst(subst)
    }
    _ => raise SynthesisError
  }
}

///|
pub fn check(self : Expr, ty : Type, gamma : Context) -> Unit raise {
  match (self, ty) {
    (_, TyTop) => ()
    (EVar(v), t) => {
      let gx = gamma[v]
      guard gx.subtype(t) else { raise CheckError }
    }
    (EAbs(xs, vs, body), TyFun(xsP, t, r)) if xs == xsP => {
      let ctx = gamma.append_vars(xs)
      guard t.zip(vs.map(xS => xS.1)).iter().all(z => z.0.subtype(z.1)) else {
        raise CheckError
      }
      body.check(r, ctx.append_binds(vs))
    }
    (EAbsI(xs, vs, body), TyFun(xsP, ss, t)) if xs == xsP &&
      ss.length() == vs.length() =>
      body.check(t, gamma.append_vars(xs).append_binds(vs.zip(ss)))
    (EAppI(f, e), u) => {
      let t = f.synthesis(gamma)
      guard !(t is TyBot && u is TyBot) else { () }
      guard f.synthesis(gamma) is TyFun(xs, t, r) else { raise CheckError }
      guard !xs.is_empty() else { () }
      let es = e.map(_.synthesis(gamma))
      let cs = es.zip(t).map(z => { l: z.0, r: z.1 }.generate(xs, Set::new()))
      let d = { l: r, r: u }.generate(xs, Set::new())
      guard meets(cs).meet(d).satisfiable() else { raise CheckError }
    }
    (EApp(f, ty, e), u) => {
      let t = f.synthesis(gamma)
      guard !(t is TyBot && u is TyBot) else { () }
      guard t is TyFun(xs, ss, r)
      let subst = mk_subst(xs, ty)
      e.zip(ss).each(es => es.0.check(es.1.apply_subst(subst), gamma))
      guard r.apply_subst(subst).subtype(u) else { raise CheckError }
    }
    _ => raise CheckError
  }
}

// section end bidirectional
