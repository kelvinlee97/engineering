# Python 测试速查表

English version: [README.md](README.md)

小型测试套件使用标准库的 `unittest` 已足够：

```python
import unittest


def add(left: int, right: int) -> int:
    return left + right


class AddTests(unittest.TestCase):
    def test_adds_two_numbers(self) -> None:
        self.assertEqual(add(2, 3), 5)

    def test_rejects_wrong_type(self) -> None:
        with self.assertRaises(TypeError):
            add(2, "3")


if __name__ == "__main__":
    unittest.main()
```

使用 `python -m unittest discover` 运行测试。每个测试应专注于可观察行为；覆盖正常情况、有意义的边界和已知回归，不要测试实现细节。
