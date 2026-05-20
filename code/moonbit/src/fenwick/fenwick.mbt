///|
priv struct FenwickTree(Array[Int])

///|
fn FenwickTree::items(self : FenwickTree) -> Array[Int] {
  let FenwickTree(items) = self
  items
}

///|
fn FenwickTree::lsb(i : Int) -> Int {
  i & -i
}

///|
fn FenwickTree::new(len : Int) -> FenwickTree {
  Array::new(capacity=len)
}

///|
fn FenwickTree::prefix(self : FenwickTree, i : Int) -> Int {
  let mut i = i
  let mut s = 0
  let items = self.items()
  while i > 0 {
    i -= FenwickTree::lsb(i)
    s += items[i]
  }
  s
}

// section start update

///|
fn FenwickTree::update(self : FenwickTree, i : Int, delta : Int) -> Unit {
  let mut i = i
  let items = self.items()
  while i < items.length() {
    items[i] += delta
    i += FenwickTree::lsb(i)
  }
}

// section end update

///|
fn FenwickTree::range(self : FenwickTree, i : Int, j : Int) -> Int {
  self.prefix(j) - self.prefix(i - 1)
}

///|
fn FenwickTree::get(self : FenwickTree, i : Int) -> Int {
  self.range(i, i)
}

///|
fn FenwickTree::set(self : FenwickTree, i : Int, value : Int) -> Unit {
  self.update(i, value - self.get(i))
}
