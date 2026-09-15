# Python 文件与路径速查表

English version: [README.md](README.md)

## 心智模型

> `Path` 对象只表示位置，不是已经打开的资源；打开文件（`open()`、`with`）是单独的一步，必须与关闭配对，而 `with` 会自动完成关闭。

使用 `pathlib.Path` 处理文件系统路径：

```python
from pathlib import Path

path = Path("logs") / "app.log"
path.exists()
path.is_file()
path.parent
path.name
path.suffix
```

```python
text = path.read_text(encoding="utf-8")
path.write_text("ready\n", encoding="utf-8")

with path.open(encoding="utf-8") as file:
    for line in file:
        print(line.rstrip())
```

处理大文件时应逐行遍历，不要调用 `read_text()`。以 `"w"` 模式打开会覆盖现有内容，`"a"` 模式会追加内容。非文本数据使用 `read_bytes()` 等二进制方法。
