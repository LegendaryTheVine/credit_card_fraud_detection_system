# Day 2 answer key

**1.** Always predicting "not fraud": 284,315 / 284,807 = **99.83%** accuracy; catches **0 of 492** frauds. Accuracy mostly measures the majority class when one class is rare.

**2.** TP = 35 (fraud caught). FN = 15 (fraud missed, money lost). FP = 70 (real customers flagged). TN = 9,880 (legit passed through).

**3.**
- Accuracy = (35 + 9,880) / 10,000 = **99.15%**
- Precision = 35 / (35 + 70) = 35 / 105 = **0.333**
- Recall = 35 / (35 + 15) = 35 / 50 = **0.70**
- F1 = 2 * 35 / (2 * 35 + 70 + 15) = 70 / 155 = **0.452**

**4.** FN = 5 means TP = 45. FP = 400.
- Precision = 45 / 445 = **0.101**
- Recall = 45 / 50 = **0.90**
Decision depends on costs: average loss per missed fraud vs. cost per false alarm (support call, declined card, lost customer), and review capacity. If a missed fraud costs far more than a false alarm, the lower threshold can win. Accept any answer that ties the choice to cost.

**5.** Legit = 56,864. FPR = 1,000 / 56,864 = **1.76%** (looks tiny, ROC looks great). Precision = 80 / (80 + 1,000) = **7.4%**: about 13 of 14 alerts are false alarms.

**6.** PR-AUC as the headline: it ignores true negatives, so it is not flattered by the huge legit class; report ROC-AUC as secondary context.

**7.** Normal transactions cluster near each other; an anomaly differs on one or more features, so its distance to the bulk of points is large.

**8.** Distance adds up differences across features; a feature with a huge numeric range dominates the total and drowns out the others, so scale features first.

**9.** PCA rotates the axes to new ones ordered by how much variation they capture, so a few components summarize many features. V1-V28 being PCA outputs means they are uncorrelated and suit distance-based anomaly detection, but they are not individually interpretable, which makes explaining results to stakeholders harder.
