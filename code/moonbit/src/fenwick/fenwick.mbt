///|
priv struct FenwickTree(Array[Int])

///|
fn FenwickTree::lsb(i : Int) -> Int {
  i & -i
}

///|
fn FenwickTree::new(len : Int) -> FenwickTree {
  Array::new(capacity=len)
}

///|
fn prefix(self : FenwickTree, i : Int) -> Int {
  let mut i = i
  let mut s = 0
  while i > 0 {
    i -= FenwickTree::lsb(i)
    s += self.inner()[i]
  }
  s
}

// section start update

///|
fn update(self : FenwickTree, i : Int, delta : Int) -> Unit {
  let mut i = i
  while i < self.inner().length() {
    self.inner()[i] += delta
    i += FenwickTree::lsb(i)
  }
}

// section end update

///|
fn range(self : FenwickTree, i : Int, j : Int) -> Int {
  self.prefix(j) - self.prefix(i - 1)
}

///|
fn get(self : FenwickTree, i : Int) -> Int {
  self.range(i, i)
}

///|
fn set(self : FenwickTree, i : Int, value : Int) -> Unit {
  self.update(i, value - self.get(i))
}
