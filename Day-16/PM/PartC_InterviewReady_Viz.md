# Day 16 PM – Part C: Interview Ready

## Q1 – Violin plot vs Box plot

**Use violin plot when**: You want to see the **density/shape** of the distribution across categories, not just summary statistics.

**Additional info violin shows**:
- Full probability density (kernel density estimation) on both sides
- Reveals **bimodal/multimodal** distributions box plots miss
- Shows **concentration** of data points

**Box plot**: 5-number summary (min, Q1, median, Q3, max+outliers). Good for quick comparisons.

## Q2 – plot_numerical_eda(df) function

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

def plot_numerical_eda(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    n_cols = len(numeric_cols)

    fig, axes = plt.subplots(n_cols, 3, figsize=(20, 4*n_cols))
    if n_cols == 1:
        axes = axes.reshape(1, -1)

    for i, col in enumerate(numeric_cols):
        # 1. Histogram + KDE
        sns.histplot(df[col], kde=True, ax=axes[i, 0])
        axes[i, 0].set_title(f'{col} - Distribution')
        axes[i, 0].set_xlabel(col)

        # 2. Box plot
        sns.boxplot(y=df[col], ax=axes[i, 1])
        axes[i, 1].set_title(f'{col} - Box Plot')

        # 3. QQ plot (normality check)
        stats.probplot(df[col], dist="norm", plot=axes[i, 2])
        axes[i, 2].set_title(f'{col} - QQ Plot (Normality)')

    plt.tight_layout()
    plt.savefig('eda_numerics.png', dpi=300, bbox_inches='tight')
    plt.show()

# Test
df = pd.read_csv('eda_assignment_data.csv')
plot_numerical_eda(df)
```

**Features**:
- **OO API**: `plt.subplots()`, `ax.set_title()`
- **Auto-detects** all numeric columns
- **1×3 panels per feature**: histogram, box, QQ plot
- **Saves** `eda_numerics.png`

## Q3 – Chart Critiques

**(a) 3D pie chart with 12 market share segments**
- **Problem**: 3D distorts area perception. 12 slices = unreadable labels.
- **Better**: Horizontal bar chart, sorted descending.

**(b) Line chart for 5 unordered survey categories**
- **Problem**: Implies ordinal trend where none exists.
- **Better**: Bar chart (vertical or horizontal).

**(c) Scatter plot with 500k points, no transparency**
- **Problem**: Overplotting makes dense areas solid black, impossible to interpret.
- **Better**: Hexbin plot, 2D histogram, or sample + jitter.
