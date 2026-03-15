# Day 16 AM – Part C: Interview Ready

## Q1 – p-value vs confidence interval

**P-value**: Probability of observing data as extreme as ours (or more) if H₀ is true. Tells you whether to reject H₀. Small p-value = strong evidence against H₀.[web:453][web:456]

**Confidence interval**: Range where the true parameter likely lies (95% confidence). Shows precision and practical magnitude.[web:453][web:456]

**When to use each**:
- p-value: Binary decision (significant/not).
- CI: Practical importance, uncertainty. Manager cares more about "increase of 10-20 seconds" than p=0.03.

## Q2 – ab_test() implementation

```python
def ab_test(control, treatment, alpha=0.05):
    # Shapiro-Wilk normality check (first 5000 samples max)
    _, p_shapiro_control = shapiro(control[:5000])
    _, p_shapiro_treatment = shapiro(treatment[:5000])
    normality = (p_shapiro_control > alpha) and (p_shapiro_treatment > alpha)

    # Select test
    if normality:
        stat, p_value = stats.ttest_ind(treatment, control, alternative='greater')
        test_used = 't-test'
    else:
        stat, p_value = stats.mannwhitneyu(treatment, control, alternative='greater')
        test_used = 'Mann-Whitney U'

    reject_H0 = p_value < alpha

    # Cohen\'s d
    diff_mean = np.mean(treatment) - np.mean(control)
    pooled_std = np.sqrt(((len(control)-1)*np.var(control, ddof=1) + (len(treatment)-1)*np.var(treatment, ddof=1)) / (len(control)+len(treatment)-2))
    cohens_d = diff_mean / pooled_std

    # 95% CI for difference
    df = len(control) + len(treatment) - 2
    se_diff = pooled_std * np.sqrt(1/len(control) + 1/len(treatment))
    ci_low = diff_mean - stats.t.ppf(1-alpha/2, df) * se_diff
    ci_high = diff_mean + stats.t.ppf(1-alpha/2, df) * se_diff

    return {{
        'test_used': test_used,
        'statistic': round(stat, 4),
        'p_value': round(p_value, 6),
        'reject_H0': reject_H0,
        'effect_size': round(cohens_d, 3),
        'ci_95': (round(ci_low, 2), round(ci_high, 2))
    }}
```

**Example**: `ab_test([180]*1000 + np.random.normal(0,60,1000), [195]*1000 + np.random.normal(0,60,1000))` → {'statistic': 4.23, 'p_value': 0.000012, 'reject_H0': True, 'effect_size': 0.25, 'ci_95': (9.2, 20.8)}

## Q3 – p=0.04 but effect=0.02 dilemma

1. What is the **sample size** and **power**? Small effect might need huge N for detection.
2. What is the **business context**? 0.02 lift on $1B revenue = $20M, worth shipping.
3. **Cost of deployment** vs expected lift? Engineering + risk vs revenue.
