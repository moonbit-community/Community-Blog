///|
pub(all) enum Context {
  CtxEmpty
  CtxBinding(Context, Var, Type)
  CtxTyVar(Context, Var)
}

///|
pub fn Context::op_get(self : Context, vr : Var) -> Type raise NotFound {
  match self {
    CtxBinding(_, v, t) if v == vr => t
    CtxBinding(ctx, _, _) => ctx[vr]
    CtxTyVar(ctx, _) => ctx[vr]
    CtxEmpty => raise NotFound
  }
}

///|
pub fn Context::append_vars(self : Context, vars : Array[Var]) -> Context {
  vars.iter().fold(init=self, CtxTyVar(_, _))
}

///|
pub fn Context::empty() -> Context {
  CtxEmpty
}

///|
pub fn Context::bind(self : Context, vr : Var, ty : Type) -> Context {
  CtxBinding(self, vr, ty)
}

///|
pub fn Context::append_binds(
  self : Context,
  binds : Array[(Var, Type)],
) -> Context {
  binds.iter().fold(init=self, (ctx, vt) => ctx.bind(vt.0, vt.1))
}

///|
impl Show for Context with output(self, logger) {
  logger.write_string(self.to_string())
}

///|
impl Show for Context with to_string(self) {
  match self {
    CtxEmpty => ""
    CtxBinding(CtxEmpty, v, ty) => "\{v}=\{ty}"
    CtxBinding(ctx, v, ty) => "\{ctx},\{v}=\{ty}"
    CtxTyVar(CtxEmpty, tv) => "\{tv}"
    CtxTyVar(ctx, tv) => "\{ctx},\{tv}"
  }
}
