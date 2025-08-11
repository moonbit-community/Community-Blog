// section start range

///|
typealias Int as Index

///|
priv struct Range((Index, Index)) derive(Eq, Show)

///|
fn subset(r1 : Range, r2 : Range) -> Bool {
  let (a1, b1) = r1.inner()
  let (a2, b2) = r2.inner()
  a1 >= a2 && b1 <= b2
}

///|
fn contains(self : Range, i : Index) -> Bool {
  subset((i, i), self)
}

///|
fn disjoint(r1 : Range, r2 : Range) -> Bool {
  let (a1, b1) = r1.inner()
  let (a2, b2) = r2.inner()
  b1 < a2 || b2 < a1
}

// section end range
