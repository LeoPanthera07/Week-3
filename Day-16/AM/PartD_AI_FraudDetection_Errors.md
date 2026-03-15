# Day 16 AM – Part D: AI-Augmented Task

## 1. Prompt used
"Explain Type I and Type II errors in the context of a fraud detection system. What are the real-world consequences of each, and how do you balance them?"

## 2. AI Output

**Type I Error (False Positive)**: System flags a legitimate transaction as fraudulent.

- **Consequence**: Customer inconvenience (blocked payment, need verification), increased support tickets, customer churn risk.

**Type II Error (False Negative)**: System misses a real fraudulent transaction.

- **Consequence**: Financial loss to business, stolen customer data, regulatory fines, reputational damage.

**Balance**: Precision-recall tradeoff.

- High precision (low Type I): Fewer false alarms but may miss fraud (high Type II).
- High recall (low Type II): Catches more fraud but annoys more customers (high Type I).

**Tradeoff mechanisms**:
- Adjust decision threshold on fraud probability score.
- Cost-sensitive learning (penalize Type II more heavily).
- Human-in-loop for high-value cases.
- A/B test thresholds on historical data.

## 3. Evaluation

**Yes**, the AI correctly explains the precision-recall tradeoff as the Type I/II error tradeoff:

- Precision = 1 / (1 + Type I rate) → low precision = many false positives.
- Recall = 1 - Type II rate → low recall = many missed frauds.

The explanation is accurate, business-focused, and includes practical balancing strategies.
