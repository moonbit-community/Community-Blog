// section start pre_order_cps

///|
fn[T : Show] pre_order_cps(self : Tree[T], f : (T) -> Unit) -> Unit {
  fn go {
    Leaf(x), k => k(f(x))
    Node(x, left, right), k => {
      f(x)
      go(left, fn { _ => go(right, k) })
    }
  }

  go(self, fn { x => x })
}
// section end pre_order_cps

// section start tree_cont

///|
enum TreeCont[T] {
  Return
  Next(Tree[T], TreeCont[T])
}
// section end tree_cont

// section start pre_order_cps_defunct

///|
fn[T : Show] pre_order_cps_defunct(self : Tree[T], f : (T) -> Unit) -> Unit {
  fn run_cont {
    Next(tree, k) => go(tree, k)
    Return => ()
  }

  fn go {
    Leaf(x), k => {
      f(x)
      run_cont(k)
    }
    Node(x, left, right), k => {
      f(x)
      go(left, Next(right, k))
    }
  }

  go(self, Return)
}
// section end pre_order_cps_defunct

// section start pre_order_cps_defunct_loop

///|
fn[T : Show] pre_order_cps_defunct_loop(
  self : Tree[T],
  f : (T) -> Unit
) -> Unit {
  loop self, Return {
    Leaf(x), k => {
      f(x)
      match k {
        Next(tree, k) => continue tree, k
        Return => ()
      }
    }
    Node(x, left, right), k => {
      f(x)
      continue left, Next(right, k)
    }
  }
}
// section end pre_order_cps_defunct_loop

// section start pre_order_loop

///|
fn[T : Show] pre_order_loop(self : Tree[T], f : (T) -> Unit) -> Unit {
  let mut k = Return
  let mut t = self
  while true {
    match t {
      Leaf(x) => {
        f(x)
        match k {
          Next(tree, next) => {
            k = next
            t = tree
          }
          Return => break
        }
      }
      Node(x, left, right) => {
        f(x)
        k = Next(right, k)
        t = left
      }
    }
  }
}
// section end pre_order_loop

// section start pre_order_loop_stack

///|
fn[T : Show] pre_order_loop_stack(self : Tree[T], f : (T) -> Unit) -> Unit {
  let k = []
  let mut t = self
  while true {
    match t {
      Leaf(x) => {
        f(x)
        match k.pop() {
          Some(tree) => t = tree
          None => break
        }
      }
      Node(x, left, right) => {
        f(x)
        k.push(right)
        t = left
      }
    }
  }
}
// section end pre_order_loop_stack
