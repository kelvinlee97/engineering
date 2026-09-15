# Python 装饰器速查表

English version: [README.md](README.md)

## 心智模型

> 写在函数定义上方的 `@trace` 只是重新赋值的语法糖：等价于 `deploy = trace(deploy)`。名字 `deploy` 最终绑定到包装函数上，因此之后每次调用 `deploy(...)` 实际上先调用的是包装函数。

```mermaid
sequenceDiagram
    accTitle: 装饰器的包装过程与调用期间接调用
    accDescr: 定义阶段，trace(deploy) 用返回的包装函数替换了名字 deploy。调用阶段，调用 deploy 实际调用的是包装函数，它先运行自己的逻辑，再调用原始函数。
    Note over Definition: 定义阶段
    Definition->>trace: trace(deploy)
    trace-->>Definition: 返回包装函数
    Definition->>Definition: deploy = 包装函数
    Note over Caller: 调用阶段
    Caller->>wrapper: deploy(service)
    wrapper->>wrapper: print(function.__name__)
    wrapper->>original: function(service)
    original-->>wrapper: 返回值
    wrapper-->>Caller: 返回值
```

装饰器接收一个可调用对象，并返回一个可调用对象。

```python
from collections.abc import Callable
from functools import wraps


def trace(function: Callable[..., object]) -> Callable[..., object]:
    @wraps(function)
    def wrapper(*args: object, **kwargs: object) -> object:
        print(function.__name__)
        return function(*args, **kwargs)

    return wrapper


@trace
def deploy(service: str) -> None:
    print(f"正在部署 {service}")
```

`@trace` 等同于 `deploy = trace(deploy)`。使用 `functools.wraps`，让包装函数保留原函数的名称和文档。不需要把行为应用到多个函数时，直接调用函数会更清楚。
