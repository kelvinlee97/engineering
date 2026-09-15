# Python 字符串速查表

English version: [README.md](README.md)

## 心智模型

> 字符串方法都会返回新字符串，原始文本永远不会被就地修改。

```python
text = "  api,error,503  "
text.strip()                 # "api,error,503"
text.lower()
text.upper()
text.replace("error", "ok")
text.startswith("  api")
"error" in text
```

```python
parts = "api,error,503".split(",")
line = " | ".join(parts)
service = "api"
status = 503
message = f"{service=} {status=:03d}"
```

字符串不可变，字符串方法会返回新字符串。无参数的 `str.split()` 会按任意空白拆分。当正则表达式或 Windows 路径中的反斜杠需要保留原义时，使用原始字符串，例如 `r"\d+"`。
