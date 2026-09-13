# Python Classes Cheatsheet

Chinese version: [README_ZH.md](README_ZH.md)

Use a data class for a small class whose main job is storing data:

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

Instance methods receive `self`. Use `@classmethod` for an alternative constructor and `@staticmethod` only for behavior that belongs in the class namespace but needs no instance or class state. Prefer composition over inheritance unless objects have a genuine “is-a” relationship.
