# Python Classes Cheatsheet

Chinese version: [README_ZH.md](README_ZH.md)

## Mental model

> A class is a template for objects that bundle state (attributes) with behavior (methods) bound to `self`. Choose the binding that matches what the method needs:

| Decorator | Receives | Use for |
| --- | --- | --- |
| (none) | `self` (the instance) | Behavior that reads or changes instance state |
| `@classmethod` | `cls` (the class) | Alternative constructors, behavior shared across instances |
| `@staticmethod` | nothing implicit | Behavior that belongs in the class namespace but touches neither instance nor class state |

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
