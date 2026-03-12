## Exact Prompt Used

> Write a Python function that takes a Pandas DataFrame and generates an automated data quality report including: shape, dtypes, missing values percentage, duplicate rows, unique value counts per column, and basic stats. Return the report as a dict and also print a formatted summary.

---

## AI Output

### AI-Generated Code

```python
import pandas as pd

def data_quality_report(df: pd.DataFrame) -> dict:
    """
    Generate a simple data quality report for a DataFrame.
    """
    report = {
        "shape": df.shape,
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_percentage": ((df.isnull().sum() / len(df)) * 100).to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "unique_values": df.nunique(dropna=False).to_dict(),
        "basic_stats": df.describe(include="all").fillna("").to_dict(),
    }

    print("=== DATA QUALITY REPORT ===")
    print("Shape:", report["shape"])
    print("Duplicate rows:", report["duplicate_rows"])
    print("Missing %:")
    for col, pct in report["missing_percentage"].items():
        print(f"  {col}: {pct:.2f}%")

    return report
```

---

## Test 1 — Clean DataFrame

```python
import pandas as pd

clean_df = pd.DataFrame({
    "name": ["Amit", "Priya", "Rohan"],
    "age":, [w3schools](https://www.w3schools.com/python/python_lists_comprehension.asp)
    "city": ["Gandhinagar", "Ahmedabad", "Surat"]
})

report_clean = data_quality_report(clean_df)
print(report_clean["shape"])
```

### Expected observations

- Shape should be `(3, 3)`
- Missing percentages should all be `0.0`
- Duplicate rows should be `0`
- Unique values should be 3 for each column

---

## Test 2 — Messy DataFrame

```python
messy_df = pd.DataFrame({
    "name": ["Amit", "Amit", None, "Riya"],
    "age": [22, 22, None, 22],
    "city": ["Gandhinagar", "Gandhinagar", None, "Surat"],
    "constant_col": ["X", "X", "X", "X"]
})

report_messy = data_quality_report(messy_df)
print(report_messy["duplicate_rows"])
print(report_messy["missing_percentage"])
```

### Expected observations

- Missing values should be non-zero for `name`, `age`, and `city`
- `constant_col` has only one unique value, so it may be a useless feature
- Duplicate patterns should be visible in unique counts

---

## Critical Evaluation

The AI solution gets the core structure right: it computes shape, dtypes, missing percentages, duplicate rows, unique counts, and descriptive statistics using standard Pandas methods.[web:349][web:350]  
It also returns the report as a dictionary and prints a readable summary, which matches the prompt reasonably well.

However, it has important gaps. The biggest issue is handling **empty DataFrames**: the expression `df.isnull().sum() / len(df)` will divide by zero when `len(df) == 0`, so missing-value percentages are not safe for empty input.  
It also does **not** use `df.memory_usage()`, which is a useful quality and profiling metric and was something we explicitly want to inspect in practical DataFrame review workflows.[web:350][web:355]  
Another missed opportunity is flagging columns with only one unique value, because such columns are often useless features in analysis or modeling.  
All-null columns are partly handled by `describe(include="all")`, but the output can be noisy and harder to use programmatically.

I would improve it by adding explicit handling for empty DataFrames, adding memory usage in MB using `df.memory_usage(deep=True).sum()`, listing single-unique-value columns, and separating numeric vs categorical summaries more clearly.  
I would also make the printed summary shorter and keep the detailed report in the returned dictionary for easier downstream use.[web:350][web:355]

---

## Improved Version

```python
import pandas as pd


def data_quality_report(df: pd.DataFrame) -> dict:
    """
    Generate an automated data quality report for a DataFrame.

    Args:
        df: Input Pandas DataFrame.

    Returns:
        Dictionary containing shape, dtypes, missing values percentage,
        duplicate rows, unique counts, single-value columns, memory usage,
        and basic statistics.
    """
    num_rows = len(df)

    if num_rows == 0:
        missing_percentage = {col: 0.0 for col in df.columns}
    else:
        missing_percentage = ((df.isnull().sum() / num_rows) * 100).round(2).to_dict()

    unique_counts = df.nunique(dropna=False).to_dict()
    single_value_columns = [col for col, count in unique_counts.items() if count <= 1]

    report = {
        "shape": df.shape,
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_percentage": missing_percentage,
        "duplicate_rows": int(df.duplicated().sum()),
        "unique_values": unique_counts,
        "single_value_columns": single_value_columns,
        "memory_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 4),
        "basic_stats": df.describe(include="all").fillna("").to_dict(),
    }

    print("=== DATA QUALITY REPORT ===")
    print("Shape:", report["shape"])
    print("Memory (MB):", report["memory_mb"])
    print("Duplicate rows:", report["duplicate_rows"])
    print("Single-value columns:", report["single_value_columns"])

    print("\nMissing % by column:")
    for col, pct in report["missing_percentage"].items():
        print(f"  {col}: {pct:.2f}%")

    return report
```

---

## Why This Version Is Better

- Handles empty DataFrames safely.
- Uses `df.memory_usage(deep=True)` to measure memory usage more accurately, especially for object columns
- Identifies columns with a single unique value, which can reveal useless features.
- Keeps the printed output concise while returning a detailed dictionary.
