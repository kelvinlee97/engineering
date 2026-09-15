# Python 模块与包速查表

English version: [README.md](README.md)

## 心智模型

> 模块是由单个文件构成的命名空间，包是由一个模块目录构成的命名空间。导入会执行一次目标文件，并把名称绑定进导入方的命名空间，这也是 `if __name__ == "__main__":` 能区分「被导入」和「直接运行」的原因。

每个 `.py` 文件都是模块；包含模块的目录可以组成包。

```python
import json
from pathlib import Path
from mypackage.parsers import parse_log
```

默认使用绝对导入。避免 `from module import *`，因为它会隐藏名称的来源。

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

该判断只在直接执行模块时运行代码，导入模块时不会运行。可使用 `python -m mypackage.cli` 执行包中的模块。
