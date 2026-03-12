import pandas as pd


def print_first_5_minutes(df: pd.DataFrame) -> None:
    print("\n=== FIRST 5 MINUTES CHECKLIST ===")
    print("\n1. Shape")
    print(df.shape)

    print("\n2. Columns")
    print(df.columns.tolist())

    print("\n3. Dtypes")
    print(df.dtypes)

    print("\n4. Head")
    print(df.head())

    print("\n5. Tail")
    print(df.tail())

    print("\n6. Null counts")
    print(df.isnull().sum())

    print("\n7. Duplicate rows")
    print(df.duplicated().sum())

    print("\n8. Numeric summary")
    print(df.describe())

    print("\n9. Memory usage (MB)")
    print(round(df.memory_usage(deep=True).sum() / (1024 * 1024), 4))


def main() -> None:
    products = [
        {"name": "Laptop", "category": "Electronics", "price": 65000, "stock": 15, "rating": 4.5, "num_reviews": 220},
        {"name": "Smartphone", "category": "Electronics", "price": 45000, "stock": 20, "rating": 4.4, "num_reviews": 310},
        {"name": "Headphones", "category": "Electronics", "price": 3000, "stock": 50, "rating": 4.1, "num_reviews": 180},
        {"name": "Keyboard", "category": "Electronics", "price": 1500, "stock": 40, "rating": 4.2, "num_reviews": 130},
        {"name": "Monitor", "category": "Electronics", "price": 12000, "stock": 18, "rating": 4.3, "num_reviews": 95},
        {"name": "Mouse", "category": "Electronics", "price": 800, "stock": 60, "rating": 4.0, "num_reviews": 150},

        {"name": "T-Shirt", "category": "Clothing", "price": 700, "stock": 100, "rating": 3.9, "num_reviews": 140},
        {"name": "Jeans", "category": "Clothing", "price": 2200, "stock": 45, "rating": 4.2, "num_reviews": 110},
        {"name": "Jacket", "category": "Clothing", "price": 3500, "stock": 25, "rating": 4.4, "num_reviews": 85},
        {"name": "Sneakers", "category": "Clothing", "price": 4200, "stock": 30, "rating": 4.1, "num_reviews": 170},
        {"name": "Cap", "category": "Clothing", "price": 500, "stock": 70, "rating": 3.8, "num_reviews": 60},

        {"name": "Clean Code", "category": "Books", "price": 600, "stock": 80, "rating": 4.7, "num_reviews": 250},
        {"name": "Python Crash Course", "category": "Books", "price": 750, "stock": 65, "rating": 4.6, "num_reviews": 210},
        {"name": "Deep Work", "category": "Books", "price": 550, "stock": 50, "rating": 4.5, "num_reviews": 125},
        {"name": "Atomic Habits", "category": "Books", "price": 650, "stock": 75, "rating": 4.8, "num_reviews": 300},
        {"name": "Data Science 101", "category": "Books", "price": 900, "stock": 40, "rating": 4.0, "num_reviews": 90},

        {"name": "Mixer", "category": "Home", "price": 2500, "stock": 20, "rating": 4.1, "num_reviews": 105},
        {"name": "Vacuum Cleaner", "category": "Home", "price": 11000, "stock": 10, "rating": 4.3, "num_reviews": 75},
        {"name": "Table Lamp", "category": "Home", "price": 1200, "stock": 35, "rating": 4.0, "num_reviews": 80},
        {"name": "Bedsheet", "category": "Home", "price": 1800, "stock": 55, "rating": 3.9, "num_reviews": 95},
        {"name": "Cookware Set", "category": "Home", "price": 8500, "stock": 12, "rating": 4.4, "num_reviews": 145},
        {"name": "Wall Clock", "category": "Home", "price": 950, "stock": 28, "rating": 4.2, "num_reviews": 115},
    ]

    df = pd.DataFrame(products)

    print_first_5_minutes(df)

    print("\n=== LOC OPERATIONS ===")
    electronics = df.loc[df["category"] == "Electronics"]
    print("\nAll Electronics:")
    print(electronics)

    high_rating_low_price = df.loc[(df["rating"] > 4.0) & (df["price"] < 5000)]
    print("\nProducts rated > 4.0 and price < 5000:")
    print(high_rating_low_price)

    df.loc[df["name"] == "Laptop", "stock"] = 12
    print("\nUpdated stock for Laptop:")
    print(df.loc[df["name"] == "Laptop"])

    print("\n=== ILOC OPERATIONS ===")
    print("\nFirst 5 products:")
    print(df.iloc[:5])

    print("\nLast 5 products:")
    print(df.iloc[-5:])

    print("\nEvery other row:")
    print(df.iloc[::2])

    print("\nRows 10-15 with columns 0-3:")
    print(df.iloc[10:16, 0:4])

    budget_products = df[df["price"] < 1000].copy()
    premium_products = df[df["price"] > 10000].copy()
    popular_products = df[(df["num_reviews"] > 100) & (df["rating"] > 4.0)].copy()

    filtered_frames = {
        "budget_products.csv": budget_products,
        "premium_products.csv": premium_products,
        "popular_products.csv": popular_products,
    }

    for filename, frame in filtered_frames.items():
        frame.to_csv(filename, index=False)

    print("\n=== FILTERED DATAFRAMES CREATED ===")
    print("budget_products:", len(budget_products))
    print("premium_products:", len(premium_products))
    print("popular_products:", len(popular_products))
    print("\nCSV files exported successfully.")


if __name__ == "__main__":
    main()