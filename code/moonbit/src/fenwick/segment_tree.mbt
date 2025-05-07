
///|
typealias List[T] = @immut/list.T[T]

// section start seg_tree
///|
enum SegTree {
  Empty
  Branch(Int, Range, SegTree, SegTree)
} derive(Eq, Show)

///|
pub fn SegTree::update(self : SegTree, i : Index, v : Int) -> SegTree {
  match self {
    Empty => Empty
    Branch(a, rng, l, r) if rng.contains(i) =>
      Branch(a + v, rng, l.update(i, v), r.update(i, v))
    _ => self
  }
}

///|
fn rq(self : SegTree, q : Range) -> Int {
  match self {
    Empty => 0
    Branch(a, rng, l, r) =>
      if disjoint(rng, q) {
        0
      } else if subset(rng, q) {
        a
      } else {
        l.rq(q) + r.rq(q)
      }
  }
}

///|
pub fn SegTree::get(self : SegTree, i : Index) -> Int {
  self.rq((i, i))
}

///|
pub fn SegTree::set(self : SegTree, i : Index, v : Int) -> SegTree {
  self.update(i, v - self.get(i))
}
// section end seg_tree

///|
pub fn interleave[T](sel : List[T], other : List[T]) -> List[T] {
  match (sel, other) {
    (Nil, _) => Nil
    (Cons(x, xs), ys) => Cons(x, interleave(ys, xs))
  }
}

///|
fn b(i : Int) -> List[Int] {
  match i {
    0 => Cons(2, Nil)
    n =>
      Int::until(1 << n, (1 << n) + (1 << (n - 1))).map(fn { x => x * 2 })
      |> @immut/list.from_iter
      |> interleave(b(n - 1))
  }
}

///|
test {
  inspect!(
    b(4),
    content="@list.of([32, 16, 34, 8, 36, 18, 38, 4, 40, 20, 42, 10, 44, 22, 46, 2])",
  )
  inspect!(1 << 10, content="1024")
}

///|
pub fn shift(self : Bits, n : Int) -> Bits {
  while_(even, shr, self.set(n))
}

///|
pub fn f2b(self : Bits, n : Int) -> Bits {
  self.shift(n + 1).dec()
}

///|
pub fn unshift(self : Bits, n : Int) -> Bits {
  while_(fn { x => not(x.test_helper(n)) }, shl, self) |> Bits::clear(_, n)
}

///|
pub fn b2f(self : Bits, n : Int) -> Bits {
  self.inc().unshift(n + 1)
}

///|
test "id" {
  let f = fn {
    size =>
      Int::until(1, 1 << size)
      .map(fn {
        x =>
          (x |> Bits::to_bits |> f2b(size) |> b2f(size) |> Bits::from_bits) == x
      })
      .all(fn { x => x })
  }
  assert_true!(f(4))
  assert_true!(f(5))
}

///|
pub fn active_parent_binary(self : Bits) -> Bits {
  while_(odd, shr, self) |> shr
}

///|
fn at_lsb(self : Bits, f : (Bits) -> Bits) -> Bits {
  match self {
    Rep(O) => Rep(O)
    s =>
      match s.pat_match() {
        (bs, O) => bs.at_lsb(f) |> Bits::make(O)
        (bs, I) => Bits::make(bs, I) |> f
      }
  }
}

///|
fn prev_segment_binary(self : Bits) -> Bits {
  while_(even, shr, self).dec()
}

///|
test "x - lsb x" {
  let x = Bits::to_bits(26)
  inspect!(x.at_lsb(dec), content="...00011000")
}

///|
test {
  fn for_n {
    n =>
      fn(x) {
        guard x == 0 else { true }
        let x = x + 1
        let x = x |> Bits::to_bits
        (f2b(x, n) |> prev_segment_binary |> b2f(n)) == x.at_lsb(dec)
      }
  }

  @qc.quick_check_fn!(for_n(4))
  // +++ [100/0/100] Ok, passed!
}
