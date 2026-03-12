## Exact Prompt Used

> Write a Python function that takes a messy Pandas DataFrame and automatically cleans it: detect and replace hidden missing values ('N/A', '', 'null', 'None'), convert object columns to appropriate types (numeric or datetime), standardize text columns (strip, lower), and remove duplicate rows. Return the cleaned DataFrame and a summary of all changes made.

---

## AI Output

### AI-Generated Code

```python
import pandas as pd


def auto_clean_dataframe(df: pd.DataFrame):
    cleaned = df.copy()
    summary = {
        "hidden_missing_replaced": {},
        "converted_columns": [],
        "duplicates_removed": 0,
    }

    hidden_missing = ["N/A", "", "null", "None"]

    for col in cleaned.columns:
        before_missing = cleaned[col].isna().sum()
        cleaned[col] = cleaned[col].replace(hidden_missing, pd.NA)
        after_missing = cleaned[col].isna().sum()
        summary["hidden_missing_replaced"][col] = int(after_missing - before_missing)

    for col in cleaned.columns:
        if cleaned[col].dtype == "object":
            cleaned[col] = cleaned[col].astype("string").str.strip().str.lower()

            numeric_version = pd.to_numeric(cleaned[col], errors="coerce")
            if numeric_version.notna().sum() > 0:
                cleaned[col] = numeric_version
                summary["converted_columns"].append(f"{col} -> numeric")
                continue

            datetime_version = pd.to_datetime(cleaned[col], errors="coerce")
            if datetime_version.notna().sum() > 0:
                cleaned[col] = datetime_version
                summary["converted_columns"].append(f"{col} -> datetime")

    before_dupes = cleaned.duplicated().sum()
    cleaned = cleaned.drop_duplicates()
    after_dupes = cleaned.duplicated().sum()
    summary["duplicates_removed"] = int(before_dupes - after_dupes)

    return cleaned, summary
```

---

## Test 1 — Messy Survey Data

### Test code

```python
import pandas as pd

survey_df = pd.read_csv("survey_results.csv")
cleaned_survey, survey_summary = auto_clean_dataframe(survey_df)

print(cleaned_survey.head())
print(survey_summary)
```

### What I would check

- Did it replace hidden markers like `N/A`, empty strings, and `None` with actual missing values
- Did it remove duplicate rows
- Did it convert numeric-looking columns correctly
- Did it damage any free-text columns by converting them incorrectly

---

## Test 2 — `messy_data.csv` from class

### Test code

```python
messy_df = pd.read_csv("messy_data.csv")
cleaned_messy, messy_summary = auto_clean_dataframe(messy_df)

print(cleaned_messy.head())
print(messy_summary)
```

### What I would check

- Whether mixed date columns were parsed safely
- Whether all-text columns stayed text
- Whether numeric columns with commas, symbols, or mixed values were handled properly
- Whether the summary clearly explains what changed

---

## Critical Evaluation

The AI solution gets the overall pipeline mostly right: it copies the DataFrame, replaces hidden missing markers, attempts type conversion, standardizes text, and removes duplicate rows, which are all core steps in real data cleaning workflows.[web:389][web:390]  
It also returns both the cleaned DataFrame and a summary of changes, which is useful for auditability and matches the assignment prompt well.

However, the logic is too aggressive and may convert columns incorrectly. For example, it tries numeric conversion on every object column and accepts the conversion if **any** values succeed, which can corrupt mixed text columns by turning many entries into `NaN`.  
Similarly, date conversion is attempted broadly without checking whether the column is truly date-like, and mixed date formats may still need more careful handling than a single generic parse.  
It also does not choose fill strategies per column, so it is more of a standardizer than a full cleaner. That matters because replacing missing values is different from deciding how to impute them responsibly.

It does not explicitly handle all-NaN columns, does not report memory usage, and does not explain performance tradeoffs for large datasets. On a 1M-row dataset, repeated per-column conversions can become expensive, especially for wide object-heavy tables.  
I would improve it by adding threshold-based type inference, safer date detection, per-column fill strategy rules, memory reporting with `memory_usage(deep=True)`, and a more detailed change log including rows dropped and columns left unchanged.[web:355][web:350]

---

## Improved Version

```python
import pandas as pd


def auto_clean_dataframe(df: pd.DataFrame):
    cleaned = df.copy()
    summary = {
        "hidden_missing_replaced": {},
        "converted_columns": [],
        "text_standardized": [],
        "duplicates_removed": 0,
        "rows_before": int(len(df)),
        "rows_after": None,
        "memory_mb_before": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 4),
        "memory_mb_after": None,
        "notes": [],
    }

    hidden_missing = ["N/A", "", "null", "None", "none", "NA"]

    for col in cleaned.columns:
        before_missing = int(cleaned[col].isna().sum())
        cleaned[col] = cleaned[col].replace(hidden_missing, pd.NA)
        after_missing = int(cleaned[col].isna().sum())
        summary["hidden_missing_replaced"][col] = after_missing - before_missing

    for col in cleaned.columns:
        if pd.api.types.is_object_dtype(cleaned[col]) or pd.api.types.is_string_dtype(cleaned[col]):
            text_col = cleaned[col].astype("string").str.strip().str.lower()
            cleaned[col] = text_col
            summary["text_standardized"].append(col)

            non_null = text_col.dropna()

            if len(non_null) == 0:
                summary["notes"].append(f"{col}: all values missing after replacement")
                continue

            numeric_try = pd.to_numeric(non_null.str.replace(",", "", regex=False), errors="coerce")
            numeric_ratio = numeric_try.notna().mean()

            if numeric_ratio >= 0.8:
                cleaned[col] = pd.to_numeric(
                    cleaned[col].astype("string").str.replace(",", "", regex=False),
                    errors="coerce",
                )
                summary["converted_columns"].append(f"{col} -> numeric")
                continue

            date_try = pd.to_datetime(non_null, errors="coerce")
            date_ratio = date_try.notna().mean()

            if date_ratio >= 0.8:
                cleaned[col] = pd.to_datetime(cleaned[col], errors="coerce")
                summary["converted_columns"].append(f"{col} -> datetime")

    before_dupes = int(cleaned.duplicated().sum())
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    summary["duplicates_removed"] = before_dupes
    summary["rows_after"] = int(len(cleaned))
    summary["memory_mb_after"] = round(cleaned.memory_usage(deep=True).sum() / (1024 * 1024), 4)

    return cleaned, summary
```

---

## Why This Version Is Better

- Avoids converting a column to numeric or datetime just because a few values happen to parse.
- Uses a conversion threshold to reduce accidental type corruption.
- Handles all-NaN columns more explicitly.
- Reports memory before and after cleaning using `memory_usage(deep=True)`, which is useful for profiling large datasets.[web:355]
- Produces a richer summary for debugging and review.
