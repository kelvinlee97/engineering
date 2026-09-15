# Python 类速查表

English version: [README.md](README.md)

## 心智模型

> 类是对象的模板，把状态（属性）和绑定到 `self` 的行为（方法）打包在一起。应根据方法实际需要的绑定方式来选择：

| 装饰器 | 接收到的第一个参数 | 适用场景 |
| --- | --- | --- |
| （无） | `self`（实例本身） | 需要读取或修改实例状态的行为 |
| `@classmethod` | `cls`（类本身） | 替代构造器，或所有实例共享的行为 |
| `@staticmethod` | 无隐式参数 | 逻辑上属于类命名空间，但既不需要实例也不需要类状态的行为 |

主要用于保存数据的小型类可以使用数据类：

```python
from dataclasses import dataclass


@dataclass
class Service:
    name: str
    port: int = 443

    @property
    def address(self) -> str:
        return f"{self.name}:{self.port}"


api = Service("api", 8080)
```

实例方法接收 `self`。替代构造器使用 `@classmethod`；行为属于类的命名空间，但不需要实例或类状态时才使用 `@staticmethod`。除非对象之间确实存在“是一种”的关系，否则组合通常比继承更合适。
