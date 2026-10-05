# Rubric: Day 2 - Statistics for imbalanced problems

Score each criterion 0-2. **Pass: 11+ of 14 and no 0 on criteria 1, 2 or 3.** Otherwise: Revise. Arithmetic must be shown; a bare number earns at most 1.

| # | Criterion | 2 = meets | 1 = partial | 0 = missing |
|---|---|---|---|---|
| 1 | Accuracy trap (Q1) | 99.83%, 0 of 492 frauds caught, and explains accuracy mostly measures the majority class | Correct numbers, weak or no explanation | Wrong or missing |
| 2 | Confusion matrix + metrics (Q2-3) | TP/FP/FN/TN identified with business meaning; accuracy 99.15%, precision 0.333, recall 0.70, F1 0.452 | Matrix right, one metric wrong or no working shown | Matrix misread or metrics swapped |
| 3 | Threshold trade-off (Q4) | Precision 0.101, recall 0.90, and ties the choice to missed-fraud vs. false-alarm cost | Numbers right, decision not tied to cost | Wrong numbers and no reasoning |
| 4 | ROC vs. PR (Q5-6) | FPR 1.76%, precision 7.4%, explains why ROC flatters; picks PR-AUC with a reason | One of the numbers or the reasoning missing | Says ROC-AUC is always safe |
| 5 | Distance intuition (Q7-8) | Anomaly = far from the cluster; unscaled large-range feature dominates distance | One of the two correct | Both wrong or missing |
| 6 | PCA (Q9) | Rotated axes ordered by variation; notes V1-V28 suit distance methods but hurt interpretability | Correct but misses the interpretability point | Wrong or missing |
| 7 | Process | Branch `day02-imbalance-stats`, PR template filled, working shown | Minor gaps | PR wrong or nothing submitted |

**Common errors to watch:** swapping precision and recall; computing F1 as the average of precision and recall; using total transactions in the FPR denominator.
