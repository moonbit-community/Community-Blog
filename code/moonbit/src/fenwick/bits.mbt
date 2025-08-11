// section start bits

///|
priv enum Bits {
  Rep(Bit)
  Snoc(Bits, Bit)
} derive(Eq)

// section end bits

// section start pattern

///|
fn to_snoc(self : Bits) -> Bits {
  match self {
    Rep(a) => Snoc(Rep(a), a)
    self => self
  }
}

///|
fn Bits::pat_match(self : Bits) -> (Bits, Bit) {
  guard self.to_snoc() is Snoc(bs, b)
  (bs, b)
}

///|
fn Bits::make(self : Bits, b : Bit) -> Bits {
  match (self, b) {
    (Rep(b), b1) if b == b1 => Rep(b)
    (bs, b) => Snoc(bs, b)
  }
}

// section end pattern

///|
fn div(n : Int, d : Int) -> Int {
  if n < 0 {
    (n - d + 1) / d
  } else {
    n / d
  }
}

// section start conversion

///|
fn Bits::to_bits(n : Int) -> Bits {
  match n {
    0 => Rep(O)
    -1 => Rep(I)
    n => Bits::make(Bits::to_bits(div(n, 2)), Bit::to_enum(n % 2))
  }
}

///|
fn Bits::from_bits(self : Bits) -> Int {
  match self {
    Rep(O) => 0
    Rep(I) => -1
    bs => {
      let (bs, b) = bs.pat_match()
      2 * Bits::from_bits(bs) + Bit::from_enum(b)
    }
  }
}

// section end conversion

// section start show

///|
impl Show for Bits with to_string(self) {
  fn go(s) {
    match s {
      Rep(b) => b.to_string().repeat(3) + "..."
      s => {
        let (bs, b) = s.pat_match()
        b.to_string() + go(bs)
      }
    }
  }

  go(self).rev()
}

///|
impl Show for Bits with output(self, logger) {
  logger.write_string(self.to_string())
}

// section end show

// section start test1

///|
test "from . to == id" {
  let b = Snoc(Rep(O), O) |> Snoc(I) |> Snoc(O) |> Snoc(I)
  inspect(b, content="...0000101")
  let b1 = Snoc(Rep(I), O) |> Snoc(I)
  inspect(b1, content="...11101")
  let b26 = Bits::to_bits(26)
  inspect(b26, content="...00011010")
  let b_30 = Bits::to_bits(-30)
  inspect(b_30, content="...11100010")
  inspect(b_30.from_bits(), content="-30")
  @qc.quick_check_fn(x => Bits::from_bits(Bits::to_bits(x)) == x)
  // +++ [100/0/100] Ok, passed!
}

// section end test1

// section start inc_dec

///|
fn inc(self : Bits) -> Bits {
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
fn dec(self : Bits) -> Bits {
  match self {
    Rep(O) => Rep(I)
    s =>
      match s.pat_match() {
        (bs, I) => Bits::make(bs, O)
        (bs, O) => Bits::make(bs.dec(), I)
      }
  }
}

// section end inc_dec

// section start lsb

///|
fn lsb(self : Bits) -> Bits {
  match self {
    Rep(O) => Rep(O)
    s =>
      match s.pat_match() {
        (bs, O) => Bits::make(bs.lsb(), O)
        (_, I) => Bits::make(Rep(O), I)
      }
  }
}

// section end lsb

// section start test2

///|
test "lsb" {
  inspect(Bits::to_bits(26), content="...00011010")
  inspect(Bits::to_bits(26).lsb(), content="...00010")
  inspect(Bits::to_bits(24), content="...00011000")
  inspect(Bits::to_bits(24).lsb(), content="...0001000")
}

// section end test2

// section start bit_and

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

// section end bit_and

// section start bit_not

///|
fn Bits::inv(self : Bits) -> Bits {
  match self {
    Rep(x) => Rep(x.not())
    s =>
      match s.pat_match() {
        (bs, b) => Bits::make(bs.inv(), b.not())
      }
  }
}

// section end bit_not

// section start op_add

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

// section end op_add

// section start op_neg

///|
impl Neg for Bits with op_neg(self) {
  self.inv().inc()
}

// section end op_neg

// section start test_add

///|
test "add" {
  @qc.quick_check_fn(fn(x : (Int, Int)) {
    x.0 + x.1 == Bits::from_bits(Bits::to_bits(x.0) + Bits::to_bits(x.1))
  })
  // +++ [100/0/100] Ok, passed!
}

// section end test_add

// section start helpers

///|
fn set_to(self : Bits, idx : Int, b1 : Bit) -> Bits {
  match (idx, self.pat_match()) {
    (0, (bs, _)) => Bits::make(bs, b1)
    (k, (bs, b)) => Bits::make(bs.set_to(k - 1, b1), b)
  }
}

///|
fn Bits::set(self : Bits, idx : Int) -> Bits {
  self.set_to(idx, I)
}

///|
fn Bits::clear(self : Bits, idx : Int) -> Bits {
  self.set_to(idx, O)
}

///|
fn test_helper(self : Bits, i : Int) -> Bool {
  loop (i, self.pat_match()) {
    (0, (_bs, b)) => b == I
    (k, (bs, _b)) => continue (k - 1, bs.pat_match())
  }
}

///|
fn odd(self : Bits) -> Bool {
  self.test_helper(0)
}

///|
fn even(self : Bits) -> Bool {
  not(self.odd())
}

// section end helpers

// section start shift

///|
fn shr(self : Bits) -> Bits {
  self.pat_match().0
}

///|
fn shl(self : Bits) -> Bits {
  Bits::make(self, O)
}

///|
fn[A] while_(p : (A) -> Bool, f : (A) -> A, x : A) -> A {
  loop x {
    x => if p(x) { continue f(x) } else { x }
  }
}

// section end shift
