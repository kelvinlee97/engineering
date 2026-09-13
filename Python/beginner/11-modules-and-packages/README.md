# Python Modules and Packages Cheatsheet

Chinese version: [README_ZH.md](README_ZH.md)

Each `.py` file is a module. A directory containing modules can be a package.

```python
import json
from pathlib import Path
from mypackage.parsers import parse_log
```

Use absolute imports by default. Avoid `from module import *` because it hides where names come from.

```text
project/
├── pyproject.toml
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── cli.py
└── tests/
```

```python
def main() -> None:
    print("run")


if __name__ == "__main__":
    main()
```

The guard runs code only when the module is executed directly, not when it is imported. Run package modules with `python -m mypackage.cli`.
