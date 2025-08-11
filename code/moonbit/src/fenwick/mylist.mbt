///|
priv enum MyList[T] {
  Nil
  Cons(T, MyList[T])
} derive(Show)

///|
fn[T] from_iter(iter : Iter[T]) -> MyList[T] {
  let mut list = Nil
  for x in iter {
    list = Cons(x, list)
  }
  list
}
