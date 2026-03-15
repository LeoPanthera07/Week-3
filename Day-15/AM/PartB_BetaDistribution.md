# Day 15 AM – Part B: Beta Distribution

## 1. Plotting Beta PDFs with `scipy.stats.beta`

We consider three Beta distributions on the interval [0, 1]:

- Beta(2, 5)
- Beta(5, 5)
- Beta(0.5, 0.5)

Example Python code to plot their PDFs:

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

x = np.linspace(0, 1, 500)

pdf_2_5 = beta.pdf(x, a=2, b=5)
pdf_5_5 = beta.pdf(x, a=5, b=5)
pdf_05_05 = beta.pdf(x, a=0.5, b=0.5)

plt.figure(figsize=(8, 5))
plt.plot(x, pdf_2_5, label="Beta(2,5)")
plt.plot(x, pdf_5_5, label="Beta(5,5)")
plt.plot(x, pdf_05_05, label="Beta(0.5,0.5)")
plt.xlabel("p (coin bias)")
plt.ylabel("Density")
plt.title("Beta Distribution PDFs")
plt.legend()
plt.grid(True, alpha=0.2)
plt.show()
```

Hand-drawn sketch guidance:

- Beta(2,5): Right-skewed, concentrated toward lower p values, peak around p ≈ 0.2.
- Beta(5,5): Symmetric, bell-shaped around p = 0.5, relatively concentrated.
- Beta(0.5,0.5): U-shaped, high near 0 and 1, low in the middle.

---

## 2. Interpreting shapes as priors on a coin’s bias

Think of p as the probability of heads when flipping a coin.

### Beta(2,5)

- Mean: 2 / (2 + 5) = 2/7 ≈ 0.29
- Interpretation: Prior belief that the coin is **biased toward tails** (p < 0.5), with moderate confidence.
- The density is low near 1 and higher near 0.2–0.3, so we believe heads is less likely than tails before seeing data.

### Beta(5,5)

- Mean: 5 / (5 + 5) = 0.5
- Interpretation: Prior belief that the coin is **approximately fair**, with some concentration around 0.5.
- The symmetric bell shape shows we expect p to be near 0.5, but we still allow uncertainty (values like 0.4 or 0.6 are possible).

### Beta(0.5,0.5)

- Mean: 0.5, but very U-shaped.
- Interpretation: Prior belief that the coin is **extreme**, either very close to 0 or very close to 1.
- This prior encodes a strong belief that the coin is heavily biased one way or the other, not fair.

In all cases, the Beta distribution represents our prior belief about p before observing any flips.

---

## 3. Posterior after 7 heads in 10 flips with Beta(1,1) prior

A Beta(a, b) prior updated with binomial data (H heads, T tails) yields a Beta(a + H, b + T) posterior.

Here:

- Prior: Beta(1,1) (uniform prior over [0,1])
- Data: 7 heads in 10 flips → H = 7, T = 3
- Posterior: Beta(1 + 7, 1 + 3) = Beta(8, 4)

Python simulation and plotting example:

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

x = np.linspace(0, 1, 500)

prior = beta.pdf(x, a=1, b=1)
posterior = beta.pdf(x, a=8, b=4)

plt.figure(figsize=(8, 5))
plt.plot(x, prior, label="Prior Beta(1,1)")
plt.plot(x, posterior, label="Posterior Beta(8,4)")
plt.xlabel("p (coin bias)")
plt.ylabel("Density")
plt.title("Prior vs Posterior after 7 heads in 10 flips")
plt.legend()
plt.grid(True, alpha=0.2)
plt.show()
```

Interpretation:

- Prior Beta(1,1) is flat: we had no strong belief about p.
- Posterior Beta(8,4) is centered at 8 / (8 + 4) = 2/3 ≈ 0.67, suggesting a coin biased toward heads.
- The posterior is more peaked than the prior, reflecting increased certainty about p after seeing data.

As more data accumulate, the Beta posterior becomes narrower, and the influence of the prior decreases; the data dominate the belief about the coin’s bias.
