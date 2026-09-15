# Python Files and Paths Cheatsheet

Chinese version: [README_ZH.md](README_ZH.md)

## Mental model

> `Path` objects represent locations, not open resources; opening (`open()`, `with`) is a separate step that must be paired with closing, which `with` does automatically.

Use `pathlib.Path` for filesystem paths:

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

Iterate over the file for large inputs instead of calling `read_text()`. Opening with mode `"w"` replaces existing content; mode `"a"` appends. Use binary methods such as `read_bytes()` for non-text data.
