///|
typealias Index = Int

///|
priv type Range (Index, Index) derive(Eq, Show)

///|
fn subset(r1 : Range, r2 : Range) -> Bool {
  let (a1, b1) = r1._
  let (a2, b2) = r2._
  a1 >= a2 && b1 <= b2
}

///|
fn contains(self : Range, i : Index) -> Bool {
  subset((i, i), self)
}

///|
fn disjoint(r1 : Range, r2 : Range) -> Bool {
  let (a1, b1) = r1._
  let (a2, b2) = r2._
  b1 < a2 || b2 < a1
}
