// section start bit
///|
enum Bit {
  O
  I
} derive(Eq)

///|
pub fn Bit::not(self : Bit) -> Bit {
  match self {
    O => I
    I => O
  }
}

///|
impl BitAnd for Bit with land(self, other) {
  match (self, other) {
    (O, _) => O
    (I, x) => x
  }
}

///|
impl BitOr for Bit with lor(self, other) {
  match (self, other) {
    (I, _) => I
    (O, x) => x
  }
}
// section end bit

///|
impl Show for Bit with to_string(self) {
  match self {
    O => "0"
    I => "1"
  }
}

///|
impl Show for Bit with output(self, logger) {
  logger.write_string(self.to_string())
}

///|
pub fn Bit::to_enum(i : Int) -> Bit {
  match i {
    0 => O
    1 | -1 => I
    _ => abort("Invalid bit value")
  }
}

///|
pub fn Bit::from_enum(self : Bit) -> Int {
  match self {
    O => 0
    I => 1
  }
}