///|
typealias MyList as List

// section start original_filter

///|
fn[T] filter(xs : List[T], pred : (T) -> Bool) -> List[T] {
  match xs {
    Nil => Nil
    Cons(x, xs) if pred(x) => Cons(x, filter(xs, pred))
    Cons(_, xs) => filter(xs, pred)
  }
}

// section end original_filter

// section start limited_filter

///|
enum Filter {
  IsEven
  IsOdd
  IsPositive
  IsNegative
}

///|
fn run(self : Filter, data : Int) -> Bool {
  match self {
    IsEven => data % 2 == 0
    IsOdd => data % 2 != 0
    IsPositive => data > 0
    IsNegative => data < 0
  }
}

// section end limited_filter

// section start defunc_filter

///|
fn filter_defunct(xs : List[Int], pred : Filter) -> List[Int] {
  match xs {
    Nil => Nil
    Cons(x, xs) if pred.run(x) => Cons(x, filter_defunct(xs, pred))
    Cons(_, xs) => filter_defunct(xs, pred)
  }
}
// section end defunc_filter

// section start defunc_filter_extend

///|
enum FilterExtend {
  //...
  IsLessThan(Int)
}

///|
fn run_extend(self : FilterExtend, data : Int) -> Bool {
  match self {
    IsLessThan(n) => data < n
    //...
  }
}
// section end defunc_filter_extend

// section start defunc_filter_extend_compose

///|
enum FilterExtendCompose {
  //...
  And(FilterExtend, FilterExtend)
}

///|
fn run_extend_compose(self : FilterExtendCompose, data : Int) -> Bool {
  match self {
    And(f1, f2) => f1.run_extend(data) && f2.run_extend(data)
    //...
  }
}

// section end defunc_filter_extend_compose
