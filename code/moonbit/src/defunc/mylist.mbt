///|
#alias(List)
priv enum MyList[T] {
  Nil
  Cons(T, MyList[T])
}

///|
impl[T : Show] Show for MyList[T] with output(self, logger) {
  logger.write_string("@list.of([")
  fn go(xs : MyList[T], first : Bool) -> Unit {
    match xs {
      Nil => ()
      Cons(x, xs) => {
        if !first {
          logger.write_string(", ")
        }
        logger.write_object(x)
        go(xs, false)
      }
    }
  }
  go(self, true)
  logger.write_string("])")
}

///|
fn[T] from_iter(iter : Iter[T]) -> MyList[T] {
  match iter.next() {
    Some(x) => Cons(x, from_iter(iter))
    None => Nil
  }
}
