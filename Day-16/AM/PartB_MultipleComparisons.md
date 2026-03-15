# Day 16 AM – Part B: Multiple Comparison Problem

## Probability of at least one false positive

For 20 independent A/B tests at α=0.05, probability of ≥1 false positive = 1 - (1-0.05)^20 = 64.0%[web:447][web:452]

## Simulation verification (10,000 runs)
Simulated: 63.8%

## Bonferroni correction
Corrected α = 0.05 / 20 = 0.0025

New family-wise error rate = 1 - (1-0.0025)^20 = 4.9% (close to 5%)
