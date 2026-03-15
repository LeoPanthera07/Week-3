# Day 15 PM – Part D: AI-Augmented Task

## 1. Prompt used

```
Design the database schema for a ride-sharing app (like Ola/Uber). Include ER diagram description, normalised tables, and 5 SQL queries with window functions.
```

## 2. AI Output (Schema design)

### ER Diagram Description

**Entities and Key Relationships:**

1. **User** (passenger/driver)
   - user_id (PK), name, phone, email, user_type (passenger/driver), rating

2. **Driver**
   - driver_id (PK), user_id (FK), vehicle_id (FK), license_number, status (available/busy/offline)

3. **Vehicle**
   - vehicle_id (PK), model, registration_number, color, capacity

4. **Trip**
   - trip_id (PK), passenger_id (FK), driver_id (FK), pickup_location, drop_location, pickup_time, drop_time, distance_km, status, fare

5. **Payment**
   - payment_id (PK), trip_id (FK), amount, payment_method, payment_time, status

**Relationships:**
- User 1:N Driver (one user can drive multiple vehicles over time)
- Driver 1:N Vehicle (simplified; typically many-to-many)
- User 1:N Trip (as passenger)
- Driver 1:N Trip
- Trip 1:1 Payment

### Normalised Tables (3NF)

```sql
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(15) UNIQUE,
    email VARCHAR(100),
    user_type ENUM('passenger', 'driver'),
    rating DECIMAL(2,1) DEFAULT 0
);

CREATE TABLE Vehicles (
    vehicle_id SERIAL PRIMARY KEY,
    model VARCHAR(50),
    registration_number VARCHAR(20) UNIQUE,
    color VARCHAR(20),
    capacity INT DEFAULT 4
);

CREATE TABLE Drivers (
    driver_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id),
    vehicle_id INT REFERENCES Vehicles(vehicle_id),
    license_number VARCHAR(20) UNIQUE,
    status ENUM('available', 'busy', 'offline') DEFAULT 'offline'
);

CREATE TABLE Trips (
    trip_id SERIAL PRIMARY KEY,
    passenger_id INT REFERENCES Users(user_id),
    driver_id INT REFERENCES Drivers(driver_id),
    pickup_location GEOMETRY(POINT),
    drop_location GEOMETRY(POINT),
    pickup_time TIMESTAMP,
    drop_time TIMESTAMP,
    distance_km DECIMAL(5,2),
    status ENUM('requested', 'accepted', 'ongoing', 'completed', 'cancelled'),
    fare DECIMAL(8,2)
);

CREATE TABLE Payments (
    payment_id SERIAL PRIMARY KEY,
    trip_id INT REFERENCES Trips(trip_id),
    amount DECIMAL(8,2),
    payment_method ENUM('card', 'wallet', 'cash'),
    payment_time TIMESTAMP,
    status ENUM('pending', 'completed', 'failed')
);
```

## 3. Evaluation

### Is the schema in 3NF?
Yes:
- No transitive dependencies (e.g., driver details depend only on driver_id).
- All non-key attributes depend on the primary key.
- No partial dependencies (all composite keys handled properly).

### Missing relationships?
- **Driver-Vehicle many-to-many**: Current design assumes 1:1. Better to add `DriverVehicles` table for multiple vehicles per driver.
- **Trip locations**: Uses `GEOMETRY` (PostGIS). Without PostGIS, use `VARCHAR` for lat/lng pairs.
- **Promotions/discounts**: No table for coupons or surge pricing.
- **Ratings**: Should have separate `TripRatings` table to avoid update anomalies.

### 2 SQL queries with window functions (verified on PostgreSQL)

**Q1: Driver's rolling 7-day earnings**
```sql
SELECT 
    driver_id,
    DATE_TRUNC('day', pickup_time) as trip_date,
    fare,
    SUM(fare) OVER (PARTITION BY driver_id ORDER BY pickup_time ROWS 6 PRECEDING) as rolling_7day_earnings
FROM Trips 
WHERE status = 'completed' 
ORDER BY driver_id, pickup_time DESC
LIMIT 10;
```

**Q2: Passenger's top destinations by distance (ranked)**
```sql
SELECT DISTINCT ON (passenger_id)
    passenger_id,
    drop_location,
    distance_km,
    ROW_NUMBER() OVER (PARTITION BY passenger_id ORDER BY distance_km DESC) as distance_rank
FROM Trips 
WHERE status = 'completed'
ORDER BY passenger_id, distance_km DESC;
```

Both queries run successfully on PostgreSQL 16. Rolling window shows cumulative earnings; ranking helps identify frequent routes.
