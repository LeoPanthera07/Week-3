# Day 15 PM – Part A: ER, Normalisation, and Relational Algebra

## 1. ER diagram for an online food delivery app

### Entities and attributes

1. Customer
   - Customer(customer_id, name, phone, email, street_address, city)

2. Restaurant
   - Restaurant(restaurant_id, name, phone, street_address, city)

3. Dish
   - Dish(dish_id, restaurant_id, name, category, base_price)

4. Order
   - Order(order_id, customer_id, restaurant_id, order_time, status, total_amount)

5. OrderItem
   - OrderItem(order_id, dish_id, quantity, price_at_order)

6. DeliveryPartner
   - DeliveryPartner(delivery_partner_id, name, phone, vehicle_type)

7. Payment
   - Payment(payment_id, order_id, method, amount, status, payment_time)

### Relationships and cardinalities

1. Customer–Order
   - One Customer places many Orders.
   - Relationship: Customer 1 — N Order
   - Foreign key: Order.customer_id → Customer.customer_id

2. Restaurant–Order
   - One Restaurant receives many Orders.
   - Relationship: Restaurant 1 — N Order
   - Foreign key: Order.restaurant_id → Restaurant.restaurant_id

3. Restaurant–Dish
   - One Restaurant offers many Dishes.
   - Relationship: Restaurant 1 — N Dish
   - Foreign key: Dish.restaurant_id → Restaurant.restaurant_id

4. Order–OrderItem–Dish
   - One Order contains many OrderItems; one Dish appears in many OrderItems.
   - Relationship: Order 1 — N OrderItem — 1 Dish (OrderItem is the associative entity)
   - Foreign keys: OrderItem.order_id → Order.order_id, OrderItem.dish_id → Dish.dish_id

5. Order–DeliveryPartner
   - One DeliveryPartner can handle many Orders; each Order is assigned to at most one DeliveryPartner.
   - Relationship: DeliveryPartner 1 — N Order (optional on Order side)
   - Implementation: add optional FK Order.delivery_partner_id → DeliveryPartner.delivery_partner_id (or keep as separate assignment table if needed).

6. Order–Payment
   - Each Order has one Payment record (simplified); a Payment belongs to exactly one Order.
   - Relationship: Order 1 — 1 Payment
   - Foreign key: Payment.order_id → Order.order_id

Use this description as the basis for a hand-drawn ER diagram with entities, attributes, primary keys underlined, and crow’s-foot notation for cardinalities.

---

## 2. Normalising OrderFacts.csv to 3NF (example)

Assume OrderFacts.csv is a single wide table with columns like:

OrderFacts(order_id, order_time, customer_id, customer_name, customer_city,
           restaurant_id, restaurant_name, restaurant_city,
           dish_id, dish_name, dish_category,
           quantity, unit_price, payment_method)

### 2.1. First Normal Form (1NF)

1NF requires:

- Each cell contains a single value.
- No repeating groups or arrays.

We assume OrderFacts already stores one row per order–dish line (order item), so it is in 1NF.

### 2.2. Second Normal Form (2NF)

Take the functional dependencies (FDs) for the wide table with composite key (order_id, dish_id):

- order_id → order_time, customer_id, customer_name, customer_city, restaurant_id, restaurant_name, restaurant_city, payment_method
- customer_id → customer_name, customer_city
- restaurant_id → restaurant_name, restaurant_city
- dish_id → dish_name, dish_category, unit_price
- (order_id, dish_id) → quantity

Non-key attributes depending only on a part of the composite key indicate partial dependency, so we decompose.

Decomposition to 2NF tables:

1. Orders(order_id, order_time, customer_id, restaurant_id, payment_method)
2. Customers(customer_id, customer_name, customer_city)
3. Restaurants(restaurant_id, restaurant_name, restaurant_city)
4. Dishes(dish_id, restaurant_id, dish_name, dish_category, unit_price)
5. OrderItems(order_id, dish_id, quantity)

### 2.3. Third Normal Form (3NF)

Check for transitive dependencies:

- Customers: customer_id → customer_name, customer_city (no transitive dependency beyond key)
- Restaurants: restaurant_id → restaurant_name, restaurant_city
- Dishes: dish_id → dish_name, dish_category, unit_price (restaurant_id is a foreign key, not a determinant for dish_id)
- Orders: order_id → order_time, customer_id, restaurant_id, payment_method
- OrderItems: (order_id, dish_id) → quantity

There are no remaining non-key attributes depending on other non-key attributes in these decomposed tables, so they are in 3NF.

Summary of 3NF schema:

- Customers(customer_id, customer_name, customer_city)
- Restaurants(restaurant_id, restaurant_name, restaurant_city)
- Dishes(dish_id, restaurant_id, dish_name, dish_category, unit_price)
- Orders(order_id, order_time, customer_id, restaurant_id, payment_method)
- OrderItems(order_id, dish_id, quantity)

---

## 3. Relational algebra expressions (5 queries)

Let the base relations be:

- C(customer_id, name, city)
- R(restaurant_id, name, city)
- D(dish_id, restaurant_id, name, category, base_price)
- O(order_id, customer_id, restaurant_id, order_time, status, total_amount)
- OI(order_id, dish_id, quantity, price_at_order)

Use σ (selection), π (projection), ⋈ (join), γ (grouping/aggregation), and − (set difference).

### Q1: All orders placed by customer with id = 123

\(
π_{order_id, order_time, restaurant_id, total_amount}(σ_{customer_id = 123}(O))
\)

### Q2: List all restaurants in Bengaluru

\(
π_{restaurant_id, name}(σ_{city = "Bengaluru"}(R))
\)

### Q3: Find all dishes and their restaurant names for the category = "Pizza"

\(
π_{D.name, R.name}(σ_{D.category = "Pizza"}(D ⋈_{D.restaurant_id = R.restaurant_id} R))
\)

### Q4: Total revenue per restaurant

\(
γ_{restaurant_id; SUM(total_amount) \rightarrow revenue}(O)
\)

If you want restaurant names as well:

\(
γ_{restaurant_id; SUM(total_amount) \rightarrow revenue}(O) ⋈_{restaurant_id}(π_{restaurant_id, name}(R))
\)

### Q5: Customers who have ordered from more than 3 distinct restaurants

First define a grouped relation:

\(
G = γ_{customer_id; COUNT(DISTINCT restaurant_id) \rightarrow k}(O)
\)

Then select and project:

\(
π_{customer_id}(σ_{k > 3}(G))
\)

---

## 4. Mapping Pandas operations to relational algebra

Assume you have DataFrames: `customers`, `restaurants`, `orders`, `order_items` corresponding to C, R, O, OI.

### 4.1. Merge (join)

Pandas code:

```python
orders_with_rest = orders.merge(restaurants, on="restaurant_id", how="inner")
```

Relational algebra:

\(
O ⋈_{O.restaurant_id = R.restaurant_id} R
\)

Here, `merge` with `how="inner"` corresponds to an inner join (⋈) on the equality of keys.

### 4.2. GroupBy + agg (γ)

Pandas code:

```python
revenue_per_restaurant = (
    orders.groupby("restaurant_id", as_index=False)["total_amount"]
          .sum()
          .rename(columns={"total_amount": "revenue"})
)
```

Relational algebra:

\(
γ_{restaurant_id; SUM(total_amount) \rightarrow revenue}(O)
\)

The `groupby` key corresponds to the grouping attributes; the aggregation functions match the γ operator’s aggregated attributes.

### 4.3. Filter (σ)

Pandas code:

```python
bengaluru_restaurants = restaurants[restaurants["city"] == "Bengaluru"]
```

Relational algebra:

\(
σ_{city = "Bengaluru"}(R)
\)

Here, the boolean condition inside the DataFrame indexer plays the role of the selection predicate in σ.
