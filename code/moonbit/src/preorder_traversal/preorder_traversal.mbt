// section start define

///|
priv enum Tree[A] {
  Nil
  Node(A, Tree[A], Tree[A])
}

// section end define

// section start preorder

///|
fn[A] Tree::preorder(self : Tree[A], f : (A) -> Unit) -> Unit {
  fn dfs(root) {
    match root {
      Nil => ()
      Node(x, left, right) => {
        f(x)
        dfs(left)
        dfs(right)
      }
    }
  }

  dfs(self)
}

// section end preorder

// section start preorder_stack

///|
fn[A] Tree::preorder_stack(self : Tree[A], f : (A) -> Unit) -> Unit {
  let stack = Array::new(capacity=4096)
  stack.push(self)
  while not(stack.is_empty()) {
    let root = stack.unsafe_pop()
    match root {
      Nil => ()
      Node(x, left, right) => {
        f(x)
        stack.push(right) // 先进后出， 先被压入后处理
        stack.push(left) // 先处理左节点
      }
    }
  }
}

// section end preorder_stack

// section start final

///|
fn Tree::from_n(n : Int) -> Tree[Int] {
  let mut i = 0
  fn dfs() {
    if i < n {
      let x = i
      i += 1
      let res = Node(x, dfs(), dfs())
      res
    } else {
      Nil
    }
  }

  dfs()
}

///|
fn test_preorder(root : Tree[Int]) -> Unit raise {
  let b1 = StringBuilder::new()
  let b2 = StringBuilder::new()
  root.preorder(fn(x) { b1.write_object(x) })
  root.preorder_stack(fn(x) { b2.write_object(x) })
  assert_eq(b1.to_string(), b2.to_string())
}

///|
test "preorder/preorder_stack" {
  let t1 = Node(
    1,
    Node(2, Nil, Nil),
    Node(3, Node(4, Nil, Nil), Node(5, Nil, Nil)),
  )
  let mut sum = 0
  t1.preorder(fn(x) { sum += x })
  inspect(sum, content="15")
  let t2 = Tree::from_n(15)
  test_preorder(t2)
}

// section end final
