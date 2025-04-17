#import "@preview/fletcher:0.5.7" as fletcher: diagram, node, edge
#set page(width: auto, height: auto, margin: (x: 0.1em, y: 0.2em), fill: rgb(0, 0, 0, 0)); 
#set text(size: 14pt, top-edge: "bounds", bottom-edge: "bounds");
#import "@preview/fletcher:0.5.7" as fletcher: diagram, node, edge

#let bent-edge(from, to, ..args) = {
  let midpoint = (from, 50%, to)
  let vertices = (
    from,
    (from, "|-", midpoint),
    (midpoint, "-|", to),
    to,
  )
  edge(..vertices, "-|>", ..args)
}

#diagram(
  node-stroke: luma(30%),
  edge-corner-radius: none,
  spacing: (10pt, 20pt),

  // Nodes
  node((1.5,0), [*Luna-Generic*], name: <a>),
  node((0.5,1.3), [*Luna-Utils*], name: <b>),
  node((2.5,1.3), [*Data Structures*], name: <c>),

	node((0.5,2.4), [*require*], name: <x>),
  
  node((2,2.5), [*complex*], name: <f>),
  node((3,2.5), [*quaternion*], name: <g>),
	node((4,2.5), $dots.c$, name: <h>),

	node((-1,3.5), [*Poly*], name: <d>),
  node((0,3.5), [*LinearAlg*], name: <e>),
  node((1,3.5), [*Calculus*], name: <i>),

  // Edges
  bent-edge(<a>, <b>),
  bent-edge(<a>, <c>),
  bent-edge(<x>, <d>),
	bent-edge(<x>, <e>),
	bent-edge(<x>, <i>),
  bent-edge(<c>, <f>),
  bent-edge(<c>, <g>),
  bent-edge(<c>, <h>),
	edge((rel: (0,0), to: <c>), <x>, "-|>", stroke: orange, label-angle: auto),
	edge((rel: (0,0), to: <b>), <x>, "-|>", stroke: orange, label-angle: auto)
)