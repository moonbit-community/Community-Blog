
///|
typealias List[T] = @immut/list.T[T]

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

///|
enum Bit {
  O
  I
} derive(Eq)

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

///|
enum Bits {
  Rep(Bit)
  Snoc(Bits, Bit)
} derive(Eq)

///|
pub fn to_snoc(self : Bits) -> Bits {
  match self {
    Rep(a) => Snoc(Rep(a), a)
    self => self
  }
}

///|
pub fn Bits::pat_match(self : Bits) -> (Bits, Bit) {
  guard self.to_snoc() is Snoc(bs, b)
  (bs, b)
}

///|
pub fn Bits::make(self : Bits, b : Bit) -> Bits {
  match (self, b) {
    (Rep(b), b1) if b == b1 => Rep(b)
    (bs, b) => Snoc(bs, b)
  }
}

///|
fn div(n : Int, d : Int) -> Int {
  if n < 0 {
    (n - d + 1) / d
  } else {
    n / d
  }
}

///|
pub fn Bits::to_bits(n : Int) -> Bits {
  match n {
    0 => Rep(O)
    -1 => Rep(I)
    n => Bits::make(Bits::to_bits(div(n, 2)), Bit::to_enum(n % 2))
  }
}

///|
pub fn Bits::from_bits(self : Bits) -> Int {
  match self {
    Rep(O) => 0
    Rep(I) => -1
    bs => {
      let (bs, b) = bs.pat_match()
      2 * Bits::from_bits(bs) + Bit::from_enum(b)
    }
  }
}

///|
test "from . to == id" {
  @qc.quick_check_fn!(fn(x) { Bits::from_bits(Bits::to_bits(x)) == x })
  // +++ [100/0/100] Ok, passed!
}

///|
impl Show for Bits with to_string(self) {
  fn go {
    Rep(b) => b.to_string().repeat(3) + "..."
    s => {
      let (bs, b) = s.pat_match()
      b.to_string() + go(bs)
    }
  }

  go(self).rev()
}

///|
impl Show for Bits with output(self, logger) {
  logger.write_string(self.to_string())
}

///|
test {
  let b = Snoc(Rep(O), O) |> Snoc(I) |> Snoc(O) |> Snoc(I)
  inspect!(b, content="...0000101")
  let b1 = Snoc(Rep(I), O) |> Snoc(I)
  inspect!(b1, content="...11101")
  let b26 = Bits::to_bits(26)
  let b24 = Bits::to_bits(24)
  inspect!(b24, content="...00011000")
  inspect!(b26, content="...00011010")
  let b_30 = Bits::to_bits(-30)
  inspect!(b_30, content="...11100010")
  inspect!(b_30.from_bits(), content="-30")
}

///|
pub fn inc(self : Bits) -> Bits {
  match self {
    Rep(I) => Rep(O)
    s =>
      match s.pat_match() {
        (bs, O) => Bits::make(bs, I)
        (bs, I) => Bits::make(bs.inc(), O)
      }
  }
}

///|
pub fn dec(self : Bits) -> Bits {
  match self {
    Rep(O) => Rep(I)
    s =>
      match s.pat_match() {
        (bs, I) => Bits::make(bs, O)
        (bs, O) => Bits::make(bs.dec(), I)
      }
  }
}

///|
pub fn lsb(self : Bits) -> Bits {
  match self {
    Rep(O) => Rep(O)
    s =>
      match s.pat_match() {
        (bs, O) => Bits::make(bs.lsb(), O)
        (_, I) => Bits::make(Rep(O), I)
      }
  }
}

///|
test {
  inspect!(Bits::to_bits(26), content="...00011010")
  inspect!(Bits::to_bits(26).lsb(), content="...00010")
  inspect!(Bits::to_bits(24), content="...00011000")
  inspect!(Bits::to_bits(24).lsb(), content="...0001000")
}

///|
impl BitAnd for Bits with land(self, other) {
  match (self, other) {
    (Rep(x), Rep(y)) => Rep(x & y)
    (xs, ys) =>
      match (xs.pat_match(), ys.pat_match()) {
        ((bs, b), (bs1, b1)) => Bits::make(bs.lsb() & bs1.lsb(), b & b1)
      }
  }
}

///|
pub fn Bits::inv(self : Bits) -> Bits {
  match self {
    Rep(x) => Rep(x.not())
    s =>
      match s.pat_match() {
        (bs, b) => Bits::make(bs.inv(), b.not())
      }
  }
}

///|
impl Add for Bits with op_add(self, other) {
  match (self, other) {
    (xs, Rep(O)) | (Rep(O), xs) => xs
    (Rep(I), Rep(I)) => Bits::make(Rep(I), O)
    _ =>
      match (self.pat_match(), other.pat_match()) {
        ((xs, I), (ys, I)) => Bits::make((xs + ys).inc(), O)
        ((xs, x), (ys, y)) => Bits::make(xs + ys, x | y)
      }
  }
}

///|
impl Neg for Bits with op_neg(self) {
  self.inv().inc()
}

///|
test "add" {
  @qc.quick_check_fn!(fn {
    (x, y) => x + y == Bits::from_bits(Bits::to_bits(x) + Bits::to_bits(y))
  })
  // +++ [100/0/100] Ok, passed!
}

///|
pub fn set_to(self : Bits, idx : Int, b1 : Bit) -> Bits {
  match (idx, self.pat_match()) {
    (0, (bs, _)) => Bits::make(bs, b1)
    (k, (bs, b)) => Bits::make(bs.set_to(k - 1, b1), b)
  }
}

///|
pub fn Bits::set(self : Bits, idx : Int) -> Bits {
  self.set_to(idx, I)
}

///|
pub fn Bits::clear(self : Bits, idx : Int) -> Bits {
  self.set_to(idx, O)
}

///|
pub fn test_helper(self : Bits, i : Int) -> Bool {
  loop i, self.pat_match() {
    0, (_bs, b) => b == I
    k, (bs, _b) => continue k - 1, bs.pat_match()
  }
}

///|
pub fn odd(self : Bits) -> Bool {
  self.test_helper(0)
}

///|
pub fn even(self : Bits) -> Bool {
  not(self.odd())
}

///|
pub fn shr(self : Bits) -> Bits {
  self.pat_match().0
}

///|
pub fn shl(self : Bits) -> Bits {
  Bits::make(self, O)
}

///|
pub fn while_[A](p : (A) -> Bool, f : (A) -> A, x : A) -> A {
  loop x {
    x => if p(x) { continue f(x) } else { x }
  }
}

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
