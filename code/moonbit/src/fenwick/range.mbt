// section start range

///|
priv struct Range((Int, Int)) derive(Eq, Debug)

///|
fn Range::bounds(self : Range) -> (Int, Int) {
  let Range(bounds) = self
  bounds
}

///|
fn subset(r1 : Range, r2 : Range) -> Bool {
  let (a1, b1) = r1.bounds()
  let (a2, b2) = r2.bounds()
  a1 >= a2 && b1 <= b2
}

///|
fn Range::contains(self : Range, i : Int) -> Bool {
  subset((i, i), self)
}

///|
fn disjoint(r1 : Range, r2 : Range) -> Bool {
  let (a1, b1) = r1.bounds()
  let (a2, b2) = r2.bounds()
  b1 < a2 || b2 < a1
}

// section end range
