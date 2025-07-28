///|
impl Show for Var with to_string(self) {
  self.inner()
}

///|
impl Show for Var with output(self, logger) {
  logger.write_string(self.to_string())
}

///|
impl Show for Type with to_string(self) {
  match self {
    TyVar(v) => v.to_string()
    TyTop => "⊤"
    TyBot => "⊥"
    TyFun(xs, ss, t) => {
      let xs_str = xs.map(Var::to_string).join(", ")
      let ss_str = ss.map(_.to_string()).join(", ")
      let prefix = if xs.is_empty() { "" } else { "∀ [" + xs_str + "]" }
      "\{prefix}(\{ss_str}) -> \{t}"
    }
  }
}

///|
impl Show for Type with output(self, logger) {
  logger.write_string(self.to_string())
}

///|
impl Show for Constraints with output(self, logger) {
  logger.write_string(self.to_string())
}

///|
impl Show for Constraints with to_string(self) {
  let cons = self
    .inner()
    .iter()
    .map(kv => {
      let { l, r } = kv.1
      "\{l} <: \{kv.0} <: \{r}"
    })
    .join(", ")
  guard !cons.is_empty() else { "∅" }
  "{\{cons}}"
}
