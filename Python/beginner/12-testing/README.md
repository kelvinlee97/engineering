# Python Testing Cheatsheet

> A test asserts observable behavior for a given input, independent of how the code is implemented internally, so it keeps passing after a safe refactor and fails when behavior actually breaks.

The standard library's `unittest` is enough for a small test suite:

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

Run with `python -m unittest discover`. Keep each test focused on observable behavior. Cover a normal case, meaningful boundaries, and known regressions; avoid testing implementation details.
