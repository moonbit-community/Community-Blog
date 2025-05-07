///|
type FenwickTree Array[Int]

///|
fn FenwickTree::lsb(i : Int) -> Int {
  i & -i
}

///|
pub fn FenwickTree::new(len : Int) -> FenwickTree {
  Array::new(capacity=len)
}

///|
pub fn prefix(self : FenwickTree, i : Int) -> Int {
  let mut i = i
  let mut s = 0
  while i > 0 {
    i -= FenwickTree::lsb(i)
    s += self._[i]
  }
  s
}

///|
pub fn update(self : FenwickTree, i : Int, delta : Int) -> Unit {
  let mut i = i
  while i < self._.length() {
    self._[i] += delta
    i += FenwickTree::lsb(i)
  }
}

///|
pub fn range(self : FenwickTree, i : Int, j : Int) -> Int {
  self.prefix(j) - self.prefix(i - 1)
}

///|
pub fn get(self : FenwickTree, i : Int) -> Int {
  self.range(i, i)
}

///|
pub fn set(self : FenwickTree, i : Int, value : Int) -> Unit {
  self.update(i, value - self.get(i))
}
