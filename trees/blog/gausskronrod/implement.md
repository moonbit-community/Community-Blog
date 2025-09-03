---
title: Gauss-Kronrod 求积算法实现
collect: true
---

如下为 moonbit 实现，其中 abscissae 与 weights可以通过查表得到。为达到精度要求，使用二分法进行递归求积。

```moonbit
pub fn quad(func : (Double) -> Double, a : Double, b : Double) -> Double {
  fn recursiveQuad(
    func : (Double) -> Double,
    a : Double,
    b : Double,
    accuracy: Double,
  ) -> Double {
    let gaussAbscissae : FixedArray[Double] = [
      0.0, -4.058451513773971669066064120769615e-1, 4.058451513773971669066064120769615e-1,
      -7.415311855993944398638647732807884e-1, 7.415311855993944398638647732807884e-1,
      -9.491079123427585245261896840478513e-1, 9.491079123427585245261896840478513e-1,
    ]
    let gaussWeights : FixedArray[Double] = [
      4.179591836734693877551020408163265e-1, 3.818300505051189449503697754889751e-1,
      3.818300505051189449503697754889751e-1, 2.797053914892766679014677714237796e-1,
      2.797053914892766679014677714237796e-1, 1.29484966168869693270611432679082e-1,
      1.29484966168869693270611432679082e-1,
    ]
    let kronrodAbscissae : FixedArray[Double] = gaussAbscissae +
      [
        -2.077849550078984676006894037732449e-1, 2.077849550078984676006894037732449e-1,
        -5.860872354676911302941448382587296e-1, 5.860872354676911302941448382587296e-1,
        -8.648644233597690727897127886409262e-1, 8.648644233597690727897127886409262e-1,
        -9.914553711208126392068546975263285e-1, 9.914553711208126392068546975263285e-1,
      ]
    let kronrodWeights : FixedArray[Double] = [
      2.094821410847278280129991748917143e-1, 1.903505780647854099132564024210137e-1,
      1.903505780647854099132564024210137e-1, 1.406532597155259187451895905102379e-1,
      1.406532597155259187451895905102379e-1, 6.309209262997855329070066318920429e-2,
      6.309209262997855329070066318920429e-2, 2.044329400752988924141619992346491e-1,
      2.044329400752988924141619992346491e-1, 1.690047266392679028265834265985503e-1,
      1.690047266392679028265834265985503e-1, 1.04790010322250183839876322541518e-1,
      1.04790010322250183839876322541518e-1, 2.293532201052922496373200805896959e-2,
      2.293532201052922496373200805896959e-2,
    ]
    let halfH = (b - a) / 2
    let mut guassResult = 0.0
    let mut kronrodResult = 0.0
    for i = 0; i < gaussAbscissae.length(); i = i + 1 {
      let xi = halfH * gaussAbscissae[i] + a + halfH
      let yi = func(xi)
      guassResult += gaussWeights[i] * yi
      kronrodResult += kronrodWeights[i] * yi
    }
    for i = gaussAbscissae.length(); i < kronrodAbscissae.length(); i = i + 1 {
      let xi = halfH * kronrodAbscissae[i] + a + halfH
      let yi = func(xi)
      kronrodResult += kronrodWeights[i] * yi
    }
    fn abs(x: Double) {
      if x < 0 {
        -x
      } else {
        x
      }
    }
    if abs(kronrodResult - guassResult) < accuracy / halfH {
      kronrodResult * halfH
    } else {
      let m = a + (b - a) / 2
      let acc = accuracy / 2
      recursiveQuad(func, a, m, acc) + recursiveQuad(func, m, b, acc)
    }
  }
  recursiveQuad(func, a, b, 1.0e-15)
}
```