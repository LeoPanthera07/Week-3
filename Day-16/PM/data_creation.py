import numpy as np
import pandas as pd

np.random.seed(42)
n = 1200

df = pd.DataFrame({
    "customer_id": np.arange(1, n+1),
    "age": np.random.randint(18, 70, size=n),
    "income": np.random.normal(60000, 15000, size=n).round(0),
    "orders_last_month": np.random.poisson(3, size=n),
    "avg_order_value": np.random.normal(1200, 400, size=n).round(2),
    "total_spent": lambda d: (d["orders_last_month"] * d["avg_order_value"]).round(2),
})

df["city"] = np.random.choice(
    ["Ahmedabad", "Mumbai", "Delhi", "Bangalore", "Hyderabad"],
    size=n
)
df["segment"] = np.random.choice(
    ["Budget", "Standard", "Premium"],
    size=n,
    p=[0.4, 0.4, 0.2]
)
df["is_active"] = np.random.choice([0, 1], size=n, p=[0.3, 0.7])
df["signup_days_ago"] = np.random.randint(1, 365*3, size=n)

# Recompute total_spent after all numeric cols exist
df["total_spent"] = (df["orders_last_month"] * df["avg_order_value"]).round(2)

df.to_csv("eda_assignment_data.csv", index=False)