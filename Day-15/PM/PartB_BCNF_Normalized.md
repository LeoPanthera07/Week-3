# Day 15 PM – Part B: BCNF and When 3NF Is Enough

## 1. Example of a 3NF schema that is not in BCNF

Consider a relation R(A, B, C) with the following functional dependencies:

- A, B → C  
- C → B  

From these dependencies:

- Candidate keys are (A, B) and (A, C).  
- All attributes (A, B, C) are prime attributes (each appears in some candidate key).

### 1.1. Why R is in 3NF

A relation is in Third Normal Form (3NF) if for every non-trivial functional dependency X → Y, either:

1. X is a superkey, or  
2. Each attribute in Y is a prime attribute (part of some candidate key).

Check the dependencies:

- A, B → C: the left side (A, B) is a superkey, so this satisfies 3NF.  
- C → B: B is a prime attribute (it appears in candidate keys), so this also satisfies 3NF.

Therefore, R(A, B, C) is in 3NF.

### 1.2. Why R is not in BCNF

A relation is in Boyce–Codd Normal Form (BCNF) if for every non-trivial functional dependency X → Y, X is a superkey.

- In dependency C → B, C is not a superkey (keys are (A, B) and (A, C)), so this violates BCNF.

Thus, R(A, B, C) is a classic example of a relation that is in 3NF but not in BCNF.

---

## 2. Decomposing R into BCNF

We decompose R(A, B, C) using the violating dependency C → B.

1. Create R1(C, B) with key C and dependency C → B.  
2. Create R2(A, C) to hold the remaining attributes and preserve candidate keys involving A and C.

Resulting BCNF schema:

- R1(C, B) with C as primary key  
- R2(A, C) with (A, C) as primary key  

In both relations, every determinant is a key, so they satisfy BCNF.

Note: This decomposition is lossless, but the original dependency A, B → C is no longer enforced in a single table; it can be derived via joins. Reasoning about or enforcing all original FDs may require additional constraints.

---

## 3. When is 3NF acceptable instead of BCNF?

BCNF removes more anomalies than 3NF, but many practical OLTP schemas intentionally stop at 3NF because:

1. **Dependency preservation**  
   Decomposing to BCNF can make it impossible to enforce all functional dependencies in one table. You may need joins, triggers, or application logic to preserve some constraints, increasing complexity.

2. **Performance trade-offs**  
   BCNF decomposition often creates more tables and forces extra joins in common queries. For high-traffic systems, extra joins can hurt latency more than the rare update anomalies BCNF would eliminate.

3. **Low risk of anomalies**  
   If the violating dependency changes rarely (for example, a lookup table that is almost static), the practical risk of inconsistent updates is small, so the benefit of full BCNF is limited.

4. **Read-heavy analytics and denormalisation**  
   In reporting or warehouse layers, partial denormalisation is sometimes preferred. A well-designed 3NF core schema plus a few denormalised or materialised views usually balances integrity and performance well.

In summary, BCNF is the theoretical ideal and a good target for critical transactional tables. It is still acceptable to leave a schema in 3NF when:

- BCNF decomposition would make frequent queries significantly more complex or slower,  
- The remaining anomalies are rare and well-understood, and  
- You explicitly trade a small amount of redundancy for simpler queries or better performance.