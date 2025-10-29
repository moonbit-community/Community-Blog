
#set page(width: auto, height: auto, margin: (x: 0.1em, y: 0em), fill: rgb(0, 0, 0, 0)); 
#set text(size: 13.2pt, top-edge: "bounds", bottom-edge: "bounds");

#import "@preview/fletcher:0.5.4" as fletcher: node, edge

#align(center)[
  #figure(fletcher.diagram(
    node-stroke: 0.7pt,
    crossing-fill: rgb(0, 0, 0, 0), 
    
    node((0, 0), $1$),
    node((1.5, 0), $2$),
    edge((0, 0), (0, 0), "-|>", bend: 130deg, label: $a$),
    edge((1.5, 0), (1.5, 0), "-|>", bend: 130deg, label: $d$),
    edge((0, 0), (1.5, 0), $b$, "-|>", bend: 15deg),
    edge((1.5, 0), (0, 0), $c$, "-|>", bend: 15deg),
  ))
]
