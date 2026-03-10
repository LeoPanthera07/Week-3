## Q1 — `json.load()` vs `json.loads()`

### Definition of `json.load()`

`json.load()` reads JSON data from a **file object** and converts it into a Python object such as a dictionary or list.[web:237][web:244][web:247]

Example:

```python
import json

with open("config.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(data)
```

### When to use `json.load()`

Use `json.load()` when your JSON data is stored in a file on disk and you want to read it directly into Python.[web:237][web:244]

### Real-world example for `json.load()`

A common real-world example is reading an application configuration file such as `settings.json`, `credentials.json`, or a saved report file.[web:244][web:247]

Example:

```python
import json

with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

print(settings["theme"])
```

---

### Definition of `json.loads()`

`json.loads()` reads JSON data from a **string** and converts that string into a Python object.[web:237][web:238][web:241]

Example:

```python
import json

text = '{"name": "Amit", "age": 22}'
data = json.loads(text)

print(data)
```

### When to use `json.loads()`

Use `json.loads()` when the JSON content is already available in memory as a string, such as data received from an API, a message queue, a web form, or another program.[web:237][web:241][web:247]

### Real-world example for `json.loads()`

A common real-world example is receiving a JSON response from a web service as text and converting it into a Python dictionary for further processing.[web:241][web:247]

Example:

```python
import json

api_response = '{"status": "ok", "items": 5}'
result = json.loads(api_response)

print(result["status"])
```

---

### Main Difference

The core difference is simple:

- `json.load()` → reads JSON from a **file object**.[web:237][web:244]
- `json.loads()` → reads JSON from a **string**.[web:237][web:238][web:241]

A good memory trick is: the **s** in `loads()` stands for **string**.[web:240][web:250]

---

## Q2 — Coding: `find_large_files(directory, size_mb)`

### Solution

```python
from pathlib import Path


def find_large_files(directory, size_mb):
    """
    Search recursively for files larger than size_mb megabytes.

    Args:
        directory: Directory path to search in.
        size_mb: Minimum size in MB.

    Returns:
        List of tuples: (filename, size_in_mb), sorted by size descending.
    """
    base_path = Path(directory)
    limit_bytes = size_mb * 1024 * 1024
    results = []

    for path in base_path.rglob("*"):
        if path.is_file():
            size_bytes = path.stat().st_size
            if size_bytes > limit_bytes:
                size_in_mb = round(size_bytes / (1024 * 1024), 2)
                results.append((path.name, size_in_mb))

    results.sort(key=lambda x: x, reverse=True)
    return results
```

### Why this solution is correct

- It uses `pathlib.Path` as required.[web:211][web:242]
- It searches **recursively** using `rglob("*")`.[web:242][web:245]
- It gets file size using `path.stat().st_size`.[web:245][web:248]
- It returns tuples in the required format and sorts them in descending size order.

### Example

```python
files = find_large_files(".", 1)
print(files)
```

Possible output:

```python
[('movie.mp4', 25.4), ('dataset.csv', 8.7)]
```

---

## Q3 — Debug / Analyze

### Buggy Code

```python
def merge_csv_files(file_list):
    all_data = []
    for filename in file_list:
        with open(filename, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                all_data.append(row)
    
    with open("merged.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(all_data)
    
    return len(all_data)
```

---

### The 3 bugs

#### 1. Missing import

The code uses `csv.reader` and `csv.writer` but does not import the `csv` module, so it will fail with `NameError`.[web:207]

#### 2. Missing `newline=''`

When writing CSV files, especially on Windows, not using `newline=''` can produce extra blank lines between rows.[web:207][web:243][web:249]

#### 3. Header row gets duplicated

Each source CSV file has its own header row. The buggy code appends every row from every file, so the header appears multiple times in the merged file.[web:207]

---

### Fixed Implementation

```python
import csv


def merge_csv_files(file_list):
    all_data = []
    header = None

    for filename in file_list:
        with open(filename, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            file_header = next(reader, None)

            if file_header is None:
                continue

            if header is None:
                header = file_header

            for row in reader:
                all_data.append(row)

    with open("merged.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if header:
            writer.writerow(header)

        writer.writerows(all_data)

    return len(all_data)
```

---

### Why the fixed version is correct

- `import csv` fixes the missing module issue.[web:207]
- `newline=""` avoids extra blank rows while reading and writing CSV files.[web:207][web:249]
- `next(reader, None)` reads the header once per file.
- Only the first file’s header is saved and written once into `merged.csv`.
- Empty files are handled safely using `next(reader, None)`.

---

## Quick Summary

### `json.load()` vs `json.loads()`

- `json.load()` reads from a file object.[web:237][web:244]
- `json.loads()` reads from a string.[web:237][web:238]

### `find_large_files()`

- Uses `pathlib`
- Searches recursively
- Filters by size
- Returns sorted results.[web:211][web:242][web:245]

### CSV Debug Fixes

- Add `import csv`
- Use `newline=""`
- Skip repeated headers properly.[web:207][web:243][web:249]
