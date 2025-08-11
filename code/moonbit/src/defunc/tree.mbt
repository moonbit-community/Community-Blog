// section start define

///|
enum Tree[T] {
  Leaf(T)
  Node(T, Tree[T], Tree[T])
}
// section end define

// section start pre_order

///|
fn[T] pre_order(tree : Tree[T], f : (T) -> Unit) -> Unit {
  match tree {
    Leaf(x) => f(x)
    Node(x, left, right) => {
      f(x)
      pre_order(left, f)
      pre_order(right, f)
    }
  }
}

// section end pre_order
