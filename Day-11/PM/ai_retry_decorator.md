## Exact Prompt Used

> Write a Python decorator called `@retry(max_attempts=3, delay=1)` that automatically retries a function if it raises an exception, with exponential backoff.

---

## AI-Generated Code

```python
import time

def retry(max_attempts=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_delay = delay

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(current_delay)
                    current_delay *= 2

        return wrapper
    return decorator
```

---

## Testing the Decorator

### Test code

```python
import random

@retry(max_attempts=3, delay=1)
def unstable_function():
    if random.random() < 0.5:
        raise ValueError("Random failure")
    return "Success"


for _ in range(5):
    try:
        print(unstable_function())
    except ValueError as e:
        print("Final failure:", e)
```

### What this test does

The function fails about 50% of the time because `random.random() < 0.5` is true roughly half the time.  
This makes it a simple way to test whether the retry decorator actually retries before finally giving up.

---

## Critical Evaluation

The AI-generated decorator gets the main retry idea right: it wraps a function, retries on exceptions, and doubles the delay after each failure, which is the core of exponential backoff.[web:307][web:308][web:310]  
It is also simple and readable, which is good for a beginner assignment.

However, it misses some important improvements. First, it does **not** use `functools.wraps`, so the wrapped function loses metadata such as its original name and docstring, which is a common decorator best practice.[web:152][web:158]  
Second, it retries **all** exceptions using `except Exception`, which is often too broad because some exceptions are not retryable and should fail immediately. A better design would let the user choose which exceptions are safe to retry.[web:307][web:311]

It also does not validate `max_attempts` or `delay`, so invalid values like `max_attempts=0` or `delay=-1` are not handled clearly.  
Another limitation is that it does not include logging, jitter, or a cap on backoff growth, all of which are useful in real systems.[web:308][web:314][web:318]  
Overall, the AI version is a solid starting point, but I would improve it by adding `functools.wraps`, argument validation, support for retryable exception types, and clearer behavior for edge cases.

---

## Improved Version

```python
import time
from functools import wraps


def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """
    Retry a function with exponential backoff.

    Args:
        max_attempts: Maximum number of attempts.
        delay: Initial delay in seconds.
        exceptions: Tuple of retryable exception types.

    Returns:
        Decorated function.

    Raises:
        ValueError: If max_attempts < 1 or delay < 0.
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    if delay < 0:
        raise ValueError("delay must be non-negative")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    print(
                        f"Attempt {attempt} failed with {type(e).__name__}: {e}. "
                        f"Retrying in {current_delay} second(s)..."
                    )
                    time.sleep(current_delay)
                    current_delay *= 2

        return wrapper

    return decorator
```

---

## Improved Test Example

```python
import random

@retry(max_attempts=4, delay=1, exceptions=(ValueError,))
def unstable_function():
    if random.random() < 0.5:
        raise ValueError("Random failure")
    return "Success"


for _ in range(5):
    try:
        print(unstable_function())
    except ValueError as e:
        print("Final failure:", e)
```

---

## Why My Version Is Better

- Uses `@wraps(func)` to preserve function metadata.[web:152][web:158][web:164]
- Validates `max_attempts` and `delay`.
- Lets you specify retryable exception types instead of retrying everything.
- Still keeps exponential backoff simple and readable.[web:307][web:311][web:314]