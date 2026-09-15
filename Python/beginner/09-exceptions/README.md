# Python Exceptions Cheatsheet

Chinese version: [README_ZH.md](README_ZH.md)

## Mental model

> `try`/`except`/`else`/`finally` are four mutually exclusive-or-guaranteed blocks: exactly one of `except` or `else` runs depending on whether an exception occurred, and `finally` always runs regardless.

```mermaid
flowchart TD
    accTitle: try/except/else/finally execution order
    accDescr: The try block runs first. If it raises a matching exception, the except block runs; otherwise the else block runs. The finally block always runs last, whether or not an exception occurred.
    T[Run try block] --> R{Exception raised?}
    R -- Yes, matches except --> EX[Run except block]
    R -- No --> EL[Run else block]
    EX --> F[Run finally block]
    EL --> F
    F --> D[Continue after statement]
```

```python
try:
    port = int(raw_port)
except ValueError as error:
    print(f"invalid port: {error}")
else:
    connect(port)
finally:
    cleanup()
```

Catch the narrowest expected exception. `else` runs only when no exception occurs; `finally` runs whether an exception occurs or not.

```python
if not 1 <= port <= 65535:
    raise ValueError("port must be between 1 and 65535")

try:
    load_config()
except OSError as error:
    raise RuntimeError("could not load configuration") from error
```

Do not use a bare `except:` unless you must also intercept process-exit and cancellation signals. Avoid silently swallowing errors.
