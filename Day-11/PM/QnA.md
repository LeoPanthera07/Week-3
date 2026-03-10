## Q1 — Complete execution flow of `try / except / else / finally`

### Basic idea

Python executes the blocks in this general order:

1. `try`
2. `except` (only if an exception happens in `try`)
3. `else` (only if no exception happens in `try`)
4. `finally` (always runs, whether there was an exception or not)[web:275][web:279][web:273]

### When each block executes

- **`try`**  
  Contains code that may raise an exception.[web:279][web:299]

- **`except`**  
  Runs only if a matching exception is raised inside the `try` block.[web:275][web:279]

- **`else`**  
  Runs only when the `try` block completes successfully without raising an exception.[web:271][web:275]

- **`finally`**  
  Always runs before leaving the `try` statement, whether the code succeeded, failed, returned early, or raised an exception.[web:279][web:296]

### Example using all four blocks

```python
def divide_numbers(a, b):
    try:
        print("Inside try")
        result = a / b
    except ZeroDivisionError as e:
        print(f"Inside except: {e}")
    else:
        print(f"Inside else: result = {result}")
    finally:
        print("Inside finally: cleanup always happens")


divide_numbers(10, 2)
print("---")
divide_numbers(10, 0)
```

### What happens here?

If `b = 2`:

- `try` runs successfully
- `except` is skipped
- `else` runs
- `finally` runs at the end[web:271][web:275]

If `b = 0`:

- `try` raises `ZeroDivisionError`
- matching `except` runs
- `else` is skipped
- `finally` still runs[web:275][web:279]

### What if an exception occurs inside the `else` block?

If an exception happens inside `else`, that exception is **not** handled by the earlier `except` clauses attached to the `try`, because `except` only handles exceptions from the `try` block itself.[web:271][web:279]  
However, `finally` still runs before the new exception propagates outward.[web:279][web:296]

Example:

```python
def demo():
    try:
        print("try block success")
    except ValueError:
        print("except block")
    else:
        print("else block starts")
        raise RuntimeError("Error inside else")
    finally:
        print("finally block always runs")

demo()
```

Output behavior:

- `try` succeeds
- `except` is skipped
- `else` starts
- `RuntimeError` is raised inside `else`
- `finally` runs
- then the error propagates unless caught elsewhere

---

## Q2 — Coding: `safe_json_load(filepath)`

### Solution

```python
import json
import logging

logging.basicConfig(
    filename="json_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def safe_json_load(filepath):
    """
    Safely read and parse a JSON file.

    Args:
        filepath: Path to the JSON file.

    Returns:
        Parsed dictionary on success, otherwise None.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError("JSON content is not a dictionary")

    except FileNotFoundError as e:
        logging.error("File not found: %s", e)
        return None
    except json.JSONDecodeError as e:
        logging.error("Invalid JSON in %s: %s", filepath, e)
        return None
    except PermissionError as e:
        logging.error("Permission denied for %s: %s", filepath, e)
        return None
    except ValueError as e:
        logging.error("Validation error in %s: %s", filepath, e)
        return None
    else:
        return data
```

### Why this is correct

- It handles the required exceptions:
  - `FileNotFoundError`
  - `json.JSONDecodeError`
  - `PermissionError`[web:244][web:297]
- It logs all errors using the `logging` module.[web:267][web:280]
- It returns the parsed dictionary on success and `None` on failure, exactly as required.

### Example usage

```python
config = safe_json_load("config.json")

if config is None:
    print("Could not load config.")
else:
    print("Config loaded successfully.")
```

---

## Q3 — Debug / Analyze

### Buggy code

```python
def process_data(data_list):
    results = []
    for item in data_list:
        try:
            value = int(item)
            results.append(value * 2)
        except:
            print("Error occurred")
            continue
        finally:
            return results
    return results
```

---

### Issue 1 — Bare `except`

The code uses:

```python
except:
```

This is bad practice because it catches **everything**, including `KeyboardInterrupt` and `SystemExit`, which usually should not be swallowed.[web:298][web:304][web:301]

### Fix

Catch only the exception you actually expect here, which is mainly `ValueError` when `int(item)` fails.

---

### Issue 2 — `return` inside `finally`

This is the most serious bug.

```python
finally:
    return results
```

The `finally` block always runs, so this `return` executes on the **first iteration** of the loop, which ends the function immediately.[web:279][web:296]

That means the function never processes the full list.

---

### Issue 3 — Uninformative error message

This code:

```python
print("Error occurred")
```

does not tell the user:

- which item failed
- what kind of error happened
- why it happened

That makes debugging harder.

---

### Corrected design

```python
def process_data(data_list):
    results = []

    for item in data_list:
        try:
            value = int(item)
            results.append(value * 2)
        except ValueError as e:
            print(f"Skipping invalid item {item!r}: {e}")
            continue

    return results
```

### Example

```python
print(process_data(["1", "2", "abc", "4"]))
```

Output:

```python
Skipping invalid item 'abc': invalid literal for int() with base 10: 'abc'

```

---

## Why the corrected version is better

- It catches only the expected exception (`ValueError`) instead of using a bare `except`.[web:298][web:304]
- It removes the dangerous `return` from `finally`, so the loop can process all items.[web:279][web:296]
- It gives a useful error message with the exact failing value and the exception details.

---

## Quick Summary

### `try / except / else / finally`
- `try` runs first
- `except` runs only if `try` raises a matching exception
- `else` runs only if `try` succeeds
- `finally` always runs[web:275][web:279][web:273]

### `safe_json_load`
- Returns parsed dictionary on success
- Returns `None` on failure
- Logs all relevant JSON/file errors[web:244][web:267][web:297]

### Debug fixes
- Replace bare `except`
- Remove `return` from `finally`
- Improve error message quality[web:298][web:279][web:304]