# Python 类速查表

English version: [README.md](README.md)

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
