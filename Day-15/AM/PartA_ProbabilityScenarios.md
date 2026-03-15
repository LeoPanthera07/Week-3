# Day 15 AM – Part A: Probability Scenarios

## 1. Website traffic

Scenario: Website receives 200 requests per minute on average. Find P(more than 220 requests in a minute).

- Distribution: Poisson(λ = 200)
- Reasons:
  - We are counting discrete events (requests) in a fixed interval of time.
  - Requests are approximately independent, and the average rate is given.

Python with `scipy.stats`:

```python
from scipy.stats import poisson

lam = 200
p_more_than_220 = poisson.sf(220, mu=lam)
print("P(X > 220) =", p_more_than_220)
```

---

## 2. Quality control

Scenario: Probability a bolt is defective is 2%. In a batch of 50, find P(exactly 3 defective).

- Distribution: Binomial(n = 50, p = 0.02)
- Reasons:
  - Fixed number of independent trials (50 bolts).
  - Each bolt is either defective or not (Bernoulli outcome) with constant probability.

Python:

```python
from scipy.stats import binom

n = 50
p = 0.02
k = 3
p_exactly_3 = binom.pmf(k, n, p)
print("P(X = 3) =", p_exactly_3)
```

---

## 3. Delivery times

Scenario: Delivery times are Normal(μ = 45 min, σ = 8 min). Find P(delivery > 60 min) and P(40 < delivery < 50).

- Distribution: Normal(μ = 45, σ = 8)
- Reasons:
  - Many small independent factors contribute to delivery time.
  - Problem statement explicitly specifies a Normal distribution.

Python:

```python
from scipy.stats import norm

mu = 45
sigma = 8

p_greater_60 = norm.sf(60, loc=mu, scale=sigma)

p_40_50 = norm.cdf(50, loc=mu, scale=sigma) - norm.cdf(40, loc=mu, scale=sigma)

print("P(X > 60) =", p_greater_60)
print("P(40 < X < 50) =", p_40_50)
```

---

## 4. Customer arrivals

Scenario: Customer arrivals follow a rate of 10 per hour. Find P(no customers in the next 6 minutes).

- Model: Poisson process with rate λ = 10/hour.
- Over 6 minutes, expected arrivals λ′ = 10 * (6/60) = 1.
- Distribution: Poisson(λ′ = 1) and we want P(X = 0).

Python:

```python
from scipy.stats import poisson

lam_per_hour = 10
interval_minutes = 6
lam_interval = lam_per_hour * (interval_minutes / 60)

p_no_customers = poisson.pmf(0, mu=lam_interval)
print("P(no customers in 6 minutes) =", p_no_customers)
```

---

## 5. Class average and CLT

Scenario: Class of 35 students. Using the Central Limit Theorem, approximate the distribution of the class average score.

Let each student’s score be a random variable X with mean μ and variance σ². The class average is:

\( \bar{X} = \frac{1}{35} \sum_{i=1}^{35} X_i \)

By the Central Limit Theorem, for reasonably large n:

- \( \bar{X} \) is approximately Normal.
- Mean of \( \bar{X} \) is μ.
- Variance of \( \bar{X} \) is σ² / 35, so standard deviation is \( \sigma / \sqrt{35} \).

So the class average is approximately:

\[ \bar{X} \sim N\left(\mu, \frac{\sigma^2}{35}\right) \]

If we have empirical estimates `mu_hat` and `sigma_hat` from past classes, we can plug them into a Normal approximation.

Example simulation with `scipy.stats` (using a generic Normal score distribution):

```python
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

mu = 70
sigma = 10
n_students = 35
n_sim = 10000

samples = np.random.normal(loc=mu, scale=sigma, size=(n_sim, n_students))
means = samples.mean(axis=1)

x = np.linspace(means.min(), means.max(), 200)
normal_pdf = norm.pdf(x, loc=mu, scale=sigma / np.sqrt(n_students))

plt.hist(means, bins=30, density=True, alpha=0.6)
plt.plot(x, normal_pdf, "r-")
plt.xlabel("Class average score")
plt.ylabel("Density")
plt.title("CLT approximation for class average (n=35)")
plt.show()
```

Hand-drawn sketches:

- Poisson PMFs for the traffic and arrivals scenarios.
- Binomial PMF for the defectives scenario.
- Normal PDF for the delivery-time scenario.
- Approximate Normal PDF for the class-average distribution.
