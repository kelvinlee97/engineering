# Python Strings Cheatsheet

Chinese version: [README_ZH.md](README_ZH.md)

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

Strings are immutable: methods return new strings. Use `str.split()` without an argument to split on any whitespace. Use raw strings for regular-expression and Windows-path literals when backslashes should remain literal: `r"\d+"`.
