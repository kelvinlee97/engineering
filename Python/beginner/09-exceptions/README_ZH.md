# Python 异常速查表

English version: [README.md](README.md)

## 心智模型

> `try`/`except`/`else`/`finally` 是四个互斥或必定执行的代码块：根据是否发生异常，`except` 和 `else` 中恰好一个会执行；`finally` 无论如何都会执行。

```mermaid
flowchart TD
    accTitle: try/except/else/finally 执行顺序
    accDescr: 先执行 try 代码块。如果抛出匹配的异常，就执行 except 代码块；否则执行 else 代码块。finally 代码块无论是否发生异常都会最后执行。
    T[执行 try 代码块] --> R{是否抛出异常?}
    R -- 是，且匹配 except --> EX[执行 except 代码块]
    R -- 否 --> EL[执行 else 代码块]
    EX --> F[执行 finally 代码块]
    EL --> F
    F --> D[语句结束后继续]
```

```python
try:
    port = int(raw_port)
except ValueError as error:
    print(f"端口无效：{error}")
else:
    connect(port)
finally:
    cleanup()
```

只捕获预期的最具体异常。没有异常时才执行 `else`；无论是否发生异常都会执行 `finally`。

```python
if not 1 <= port <= 65535:
    raise ValueError("端口必须介于 1 和 65535 之间")

try:
    load_config()
except OSError as error:
    raise RuntimeError("无法载入配置") from error
```

除非确实需要拦截程序退出和取消信号，否则不要使用裸 `except:`。不要静默忽略错误。
