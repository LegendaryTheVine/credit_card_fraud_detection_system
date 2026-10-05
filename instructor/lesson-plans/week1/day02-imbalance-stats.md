# Day 2: Theory: statistics for imbalanced problems

**Week 1** · 90-120 minutes · Calculator or a blank notebook for arithmetic; still no dataset.

## Goal for the session
By the end, the student can: show why accuracy is meaningless at a 0.17% positive rate, read a confusion matrix, compute precision / recall / F1 by hand, explain when ROC-AUC and PR-AUC mislead, and describe distance and PCA well enough that anomaly detection will make sense in Week 2.

## Session outline
| Time | Segment |
|---|---|
| 0-10 | Review Day 1 PR; recap the open question: "is 99.8% accuracy impressive?" |
| 10-30 | Why accuracy breaks under imbalance |
| 30-60 | Confusion matrix, precision, recall, F1, with a worked example |
| 60-80 | ROC-AUC vs. PR-AUC |
| 80-105 | Distance and PCA intuition |
| 105-120 | Assignment handoff |

## 1. Why accuracy breaks (20 min)
Do it live. The dataset has 284,807 transactions and 492 frauds.
- A "model" that always says *not fraud* is right on 284,315 of them: accuracy = 284,315 / 284,807 = **99.83%**.
- It catches **zero** fraud. It is useless and it scores 99.83%.
- Lesson: when one class is rare, accuracy mostly measures the majority class. We need metrics that focus on the rare class.
Ask the student to explain, in their own words, why the Day 1 question "99.8% accurate?" has no good answer without more information.

## 2. Confusion matrix, precision, recall, F1 (30 min)
Draw the 2x2 grid: rows = actual, columns = predicted. TP, FP, FN, TN. Name each in business terms:
- **TP**: fraud, we flagged it (good catch)
- **FN**: fraud, we missed it (money lost)
- **FP**: legit, we flagged it (customer blocked)
- **TN**: legit, we let it through

**Worked example** (use a 20% stratified test set: 56,962 transactions, about 98 frauds):

| | Predicted fraud | Predicted legit |
|---|---|---|
| **Actual fraud** | TP = 80 | FN = 18 |
| **Actual legit** | FP = 20 | TN = 56,844 |

- Accuracy = (80 + 56,844) / 56,962 = **99.93%** (looks great, tells us little)
- Precision = TP / (TP + FP) = 80 / 100 = **0.80** ("when we flag, how often are we right?")
- Recall = TP / (TP + FN) = 80 / 98 = **0.82** ("of real fraud, how much do we catch?")
- F1 = 2TP / (2TP + FP + FN) = 160 / 198 = **0.81** (harmonic mean; punishes imbalance between the two)

Key ideas to land:
- Precision and recall trade off through the **threshold**. Flag more, recall goes up, precision goes down. This is the bridge to Day 7's cost-based tuning.
- Which matters more depends on cost. A missed fraud and a false alarm are not equally expensive.
- F1 treats both errors equally; sometimes the business does not.

Have the student recompute with a different threshold: FP = 200, FN = 8 (so TP = 90). Precision = 0.31, recall = 0.92. Discuss: is that better?

## 3. ROC-AUC vs. PR-AUC (20 min)
- **ROC curve**: true positive rate (recall) vs. false positive rate (FP / all legit) across thresholds. AUC = chance a random fraud scores higher than a random legit transaction.
- **Why ROC lies here**: the false positive rate divides by ~284,000 legit transactions, so even many false alarms look tiny. Example: 1,000 false positives on 56,864 legit = FPR of 1.8%, which looks excellent on a ROC curve, yet with 80 TPs precision = 80 / 1,080 = **7%**. Roughly 13 of 14 alerts are false alarms.
- **PR curve**: precision vs. recall. Ignores true negatives, so it does not get flattered by the huge legit class. Baseline is the positive rate (~0.17%), not 0.5.
- Rule of thumb for this project: report **PR-AUC** as the headline, ROC-AUC as secondary, and always say what the false alarm volume looks like in business terms.
- Do not over-teach. Day 7 does the hands-on version.

## 4. Distance and PCA intuition (25 min)
Goal is intuition only; no linear algebra derivations.
- **Distance**: each transaction is a point in space (one axis per feature). Euclidean distance is "how far apart are two points". Normal transactions cluster together; an anomaly sits far from the crowd. Draw 2D scatter with a dense blob and a few distant dots.
- **Scale matters**: if Amount is in the thousands and another feature is around 1, distance is dominated by Amount. That is why scaling matters on Day 4.
- **PCA**: with 30 features you cannot draw the space. PCA finds new axes that capture the most variation, ordered by importance, and lets you keep the top few. Analogy: photographing a 3D object from the angle that shows the most detail.
- **Why V1-V28**: the dataset's features are already PCA outputs (for privacy), so they are uncorrelated and not individually interpretable. Consequence: great for distance-based anomaly detection, hard to explain to stakeholders (Day 6 returns to this).
- Preview: Isolation Forest (Day 9) works because anomalies are easy to isolate in this space.

## Assignment handoff (10-15 min)
Walk through the questions in the student README, especially the by-hand calculation.

## Common pitfalls
- Mixing up precision and recall. Use the plain-English phrasing: precision = "of my alerts, how many were real"; recall = "of the real fraud, how much I caught".
- Believing ROC-AUC is always safe. Return to the 1,000 FP example.
- Treating PCA as magic. It is a rotation of the axes sorted by how much variation they hold.

## Expected deliverable
`submission.md` with answers and the by-hand calculations (see the student README). Answer key: `instructor/solutions/week1/day02-imbalance-stats/answer-key.md`.

## Review focus
Are the arithmetic steps shown, not just the answers? Do they explain *why* accuracy fails in their own words? Do they connect FP and FN to business cost?
