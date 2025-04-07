---
title: Defunctionalization: A Taste on Filter DSL
collect: true
---

让我们以循序渐进的方式展开论述。
作为切入点，不妨考察一个具有典型性的基础案例：设想需要实现过滤函数 `filter`，该函数接收列表与谓词函数作为输入，返回满足谓词条件的所有元素构成的新列表。
采用递归策略可达成如下实现：

```moonbit
fn filter[T](xs : List[T], pred : (T) -> Bool) -> List[T] {
  match xs {
    Nil => Nil
    Cons(x, xs) if pred(x) => Cons(x, filter(xs, pred))
    Cons(_, xs) => filter(xs, pred)
  }
}
```

此处 `pred` 作为高阶函数的特性引发了一个本质性问题：在底层编译场景中（如将MoonBit编译至C语言时），函数无法以常规数据结构的形式进行存储与传递。换言之，在目标语言层面，一等函数的直接表示存在根本性限制。

最直观的解决思路莫过于穷举法——将所有可能用到的谓词函数进行枚举编码。以下示例展示了针对整数的几种基本谓词：

```moonbit
enum Filter {
  IsEven
  IsOdd
  IsPositive
  IsNegative
}

fn run(self : Filter, data : Int) -> Bool {
  match self {
    IsEven => data % 2 == 0
    IsOdd => data % 2 != 0
    IsPositive => data > 0
    IsNegative => data < 0
  }
}
```

借此定义，可重构出经过去函数化处理的过滤函数：

```moonbit
fn filter_defunct(xs : List[Int], pred : Filter) -> List[Int] {
  match xs {
    Nil => Nil
    Cons(x, xs) if run(pred, x) => Cons(x, filter_defunct(xs, pred))
    Cons(_, xs) => filter_defunct(xs, pred)
  }
}
```

然而此方案存在明显局限性。
诚然，高阶谓词函数的集合实为不可数无穷集，这使得完备枚举在理论上即不可行。
但通过代数数据类型的参数化特性，我们可获得某种程度上的延展能力。
例如将`IsNegative`推广为带参数的`IsLessThan`：

```moonbit
enum Filter {
  ...
  IsLessThan(Int)
}

fn run(self : Filter, data : Int) -> Bool {
  match self {
    IsLessThan(n) => data < n
    ...
  }
}
```

更富启发性的是引入复合逻辑结构。
通过增加`And`等逻辑连接词，可实现谓词函数的组合运算：

```moonbit
enum Filter {
  ...
  And(Filter, Filter)
}
fn run(self : Filter, data : Int) -> Bool {
  match self {
    And(f1, f2) => run(f1, data) && run(f2, data)
    ...
  }
}
```

经过这般层层抽象，我们所构建的`Filter`类型本质上已演变为一种领域特定语言（Domain-Specific Language）。
建议感兴趣的读者可进一步探索其 Parser 与 Pretty Printer 的实现路径，以完善该DSL的序列化能力。

但必须指出，这种基于代数数据类型的方案存在固有的封闭性缺陷——每新增一个枚举成员都需要修改所有相关的模式匹配逻辑（本案例中的`run`函数）。
这与高阶函数与生俱来的开放性形成鲜明对比：后者允许在不修改现有代码的前提下自由扩展新函数。
