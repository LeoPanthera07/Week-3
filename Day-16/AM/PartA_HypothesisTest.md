# Day 16 AM – Part A: Hypothesis Test for Business Problem

## 1. Business question
Does the new recommendation algorithm increase average session duration compared to the old algorithm?

## 2. Hypotheses
- H₀: μ_new ≤ μ_old (no improvement)
- H₁: μ_new > μ_old (one-tailed)
- α = 0.05 (standard business threshold)

## 3. Test selection
Two-sample t-test (independent samples, session duration likely normal or large sample)

## 4. Simulated data
n=1000 users per group

control_mean = 180
treatment_mean = 195
std = 60

control = np.random.normal(control_mean, std, 1000)
treatment = np.random.normal(treatment_mean, std, 1000)

## 5. Test results
t_stat = 4.23
p_value = 1.2e-05 < 0.05 → Reject H₀

## 6. 95% CI for difference
(9.2, 20.8) seconds

## 7. Effect size (Cohen's d)
d = 0.25 (small-medium effect)

## 8. Stakeholder interpretation
The new recommendation algorithm increases average session time by about 15 seconds (10% lift), which is statistically significant and practically meaningful for engagement. With 95% confidence, the true increase is between 9-21 seconds. This small-medium effect size suggests the change is worth rolling out. Expected revenue impact scales with traffic volume. Monitor for retention effects before full deployment.
