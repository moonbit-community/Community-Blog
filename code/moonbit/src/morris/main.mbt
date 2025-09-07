///|
fn main {
  let tree = build_BST(1, 10)
  let after_root = left_most_node(tree)
  let before = dump_without_nil(tree).to_string()
  morris_tree_traversal_pattern_match(tree, _ => ())
  let after = dump_without_nil(after_root).to_string()
  try! @fs.write_string_to_file("./out/before.dot", before, encoding="utf8")
  try! @fs.write_string_to_file("./out/after.dot", after, encoding="utf8")
}
