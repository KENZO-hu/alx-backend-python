# Unit Tests for `utils.py`

This repository contains unit tests for utility functions defined in the `utils.py` module. These tests are written using Python's built-in `unittest` framework and the `parameterized` library for cleaner, data-driven tests.

## 📂 Files

- `utils.py`: Module containing utility functions such as `access_nested_map` and `get_json`.
- `test_utils.py`: Unit test file for functions in `utils.py`.

## ✅ Tested Functions

### `access_nested_map(nested_map, path)`
Accesses a value in a nested map using a tuple path.

**Examples:**
```python
access_nested_map({"a": 1}, ("a",))          # Returns 1
access_nested_map({"a": {"b": 2}}, ("a",))    # Returns {"b": 2}
access_nested_map({"a": {"b": 2}}, ("a", "b"))# Returns 2
