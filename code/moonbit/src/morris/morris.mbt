///|
pub(all) struct Node[A] {
  mut data : A
  mut left : Node[A]?
  mut right : Node[A]?
} derive(Show)

///|
pub fn[A] clone(root : Node[A]?) -> Node[A]? {
  match root {
    None => None
    Some({ data, left, right }) =>
      Some(Node::{ data, left: clone(left), right: clone(right) })
  }
}

///|
pub fn build_BST(start : Int, end : Int) -> Node[Int]? {
  let n = end - start + 1
  if n <= 0 {
    None
  } else {
    let quot = n / 2
    let data = start + quot
    let left = build_BST(start, data - 1)
    let right = build_BST(data + 1, end)
    Some(Node::{ data, left, right })
  }
}

///|
typealias @graphviz.Digraph

///|
typealias Int as Id

///|
pub fn dump(root : Node[Int]?) -> Digraph {
  let edges = []
  let nodes = []
  let mut cnt = 0
  fn dfs(self : Node[Int]?) -> Id {
    cnt += 1
    match self {
      None => {
        let label = "nil"
        nodes.push(@graphviz.Node::new(id=cnt, label~))
        cnt
      }
      Some({ data, left, right }) => {
        let from = cnt
        let left_id = dfs(left)
        let right_id = dfs(right)
        let label = data.to_string()
        edges.push(@graphviz.Edge::new(from~, to=left_id))
        edges.push(@graphviz.Edge::new(from~, to=right_id))
        nodes.push(@graphviz.Node::new(id=from, label~))
        from
      }
    }
  }

  dfs(root) |> ignore
  Digraph::{ edges, nodes }
}

///|
pub fn dump_without_nil(root : Node[Int]?) -> Digraph {
  let edges = []
  let nodes = []
  let mut cnt = 0
  fn dfs(self : Node[Int]?) -> Id? {
    cnt += 1
    match self {
      None => None
      Some({ data, left, right }) => {
        let from = cnt
        let left_id = dfs(left)
        let right_id = dfs(right)
        let label = data.to_string()
        left_id.map(fn(to) { edges.push(@graphviz.Edge::new(from~, to~)) })
        |> ignore
        right_id.map(fn(to) { edges.push(@graphviz.Edge::new(from~, to~)) })
        |> ignore
        nodes.push(@graphviz.Node::new(id=from, label~))
        Some(from)
      }
    }
  }

  dfs(root) |> ignore
  Digraph::{ edges, nodes }
}

///|
pub fn[A] right_most_node(root : Node[A]?) -> Node[A]? {
  loop root {
    None => None
    Some({ right, .. }) as prev if right.is_empty() => prev
    Some({ right, .. }) => continue right
  }
}

///|
pub fn[A] left_most_node(root : Node[A]?) -> Node[A]? {
  loop root {
    None => None
    Some({ left, .. }) as prev if left.is_empty() => prev
    Some({ left, .. }) => continue left
  }
}

///|
///  this algorithm adapted from 
/// 
///  https://medium.com/@mssandeepkamath/morris-tree-traversal-the-o-n-time-and-o-1-space-algorithm-5d2d2d47814a
pub fn[A] morris_tree_traversal(root : Node[A]?, f : (A) -> Unit) -> Unit {
  let mut cur = root
  // let mut prev = None 
  while not(cur.is_empty()) {
    if not(cur.unwrap().left.is_empty()) {
      let prev = right_most_node(cur.unwrap().left)
      prev.unwrap().right = cur
      let cur_left = cur.unwrap().left
      cur.unwrap().left = None
      cur = cur_left
    } else {
      f(cur.unwrap().data)
      cur = cur.unwrap().right
    }
  }
}

// section start inorder_recursive
///|
/// Traditional recursive inorder traversal
pub fn[A] inorder_recursive(root : Node[A]?, f : (A) -> Unit) -> Unit {
  match root {
    None => ()
    Some({ left, data, right }) => {
      inorder_recursive(left, f)
      f(data)
      inorder_recursive(right, f)
    }
  }
}
// section end inorder_recursive

// section start inorder_iterative
///|
/// Traditional iterative inorder traversal using stack
pub fn[A] inorder_iterative(root : Node[A]?, f : (A) -> Unit) -> Unit {
  let stack : Array[Node[A]] = []
  let mut current = root
  
  while not(stack.is_empty()) || current is Some(_) {
    while current is Some(_) {
      stack.push(current.unwrap())
      current = current.unwrap().left
    }
    
    let node = stack.unsafe_pop()
    f(node.data)
    current = node.right
  }
}
// section end inorder_iterative

// section start morris
///|
pub fn[A] morris_tree_traversal_pattern_match(
  root : Node[A]?,
  f : (A) -> Unit,
) -> Unit {
  loop root {
    None => break
    // This part of the code is responsible for transforming the tree into a right-skewed tree
    Some({ left: Some(_) as left, .. } as cur_) as cur => {
      // The rightmost node of the left subtree is the predecessor of the last node visited in the left subtree during inorder traversal, where the last node is the root of the left subtree
      guard right_most_node(left) is Some(left_subtree_last_visited_node)
      // Create a back edge here so that after visiting the left subtree, we can return to the root of the left subtree
      left_subtree_last_visited_node.right = cur
      let cur_left = cur_.left

      // This step prevents infinite loops when traversing through the previously created back edge
      cur_.left = None

      // Continue visiting the left subtree
      continue cur_left
    }
    Some(cur_) => {
      // At this point the tree has become a right-skewed tree, with no more left subtrees
      f(cur_.data)
      // Simply continue visiting the right subtree
      continue cur_.right
    }
  }
}
// section end morris
  
///|
test "BST structure visualization" (t : @test.T) {
  t.writeln(dump_without_nil(build_BST(0, 8)))
  t.snapshot(filename="bst_structure_visualization.dot")
}

///|
test "C style" (t : @test.T) {
  let tree = build_BST(0, 8)
  let xs = []
  morris_tree_traversal(tree, fn(x) { xs.push(x) })
  inspect(xs, content="[0, 1, 2, 3, 4, 5, 6, 7, 8]")
  t.writeln(dump_without_nil(build_BST(0, 8)))
  t.snapshot(filename="morris_traversal_c_style.dot")
}

///|
test "Moonbit style" (t : @test.T) {
  let tree = build_BST(0, 8)
  let xs = []
  morris_tree_traversal_pattern_match(tree, fn(x) { xs.push(x) })
  inspect(xs, content="[0, 1, 2, 3, 4, 5, 6, 7, 8]")
  t.writeln(dump_without_nil(build_BST(0, 8)))
  t.snapshot(filename="morris_traversal_moonbit_style.dot")
}

///|
test "Traditional recursive traversal" {
  let tree = build_BST(0, 8)
  let xs = []
  inorder_recursive(tree, fn(x) { xs.push(x) })
  inspect(xs, content="[0, 1, 2, 3, 4, 5, 6, 7, 8]")
}

///|
test "Traditional iterative traversal" {
  let tree = build_BST(0, 8)
  let xs = []
  inorder_iterative(tree, fn(x) { xs.push(x) })
  inspect(xs, content="[0, 1, 2, 3, 4, 5, 6, 7, 8]")
}
