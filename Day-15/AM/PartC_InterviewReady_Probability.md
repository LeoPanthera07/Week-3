# Day 15 AM – Part C: Interview Ready

## Q1 – Base rate fallacy with a medical test

Suppose a rare disease affects 1 in 10,000 people (prevalence = 0.01%). A medical test for this disease has:

- 99% sensitivity (P(test positive | disease) = 0.99)
- 99% specificity (P(test negative | no disease) = 0.99)

You test a random person from the general population and the result is positive. What is the probability they actually have the disease?

Let:

- D = event that the person has the disease
- ¬D = event that the person does not have the disease
- T+ = event that the test is positive

Using Bayes’ theorem:

\[
P(D \mid T+) = \frac{P(T+ \mid D) P(D)}{P(T+ \mid D) P(D) + P(T+ \mid \neg D) P(\neg D)}
\]

We have:

- P(D) = 0.0001
- P(¬D) = 0.9999
- P(T+ | D) = 0.99
- P(T+ | ¬D) = 1 − specificity = 0.01

Plugging in:

\[
P(D \mid T+) = \frac{0.99 \cdot 0.0001}{0.99 \cdot 0.0001 + 0.01 \cdot 0.9999}
\]

Numerically, the denominator is dominated by false positives from the large healthy population. The posterior probability is around 0.0098, i.e., **less than 1%**, even though the test is 99% accurate.

This is the base rate fallacy: ignoring the very low base rate (prevalence) leads people to overestimate how likely a positive test means “you are sick.” In practice, a second confirmatory test or additional information is needed.

---

## Q2 – `simulate_clt(distribution, params, n_samples, n_simulations)`

High-level design for the function:

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


def simulate_clt(distribution, params, n_samples, n_simulations):
    dist = distribution(**params)

    samples = dist.rvs(size=(n_simulations, n_samples))
    means = samples.mean(axis=1)

    theoretical_mean = dist.mean()
    theoretical_std = dist.std() / (n_samples ** 0.5)

    plt.hist(means, bins=30, density=True, alpha=0.6, label="Sample means")

    x = np.linspace(means.min(), means.max(), 200)
    plt.plot(x, norm.pdf(x, loc=theoretical_mean, scale=theoretical_std),
             "r-", label="Normal approximation")

    plt.xlabel("Sample mean")
    plt.ylabel("Density")
    plt.title(f"CLT Simulation (n={n_samples}, sims={n_simulations})")
    plt.legend()
    plt.show()

    return means
```

This works for any `scipy.stats` distribution that has `.rvs`, `.mean`, and `.std`, such as `scipy.stats.expon`, `poisson`, `beta`, etc. The histogram of sample means should look approximately normal as `n_samples` becomes large, even if the original distribution is skewed.

---

## Q3 – Exponential purchases and misleading mean

If individual customer purchase amounts follow an exponential distribution, most customers make **small** purchases, while a few make very large purchases. The distribution is heavily right-skewed: many observations near 0, with a long tail to the right.

In such a distribution:

- The **mean** is sensitive to rare but very large purchases.
- A small number of “whale” customers can pull the mean up significantly.

If you show investors only the mean purchase amount, they may think “typical” customers spend that much, which is misleading. In reality, the **median** and quantiles (e.g., 25th, 50th, 75th percentiles) will be much lower than the mean.

Better metrics to show instead:

- Median purchase amount and interquartile range.
- Distribution of spend by customer decile (e.g., top 10% vs rest).
- Gini coefficient or Lorenz curve to illustrate concentration of revenue.

These metrics make it clear that revenue is concentrated in a small subset of customers, and that most customers are low spenders. This is crucial for understanding customer segmentation, risk, and the true shape of the revenue distribution.
