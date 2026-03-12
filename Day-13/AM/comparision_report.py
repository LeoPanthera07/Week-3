import pandas as pd


def monthly_metrics(df: pd.DataFrame) -> dict:
    df = df.copy()
    df["revenue"] = df["qty"] * df["price"]

    total_revenue = df["revenue"].sum()
    average_order_value = df["revenue"].mean()

    product_sales = df.groupby("product")["qty"].sum()
    top_selling_product = product_sales.idxmax()

    return {
        "total_revenue": round(total_revenue, 2),
        "average_order_value": round(average_order_value, 2),
        "top_selling_product": top_selling_product,
    }


def main() -> None:
    january = pd.DataFrame([
        {"order_id": 1, "product": "Laptop", "qty": 2, "price": 65000},
        {"order_id": 2, "product": "Mouse", "qty": 5, "price": 600},
        {"order_id": 3, "product": "Keyboard", "qty": 3, "price": 1400},
        {"order_id": 4, "product": "Monitor", "qty": 1, "price": 22000},
        {"order_id": 5, "product": "Headphones", "qty": 4, "price": 3000},
    ])

    february = pd.DataFrame([
        {"order_id": 1, "product": "Laptop", "qty": 1, "price": 65000},
        {"order_id": 2, "product": "Mouse", "qty": 8, "price": 600},
        {"order_id": 3, "product": "Keyboard", "qty": 6, "price": 1400},
        {"order_id": 4, "product": "Monitor", "qty": 2, "price": 22000},
        {"order_id": 5, "product": "Webcam", "qty": 3, "price": 2500},
    ])

    march = pd.DataFrame([
        {"order_id": 1, "product": "Laptop", "qty": 3, "price": 65000},
        {"order_id": 2, "product": "Mouse", "qty": 10, "price": 600},
        {"order_id": 3, "product": "Keyboard", "qty": 4, "price": 1400},
        {"order_id": 4, "product": "Monitor", "qty": 1, "price": 22000},
        {"order_id": 5, "product": "Headphones", "qty": 5, "price": 3000},
    ])

    months = {
        "January": january,
        "February": february,
        "March": march,
    }

    summary = {}

    for month_name, df in months.items():
        metrics = monthly_metrics(df)
        summary[month_name] = metrics

    summary_df = pd.DataFrame(summary).T
    print("=== SUMMARY COMPARISON DATAFRAME ===")
    print(summary_df)

    print("\n=== QUERY EXAMPLES ===")
    jan_high_value = january.query("price > 5000")
    print("\nJanuary products with price > 5000:")
    print(jan_high_value)

    feb_bulk_orders = february.query("qty >= 3")
    print("\nFebruary orders with qty >= 3:")
    print(feb_bulk_orders)

    march_mid_range = march.query("1000 <= price <= 30000")
    print("\nMarch products with 1000 <= price <= 30000:")
    print(march_mid_range)

    print("\n=== OUTLIERS USING NLARGEST / NSMALLEST ===")
    january["revenue"] = january["qty"] * january["price"]
    february["revenue"] = february["qty"] * february["price"]
    march["revenue"] = march["qty"] * march["price"]

    print("\nTop 2 January revenue rows:")
    print(january.nlargest(2, "revenue"))

    print("\nBottom 2 February revenue rows:")
    print(february.nsmallest(2, "revenue"))

    print("\nTop 2 March quantity rows:")
    print(march.nlargest(2, "qty"))

    print("\nBottom 2 March quantity rows:")
    print(march.nsmallest(2, "qty"))

    combined = pd.concat([january, february, march], keys=months.keys(), names=["month"])
    print("\n=== COMBINED DATAFRAME USING PD.CONCAT ===")
    print(combined)


if __name__ == "__main__":
    main()