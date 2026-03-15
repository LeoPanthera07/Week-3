# Day 15 PM – Part C: Interview Ready

## Q1 – Update anomalies in a denormalised database

A denormalised database stores redundant copies of the same fact in multiple rows or tables. That redundancy creates classic update anomalies: if one copy is changed and another is missed, the database becomes inconsistent.[web:435][web:438]

The main update anomalies are:

1. **Update anomaly**
   - The same fact must be updated in multiple places.
   - Missing even one row leaves conflicting values.[web:435][web:438]

2. **Insertion anomaly**
   - You may be forced to insert unrelated or duplicate data just to add one new fact.
   - For example, adding a new supplier might require creating a fake order row if supplier data is only stored inside an orders table.[web:435]

3. **Deletion anomaly**
   - Deleting one row can accidentally remove other important facts that should have been stored independently.[web:435]

### Concrete e-commerce example

Suppose an e-commerce site keeps this denormalised table:

| order_id | product_id | product_name | current_price | customer_id | customer_name |
|---------|------------|--------------|---------------|-------------|---------------|
| 101 | 1 | Wireless Mouse | 799 | 10 | Amit |
| 102 | 1 | Wireless Mouse | 799 | 11 | Priya |
| 103 | 1 | Wireless Mouse | 799 | 12 | Rohan |

Now the business changes the price of `Wireless Mouse` from 799 to 899. Because the price is repeated in many rows, every row for that product must be updated. If one row still shows 799 while others show 899, the database becomes inconsistent, which is a classic update anomaly.[web:438][web:432]

A normalized design would instead store product price in a `Products` table and refer to it by `product_id`, reducing redundant updates.

---

## Q2 – Schema design for current price and price history in 3NF

We need a schema that:

- Maintains the current product price.
- Records price history with timestamps.
- Stays in 3NF.

### Proposed schema

#### 1. Products

- `product_id` (PK)
- `product_name`
- `category_id` (FK)
- `current_price`

#### 2. Categories

- `category_id` (PK)
- `category_name`

#### 3. ProductPriceHistory

- `price_history_id` (PK)
- `product_id` (FK → Products.product_id)
- `price`
- `effective_from`
- `effective_to`

### Why this is in 3NF

- `Categories` stores category facts separately, so category names are not repeated across many products.
- `Products` stores only current product information and a foreign key to category.
- `ProductPriceHistory` stores time-dependent price changes separately from the product master row.
- Non-key attributes depend on the key, the whole key, and nothing but the key, so the design is compatible with 3NF principles.[web:433][web:439]

### How it works

- `Products.current_price` gives fast access to the current price.
- `ProductPriceHistory` preserves the full audit trail of price changes.
- When a price changes, you:
  1. close the previous history row by setting `effective_to`,
  2. insert a new history row with the new price and `effective_from`,
  3. update `Products.current_price`.

This design separates current state from historical state while remaining easy to query.

---

## Q3 – ACID property at risk in double-booking the last hotel room

Scenario: two users simultaneously try to book the last hotel room.

The ACID property most directly at risk is **Isolation**. Isolation ensures that concurrent transactions do not interfere with each other in a way that creates anomalies such as lost updates or double-booking.[web:427][web:428][web:429]

### What can go wrong

If both transactions read “1 room available” at the same time and both proceed to reserve it, the database may accept both bookings unless concurrency is controlled. That creates an overbooking anomaly, meaning the final state is incorrect.[web:427][web:429]

### How the database prevents double-booking

A database typically prevents this with one or more of the following:

1. **Row-level locking**
   - The booking transaction locks the row representing the room or inventory count.
   - Other transactions trying to update that same row must wait.[web:429]

2. **Transaction isolation levels**
   - Stronger isolation, especially `SERIALIZABLE`, makes concurrent transactions behave as if they ran one after another, preventing this class of anomaly.[web:429][web:428]

3. **Optimistic concurrency control**
   - The transaction checks whether the room version or stock count changed before committing.
   - If it changed, one transaction fails and must retry.[web:427]

### Practical explanation

A safe booking flow is:

- Start transaction.
- Check room availability.
- Lock the room row or inventory row.
- Insert booking.
- Decrement availability.
- Commit.

If another transaction tries the same room simultaneously, it will block, fail, or retry depending on the isolation and locking strategy. This is how the database preserves consistency by enforcing isolation between competing transactions.[web:429][web:440]
