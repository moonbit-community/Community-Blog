///|
typealias MyList as List

// section start seg_tree

///|
priv enum SegTree {
  Empty
  Branch(Int, Range, SegTree, SegTree)
} derive(Eq, Show)

///|
fn SegTree::update(self : SegTree, i : Index, v : Int) -> SegTree {
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
fn SegTree::get(self : SegTree, i : Index) -> Int {
  self.rq((i, i))
}

///|
fn SegTree::set(self : SegTree, i : Index, v : Int) -> SegTree {
  self.update(i, v - self.get(i))
}

// section end seg_tree

// section start interleave

///|
fn[T] interleave(sel : List[T], other : List[T]) -> List[T] {
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
      Int::until(1 << n, (1 << n) + (1 << (n - 1))).map(x => x * 2)
      |> from_iter
      |> interleave(b(n - 1))
  }
}

// section end interleave

// section start b4

///|
test "b(4)" {
  inspect(
    b(4),
    content="@list.of([32, 16, 34, 8, 36, 18, 38, 4, 40, 20, 42, 10, 44, 22, 46, 2])",
  )
}

// section end b4

// section start shift

///|
fn shift(n : Int, se : Bits) -> Bits {
  while_(Bits::even, Bits::shr, se.set(n))
}

///|
fn f2b(n : Int, se : Bits) -> Bits {
  shift(n + 1, se).dec()
}

// section end shift

// section start unshift

///|
fn unshift(n : Int, se : Bits) -> Bits {
  while_(x => not(x.test_helper(n)), Bits::shl, se) |> Bits::clear(_, n)
}

///|
fn b2f(n : Int, se : Bits) -> Bits {
  unshift(n + 1, se.inc())
}

// section end unshift

// section start test_id

///|
test "id" {
  let f = size => Int::until(1, 1 << size)
    .map(x => (f2b(size, x |> Bits::to_bits) |> b2f(size, _) |> Bits::from_bits) ==
      x)
    .all(x => x)
  assert_true(f(4))
  assert_true(f(5))
}

// section end test_id

// section start active_parent_binary

///|
fn active_parent_binary(self : Bits) -> Bits {
  while_(Bits::odd, Bits::shr, self.shr())
}

// section end active_parent_binary

// section start at_lsb

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

// section end at_lsb

// section start prev_segment_binary

///|
fn prev_segment_binary(self : Bits) -> Bits {
  while_(Bits::even, Bits::shr, self).dec()
}

// section end prev_segment_binary

///|
test "x - lsb x" {
  let x = Bits::to_bits(26)
  inspect(x.at_lsb(Bits::dec), content="...00011000")
}

///|
test {
  let for_n = n => fn(x) {
    guard x == 0 else { true }
    let x = x + 1
    let x = x |> Bits::to_bits
    (f2b(n, x) |> Bits::prev_segment_binary |> b2f(n, _)) == x.at_lsb(Bits::dec)
  }
  @qc.quick_check_fn(for_n(4))
  // +++ [100/0/100] Ok, passed!
}
