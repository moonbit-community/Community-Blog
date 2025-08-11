///|
pub(all) struct Var(String) derive(Hash, Eq)

// section start spec

///|
pub(all) enum Type {
  TyVar(Var)
  TyTop
  TyBot
  TyFun(Array[Var], Array[Type], Type)
} derive(Eq)

///|
pub(all) enum Expr {
  EVar(Var)
  EAppI(Expr, Array[Expr])
  EApp(Expr, Array[Type], Array[Expr])
  EAbs(Array[Var], Array[(Var, Type)], Expr)
  EAbsI(Array[Var], Array[Var], Expr)
}

// section end spec

// section start subtype

///|
/// l <: r
struct Subtype {
  l : Type
  r : Type
}

///|
pub fn subtype(self : Subtype) -> Bool {
  match (self.l, self.r) {
    (TyVar(v1), TyVar(v2)) => v1 == v2
    (_, TyTop) => true
    (TyBot, _) => true
    (TyFun(xs1, r, s), TyFun(xs2, t, u)) if xs1 == xs2 =>
      subtypes(t, r) && { l: s, r: u }.subtype()
    _ => false
  }
}

// section end subtype

///|
pub fn Type::subtype(self : Type, other : Type) -> Bool {
  { l: self, r: other }.subtype()
}

// section start subtype_op

///|
impl BitAnd for Type with land(s, t) {
  match (s, t) {
    (TyFun(xs1, v, p), TyFun(xs2, w, q)) if xs1 == xs2 => {
      guard v.length() == w.length() else { TyBot }
      TyFun(xs1, v.zip(w).map(z => z.0 | z.1), p & q)
    }
    (s, t) if s.subtype(t) => s
    (s, t) if t.subtype(s) => t
    _ => TyBot
  }
}

///|
impl BitOr for Type with lor(s, t) {
  match (s, t) {
    (TyFun(xs1, v, p), TyFun(xs2, w, q)) if xs1 == xs2 => {
      guard v.length() == w.length() else { TyTop }
      TyFun(xs1, v.zip(w).map(z => z.0 & z.1), p | q)
    }
    (s, t) if s.subtype(t) => t
    (s, t) if t.subtype(s) => s
    _ => TyTop
  }
}

// section end subtype_op

///|
pub fn subtypes(t1 : Array[Type], t2 : Array[Type]) -> Bool {
  guard t1.length() == t2.length() else { false }
  t1.zip_to_iter2(t2).iter().all(s => s.0.subtype(s.1))
}

// section start promotion_demotion

///|
pub fn promotion(self : Type, v : Set[Var]) -> Type {
  match self {
    TyFun(xs, ss, t) => {
      let vP = v.iter().filter(x => !xs.contains(x)) |> Set::from_iter
      let us = ss.map(_.demotion(vP))
      let r = t.promotion(vP)
      guard xs.iter().all(x => !v.contains(x))
      TyFun(xs, us, r)
    }
    TyVar(vr) if v.contains(vr) => TyTop
    _ => self
  }
}

///|
pub fn demotion(self : Type, v : Set[Var]) -> Type {
  match self {
    TyFun(xs, ss, t) => {
      let vP = v.iter().filter(x => !xs.contains(x)) |> Set::from_iter
      let us = ss.map(_.demotion(vP))
      let r = t.demotion(vP)
      TyFun(xs, us, r)
    }
    TyVar(vr) if v.contains(vr) => TyBot
    _ => self
  }
}

// section end promotion_demotion

// section start constraints

///|
struct Constraints(Map[Var, Subtype])

///|
pub fn Constraints::empty() -> Constraints {
  Constraints(Map::new())
}

///|
pub fn meet(self : Constraints, other : Constraints) -> Constraints {
  union_with(self.inner(), other.inner(), (l, r) => {
    let { l: l1, r: r1 } = l
    let { l: l2, r: r2 } = r
    { l: l1 & l2, r: r1 | r2 }
  })
}

///|
pub fn meets(c : Array[Constraints]) -> Constraints {
  c.iter().fold(init=Constraints::empty(), Constraints::meet)
}

// section end constraints

///|
pub suberror ConstraintGenerationError

///|
pub suberror NotFound

///|
pub suberror ArgumentLengthMismatch

///|
pub suberror TypeError {
  SynthesisError
  CheckError
}

// section start cg

///|
/// Pre-condition: xs and v are disjoint sets of variables.
pub fn generate(
  self : Subtype,
  xs : Array[Var],
  v : Set[Var],
) -> Constraints raise {
  match (self.l, self.r) {
    (_, TyTop) | (TyBot, _) => Constraints::empty()
    (TyVar(y1), TyVar(y2)) if y1 == y2 && !xs.contains(y1) =>
      Constraints::empty()
    (TyVar(y), s) if xs.contains(y) => {
      let t = s.demotion(v)
      Map::from_array([(y, { l: TyBot, r: t })])
    }
    (s, TyVar(y)) if xs.contains(y) => {
      let t = s.promotion(v)
      Map::from_array([(y, { l: t, r: TyTop })])
    }
    (TyFun(ys1, r, s), TyFun(ys2, t, u)) if ys1 == ys2 => {
      let vy = v.union(Set::from_array(ys1))
      let cs = t.zip(r).map(tr => { l: tr.0, r: tr.1 }.generate(xs, vy))
        |> meets()
      cs.meet({ l: s, r: u }.generate(xs, vy))
    }
    _ => raise ConstraintGenerationError
  }
}

// section end cg

///|
enum Variance {
  Covariant
  Contravariant
  Constant
  Invariant
} derive(Show)

// section start solve

///|
pub fn solve(self : Constraints, ty : Type) -> Map[Var, Type]? {
  let f = (vs : (Var, Subtype)) => {
    let { l, r } = vs.1
    let v = match ty.variance(vs.0) {
      Constant | Covariant => Some(l)
      Contravariant => Some(r)
      Invariant => if l == r { Some(l) } else { None }
    }
    v.map(v => (vs.0, v))
  }
  let i = self.inner().iter().filter_map(f)
  guard i.count() == self.inner().size() else { None }
  Some(Map::from_iter(i))
}

// section end solve

///|
pub fn satisfiable(self : Constraints) -> Bool {
  self.inner().iter().all(kv => kv.1.subtype())
}

// section start variance

///|
pub fn variance(self : Type, va : Var) -> Variance {
  letrec go = (ty : Type, polarity : Bool) => match ty {
    TyVar(v) if v == va => if polarity { Covariant } else { Contravariant }
    TyVar(_) | TyTop | TyBot => Constant
    TyFun(_, params, ret) => {
      let param_variance = params
        .map(p => go(p, !polarity))
        .fold(init=Constant, combine_variance)
      combine_variance(param_variance, go(ret, polarity))
    }
  }
  and combine_variance = (v1 : Variance, v2 : Variance) => match (v1, v2) {
    (Constant, v) | (v, Constant) => v
    (Covariant, Covariant) | (Contravariant, Contravariant) => v1
    (Covariant, Contravariant) | (Contravariant, Covariant) => Invariant
    (Invariant, _) | (_, Invariant) => Invariant
  }

  go(self, true)
}

// section end variance

// section start subst

///|
pub fn mk_subst(vars : Array[Var], tys : Array[Type]) -> Map[Var, Type] raise {
  guard vars.length() == tys.length() else { raise ArgumentLengthMismatch }
  Map::from_array(vars.zip(tys))
}

///|
pub fn apply_subst(self : Type, subst : Map[Var, Type]) -> Type {
  match self {
    TyVar(v) => subst.get(v).unwrap_or(self)
    TyTop | TyBot => self
    TyFun(xs, ss, t) => {
      let fs = subst.iter().filter(kv => !xs.contains(kv.0)) |> Map::from_iter
      let new_ss = ss.map(s => s.apply_subst(fs))
      let new_t = t.apply_subst(fs)
      TyFun(xs, new_ss, new_t)
    }
  }
}

// section end subst

///|
fn[K : Eq + Hash, V] union_with(
  m1 : Map[K, V],
  m2 : Map[K, V],
  f : (V, V) -> V,
) -> Map[K, V] {
  let c = m1.copy()
  for k, v in m2 {
    match c.get(k) {
      None => c[k] = v
      Some(e) => c[k] = f(e, v)
    }
  }
  c
}
