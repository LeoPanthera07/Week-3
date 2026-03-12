ss## Q1. Handling 40% missing values in a 1M-row `income` column

If a DataFrame has 1 million rows and 40% of the `income` column is missing, I would **not** immediately fill or drop it without first understanding the business meaning of the column and why the values are missing. The decision depends on whether `income` is critical for the task, whether the missingness is random, and how much bias filling or dropping could introduce.[web:380][web:355]

### Step-by-step decision process

#### 1. Measure the problem first

I would first calculate:

- percentage missing
- distribution of non-missing income values
- whether missing income is concentrated in specific user groups
- correlation between missingness and other variables like city, age, plan type, or region

This matters because 40% missing is large enough that careless imputation can distort the dataset.

#### 2. Ask: is `income` important?

- If `income` is **not critical** for the downstream task, I might leave it as missing or drop the column.
- If `income` is a **key feature**, I would try to preserve it through sensible imputation rather than dropping it immediately.

#### 3. When would I drop rows?

I would drop rows only if:

- the analysis absolutely requires `income`
- the rows with missing income are a minority
- dropping them does not create major bias

With 40% missing, dropping all those rows is usually expensive because it throws away 400,000 rows, which may reduce statistical power and skew the sample.

#### 4. When would I drop the column?

I would consider dropping the `income` column if:

- the missingness is extremely high and unfixable
- the feature is not central to the problem
- imputation would be mostly guesswork
- alternative features already capture similar information

At 40%, I would not automatically drop the column, but I would evaluate how useful it remains.

### Fill strategy choice

For `income`, I would usually prefer **median imputation**, not mean, because income is often skewed and affected by large outliers. Median is more robust and gives a more realistic central fill value than mean in many real-world financial datasets.[web:380]

Example:

```python
df["income"] = df["income"].fillna(df["income"].median())
```

### Better strategies than one global fill

If I have useful related columns, I would use **group-wise imputation**, for example median income by:

- city
- occupation
- education level
- age group

Example:

```python
df["income"] = df["income"].fillna(
    df.groupby("city")["income"].transform("median")
)
```

This is often better than a single global median because it preserves local structure in the data.

### Final decision

My default decision would be:

1. Investigate missingness pattern
2. Avoid dropping 40% of rows unless absolutely necessary
3. Fill with median or group-wise median
4. Add a flag column such as `income_was_missing` so the model/analysis knows the value was imputed

Example:

```python
df["income_was_missing"] = df["income"].isna().astype(int)
df["income"] = df["income"].fillna(df["income"].median())
```

That keeps information about the original missingness while preserving row count.

---

## Q2. Coding — `standardize_column(series)`

### Solution

```python
import pandas as pd


def standardize_column(series: pd.Series) -> pd.Series:
    """
    Clean a text Series by:
    - stripping whitespace
    - converting to lowercase
    - replacing multiple spaces with one
    - removing special characters
    """
    cleaned = (
        series.astype("string")
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
        .str.replace(r"[^a-z0-9 ]", "", regex=True)
        .str.strip()
    )
    return cleaned
```

### Test

```python
import pandas as pd

sample = pd.Series([
    "  Hello  World!! ",
    "  NEW YORK  ",
    "san--francisco",
    "   MUMBAI   "
])

print(standardize_column(sample))
```

### Expected output

```python
0     hello world
1         new york
2    sanfrancisco
3           mumbai
dtype: string
```

### Why this works

- `.str.strip()` removes leading and trailing whitespace
- `.str.lower()` standardizes casing
- `.str.replace(r"\s+", " ", regex=True)` collapses repeated spaces
- `.str.replace(r"[^a-z0-9 ]", "", regex=True)` removes special characters

This is a standard and reusable text-cleaning pattern in Pandas string workflows.[web:322][web:380]

---

## Q3. Debug — Fix all 4 bugs

### Original buggy code

```python
import pandas as pd

df = pd.DataFrame({
    "price": ["1,500", "2000", "N/A", "3,200", "abc"],
    "category": ["  Electronics ", "CLOTHING", "electronics", " Books", ""],
    "date": ["15/03/2024", "2024-07-01", "22-Nov-2024", "01/10/2024", None],
})

# Bug 1: Not replacing hidden NaN before to_numeric
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Bug 2: Using Python and instead of &
clean = df[df["price"] > 1000 and df["category"] != ""]

# Bug 3: .str operations on NaN without na handling
electronics = df[df["category"].str.contains("electronics")]

# Bug 4: to_datetime without handling mixed formats
df["date"] = pd.to_datetime(df["date"])
```

---

### Bug 1 — Hidden missing values and commas in numeric data

This line is incomplete:

```python
df["price"] = pd.to_numeric(df["price"], errors="coerce")
```

Problems:

- `"N/A"` should be treated as missing
- `"1,500"` and `"3,200"` contain commas, so they will not parse correctly unless commas are removed first
- `"abc"` should become `NaN`, which `errors="coerce"` handles well[web:368]

### Fix

```python
df["price"] = (
    df["price"]
    .replace(["N/A", "", "null", "None"], pd.NA)
    .astype("string")
    .str.replace(",", "", regex=False)
)

df["price"] = pd.to_numeric(df["price"], errors="coerce")
```

---

### Bug 2 — Using `and` instead of `&`

This is wrong in Pandas:

```python
clean = df[df["price"] > 1000 and df["category"] != ""]
```

For element-wise boolean filtering, Pandas requires `&`, and each condition should be wrapped in parentheses.[web:322]

### Fix

```python
clean = df[(df["price"] > 1000) & (df["category"] != "")]
```

---

### Bug 3 — String operations without `na` handling

This line can fail or behave badly when the column contains missing values:

```python
electronics = df[df["category"].str.contains("electronics")]
```

If `category` has `NaN`, `.str.contains()` can propagate missing values into the boolean mask.

### Fix

Also standardize the text first:

```python
df["category"] = (
    df["category"]
    .astype("string")
    .str.strip()
    .str.lower()
)

electronics = df[df["category"].str.contains("electronics", na=False)]
```

Using `na=False` makes missing values behave like `False`, which is safer for filtering.

---

### Bug 4 — Mixed date formats without safe parsing

This line is risky:

```python
df["date"] = pd.to_datetime(df["date"])
```

The column has mixed date formats and missing values, so parsing should be tolerant. In messy real-world data, `errors="coerce"` is safer because invalid dates become `NaT` instead of crashing.

### Fix

```python
df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
```

This is appropriate here because values like `15/03/2024` and `01/10/2024` are day-first style.

---

## Fully corrected version

```python
import pandas as pd

df = pd.DataFrame({
    "price": ["1,500", "2000", "N/A", "3,200", "abc"],
    "category": ["  Electronics ", "CLOTHING", "electronics", " Books", ""],
    "date": ["15/03/2024", "2024-07-01", "22-Nov-2024", "01/10/2024", None],
})

# Fix 1: Replace hidden NaN markers and remove commas before numeric conversion
df["price"] = (
    df["price"]
    .replace(["N/A", "", "null", "None"], pd.NA)
    .astype("string")
    .str.replace(",", "", regex=False)
)
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Standardize text column
df["category"] = (
    df["category"]
    .astype("string")
    .str.strip()
    .str.lower()
)

# Fix 2: Use & instead of and
clean = df[(df["price"] > 1000) & (df["category"] != "")]

# Fix 3: Handle missing values in str.contains
electronics = df[df["category"].str.contains("electronics", na=False)]

# Fix 4: Safely parse mixed date formats
df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)

print("Clean filtered rows:")
print(clean)

print("\nElectronics rows:")
print(electronics)

print("\nParsed dates:")
print(df["date"])
```

---

## Quick summary

- Use `pd.to_numeric(errors="coerce")` after replacing hidden missing markers and removing commas from numeric strings.[web:368]
- Use `&` with parentheses for Pandas boolean conditions, not Python `and`.[web:322]
- Use `na=False` in `.str.contains()` when missing values may exist.
- Use `pd.to_datetime(..., errors="coerce")` for messy mixed-format dates.
