from __future__ import annotations

import re
from typing import Any

import pandas as pd
from scipy.stats import skew


def detect_pattern(value: str) -> str:
    """Return a simple pattern label for a string value."""
    if re.fullmatch(r"[A-Za-z ]+", value):
        return "letters_spaces"
    if re.fullmatch(r"\d+", value):
        return "digits_only"
    if re.fullmatch(r"[A-Za-z0-9 ]+", value):
        return "alphanumeric"
    if re.fullmatch(r"[\w\-.@ ]+", value):
        return "mixed_safe_chars"
    return "special_chars"


def profile_dataframe(df: pd.DataFrame) -> dict[str, Any]:
    """Generate a complete reusable profile for any DataFrame."""
    total_rows, total_cols = df.shape
    memory_mb = round(df.memory_usage(deep=True).sum() / (1024 * 1024), 4)

    profile: dict[str, Any] = {
        "shape": {"rows": total_rows, "cols": total_cols},
        "memory_mb": memory_mb,
        "duplicate_rows": int(df.duplicated().sum()),
        "columns": {},
        "issues": {
            "single_value_columns": [],
            "high_cardinality_strings": [],
            "outlier_columns": {},
        },
        "describe_all": df.describe(include="all").fillna("").to_dict(),
    }

    for col in df.columns:
        series = df[col]
        col_profile: dict[str, Any] = {
            "dtype": str(series.dtype),
            "unique_count": int(series.nunique(dropna=False)),
            "null_count": int(series.isna().sum()),
            "null_percentage": round((series.isna().mean() * 100), 2),
            "top_5_frequent_values": {
                str(k): int(v)
                for k, v in series.value_counts(dropna=False).head(5).to_dict().items()
            },
        }

        if series.nunique(dropna=False) <= 1:
            profile["issues"]["single_value_columns"].append(col)

        if pd.api.types.is_numeric_dtype(series):
            numeric = series.dropna()

            if len(numeric) > 0:
                mean_val = numeric.mean()
                std_val = numeric.std()

                col_profile.update(
                    {
                        "min": float(numeric.min()),
                        "max": float(numeric.max()),
                        "mean": round(float(mean_val), 4),
                        "median": round(float(numeric.median()), 4),
                        "std": round(float(std_val), 4) if pd.notna(std_val) else 0.0,
                        "skewness": round(float(skew(numeric, nan_policy="omit")), 4)
                        if len(numeric) > 2
                        else 0.0,
                    }
                )

                if pd.notna(std_val) and std_val > 0:
                    outlier_mask = (numeric - mean_val).abs() > 3 * std_val
                    outlier_count = int(outlier_mask.sum())
                    if outlier_count > 0:
                        profile["issues"]["outlier_columns"][col] = outlier_count
            else:
                col_profile.update(
                    {
                        "min": None,
                        "max": None,
                        "mean": None,
                        "median": None,
                        "std": None,
                        "skewness": None,
                    }
                )

        else:
            text_series = series.dropna().astype(str)

            if len(text_series) > 0:
                lengths = text_series.str.len()
                pattern_counts = text_series.map(detect_pattern).value_counts().head(5)

                col_profile.update(
                    {
                        "avg_length": round(float(lengths.mean()), 2),
                        "min_length": int(lengths.min()),
                        "max_length": int(lengths.max()),
                        "common_patterns": {
                            str(k): int(v) for k, v in pattern_counts.to_dict().items()
                        },
                    }
                )

                if text_series.nunique(dropna=False) > max(20, total_rows * 0.8):
                    profile["issues"]["high_cardinality_strings"].append(col)
            else:
                col_profile.update(
                    {
                        "avg_length": None,
                        "min_length": None,
                        "max_length": None,
                        "common_patterns": {},
                    }
                )

        profile["columns"][col] = col_profile

    print("=== DATA PROFILE SUMMARY ===")
    print("Shape:", profile["shape"])
    print("Memory (MB):", profile["memory_mb"])
    print("Duplicate rows:", profile["duplicate_rows"])
    print("Single-value columns:", profile["issues"]["single_value_columns"])
    print("High-cardinality strings:", profile["issues"]["high_cardinality_strings"])
    print("Outlier columns:", profile["issues"]["outlier_columns"])

    print("\nColumn summary:")
    for col, details in profile["columns"].items():
        print(
            f"- {col}: dtype={details['dtype']}, "
            f"nulls={details['null_count']} ({details['null_percentage']}%), "
            f"unique={details['unique_count']}"
        )

    return profile


if __name__ == "__main__":
    demo_df = pd.DataFrame(
        {
            "name": ["Amit", "Priya", "Rohan", "Priya", None],
            "age": [22, 23, 24, 23, 500],
            "city": ["Delhi", "Mumbai", "Delhi", "Mumbai", "Delhi"],
            "score": [88.5, 91.0, 85.0, 91.0, None],
            "constant_col": ["X", "X", "X", "X", "X"],
        }
    )

    profile = profile_dataframe(demo_df)
    print("\nProfile keys:", profile.keys())
