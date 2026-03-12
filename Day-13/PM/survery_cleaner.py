import json
import numpy as np
import pandas as pd


INPUT_FILE = "survey_results.csv"
CLEANED_FILE = "cleaned_survey.csv"
REPORT_FILE = "data_quality_report.json"


def create_messy_survey_data() -> pd.DataFrame:
    rows = []
    names = [
        "Amit", "Priya", "Rohan", "Neha", "Vikram", "Sara", "Kunal", "Meera",
        "Arjun", "Pooja", "Rahul", "Isha"
    ]
    cities = ["Mumbai", "Delhi", "Bengaluru", "Ahmedabad", "Pune", "Chennai"]
    feedbacks = [
        " Great service ", "average experience", " VERY GOOD ", "bad support",
        "", "N/A", None, "  quick delivery  "
    ]
    genders = ["Male", "FEMALE", " female ", "MALE ", "Other", "", None]

    for i in range(1, 55):
        rows.append(
            {
                "respondent_id": i,
                "name": f" {names[i % len(names)]} " if i % 7 == 0 else names[i % len(names)],
                "age": 20 + (i % 35),
                "gender": genders[i % len(genders)],
                "city": cities[i % len(cities)] if i % 6 else f"  {cities[i % len(cities)]}  ",
                "satisfaction_score": (i % 5) + 1,
                "feedback": feedbacks[i % len(feedbacks)],
                "purchase_amount": str(500 + i * 75),
                "survey_date": f"2026-03-{(i % 28) + 1:02d}",
            }
        )

    df = pd.DataFrame(rows)

    # Inject 8+ quality issues
    df.loc[1, "age"] = -5
    df.loc[2, "age"] = 200
    df.loc[3, "age"] = "twenty five"
    df.loc[4, "purchase_amount"] = "1,500"
    df.loc[5, "purchase_amount"] = "abc"
    df.loc[6, "purchase_amount"] = "N/A"
    df.loc[7, "satisfaction_score"] = 0
    df.loc[8, "satisfaction_score"] = 6
    df.loc[9, "gender"] = " FEMALE "
    df.loc[10, "city"] = "  mumbai "
    df.loc[11, "feedback"] = "null"
    df.loc[12, "feedback"] = "   "
    df.loc[13, "name"] = None
    df.loc[14, "survey_date"] = "not_a_date"
    df.loc[15, "survey_date"] = None
    df.loc[16, "gender"] = ""
    df.loc[17, "city"] = "N/A"
    df.loc[18, "age"] = None
    df.loc[19, "purchase_amount"] = None
    df.loc[20, "feedback"] = np.nan

    # Add duplicates
    df = pd.concat([df, df.iloc[[5, 10]]], ignore_index=True)

    return df


def detect_issues(df: pd.DataFrame) -> dict:
    hidden_missing = ["", " ", "N/A", "n/a", "null", "None", "none", "NA"]

    temp = df.replace(hidden_missing, np.nan)

    wrong_types = {}
    invalid_values = {}

    age_numeric = pd.to_numeric(temp["age"], errors="coerce")
    purchase_numeric = pd.to_numeric(
        temp["purchase_amount"].astype(str).str.replace(",", "", regex=False),
        errors="coerce",
    )
    score_numeric = pd.to_numeric(temp["satisfaction_score"], errors="coerce")
    parsed_dates = pd.to_datetime(temp["survey_date"], errors="coerce")

    wrong_types["age"] = int(age_numeric.isna().sum() - temp["age"].isna().sum())
    wrong_types["purchase_amount"] = int(
        purchase_numeric.isna().sum() - temp["purchase_amount"].isna().sum()
    )
    wrong_types["satisfaction_score"] = int(
        score_numeric.isna().sum() - temp["satisfaction_score"].isna().sum()
    )
    wrong_types["survey_date"] = int(parsed_dates.isna().sum() - temp["survey_date"].isna().sum())

    invalid_values["age_out_of_range"] = int(((age_numeric < 18) | (age_numeric > 100)).fillna(False).sum())
    invalid_values["satisfaction_out_of_range"] = int(
        ((score_numeric < 1) | (score_numeric > 5)).fillna(False).sum()
    )
    invalid_values["negative_purchase_amount"] = int((purchase_numeric < 0).fillna(False).sum())
    invalid_values["blank_gender"] = int(temp["gender"].isna().sum())
    invalid_values["blank_city"] = int(temp["city"].isna().sum())

    report = {
        "total_rows": int(len(df)),
        "total_missing": int(temp.isna().sum().sum()),
        "missing_per_column": {k: int(v) for k, v in temp.isna().sum().to_dict().items()},
        "duplicate_count": int(df.duplicated().sum()),
        "wrong_types": wrong_types,
        "invalid_values": invalid_values,
    }
    return report


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    hidden_missing = ["", " ", "N/A", "n/a", "null", "None", "none", "NA"]
    cleaned = cleaned.replace(hidden_missing, np.nan)

    # Standardize text columns first
    text_cols = ["name", "gender", "city", "feedback"]
    for col in text_cols:
        cleaned[col] = cleaned[col].astype("string").str.strip()

    cleaned["name"] = cleaned["name"].str.title()
    cleaned["gender"] = cleaned["gender"].str.lower().replace(
        {"male": "Male", "female": "Female", "other": "Other"}
    )
    cleaned["city"] = cleaned["city"].str.lower().str.replace(r"\s+", " ", regex=True).str.title()
    cleaned["feedback"] = cleaned["feedback"].str.lower().str.replace(r"\s+", " ", regex=True).str.strip()

    # Numeric cleanup
    cleaned["age"] = pd.to_numeric(cleaned["age"], errors="coerce")
    cleaned["purchase_amount"] = pd.to_numeric(
        cleaned["purchase_amount"].astype("string").str.replace(",", "", regex=False),
        errors="coerce",
    )
    cleaned["satisfaction_score"] = pd.to_numeric(cleaned["satisfaction_score"], errors="coerce")

    # Date cleanup
    cleaned["survey_date"] = pd.to_datetime(cleaned["survey_date"], errors="coerce")

    # Invalidate impossible values
    cleaned.loc[(cleaned["age"] < 18) | (cleaned["age"] > 100), "age"] = np.nan
    cleaned.loc[
        (cleaned["satisfaction_score"] < 1) | (cleaned["satisfaction_score"] > 5),
        "satisfaction_score",
    ] = np.nan
    cleaned.loc[cleaned["purchase_amount"] < 0, "purchase_amount"] = np.nan

    # Fill strategies:
    # age -> median because age can have outliers and median is robust
    cleaned["age"] = cleaned["age"].fillna(cleaned["age"].median())

    # gender -> mode because it is categorical and we want the most common valid label
    gender_mode = cleaned["gender"].mode(dropna=True)
    cleaned["gender"] = cleaned["gender"].fillna(gender_mode.iloc[0] if not gender_mode.empty else "Unknown")

    # city -> mode because it is categorical and frequent city is a simple fallback
    city_mode = cleaned["city"].mode(dropna=True)
    cleaned["city"] = cleaned["city"].fillna(city_mode.iloc[0] if not city_mode.empty else "Unknown")

    # satisfaction_score -> median because score is ordinal and median is safer than mean
    cleaned["satisfaction_score"] = cleaned["satisfaction_score"].fillna(
        cleaned["satisfaction_score"].median()
    )

    # purchase_amount -> median because amounts can be skewed by large purchases
    cleaned["purchase_amount"] = cleaned["purchase_amount"].fillna(cleaned["purchase_amount"].median())

    # feedback -> fill with placeholder because free text is hard to infer correctly
    cleaned["feedback"] = cleaned["feedback"].fillna("no feedback")

    # name -> cannot safely infer identity, so rows missing respondent name are dropped
    # survey_date -> critical for timeline analysis, rows missing invalid dates are dropped
    cleaned = cleaned.dropna(subset=["name", "survey_date"])

    cleaned["respondent_id"] = cleaned["respondent_id"].astype(int)
    cleaned["age"] = cleaned["age"].round().astype(int)
    cleaned["satisfaction_score"] = cleaned["satisfaction_score"].round().astype(int)

    cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    return cleaned


def comparison_stats(before: pd.DataFrame, after: pd.DataFrame) -> pd.DataFrame:
    before_memory = round(before.memory_usage(deep=True).sum() / (1024 * 1024), 4)
    after_memory = round(after.memory_usage(deep=True).sum() / (1024 * 1024), 4)

    return pd.DataFrame(
        {
            "before": {
                "rows": int(len(before)),
                "nulls": int(before.isna().sum().sum()),
                "memory_mb": before_memory,
                "dtypes": before.dtypes.astype(str).to_dict(),
            },
            "after": {
                "rows": int(len(after)),
                "nulls": int(after.isna().sum().sum()),
                "memory_mb": after_memory,
                "dtypes": after.dtypes.astype(str).to_dict(),
            },
        }
    )


def export_outputs(cleaned: pd.DataFrame, report: dict) -> None:
    cleaned.to_csv(CLEANED_FILE, index=False)

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)


def main() -> None:
    messy_df = create_messy_survey_data()
    messy_df.to_csv(INPUT_FILE, index=False)

    df = pd.read_csv(INPUT_FILE)

    before_report = detect_issues(df)
    cleaned_df = clean_data(df)
    after_report = detect_issues(cleaned_df)

    full_report = {
        "before_cleaning": before_report,
        "after_cleaning": after_report,
    }

    stats = comparison_stats(df, cleaned_df)

    print("=== BEFORE CLEANING REPORT ===")
    print(json.dumps(before_report, indent=2))

    print("\n=== AFTER CLEANING REPORT ===")
    print(json.dumps(after_report, indent=2))

    print("\n=== BEFORE / AFTER STATS ===")
    print(stats)

    export_outputs(cleaned_df, full_report)
    print(f"\nCreated: {INPUT_FILE}, {CLEANED_FILE}, {REPORT_FILE}")


if __name__ == "__main__":
    main()
