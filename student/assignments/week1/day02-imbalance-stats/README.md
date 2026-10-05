# Day 2: Theory: statistics for imbalanced problems

**Week 1** · Branch name to use: `day02-imbalance-stats`

## Objective
Understand why accuracy is the wrong metric for fraud, compute precision / recall / F1 by hand, know when ROC-AUC misleads, and build distance/PCA intuition for Week 2.

## Reading / prep
Your notes from today's session. Calculator or paper is fine. No dataset needed.

## Questions (answer in `submission.md`)
Show your arithmetic for every calculation.

**Part A: Accuracy**
1. The dataset has 284,807 transactions and 492 frauds. A model predicts "not fraud" every time. What is its accuracy? How much fraud does it catch? What does this tell you about accuracy?

**Part B: Confusion matrix by hand**

A model is tested on 10,000 transactions, of which 50 are fraud. It produces:

| | Predicted fraud | Predicted legit |
|---|---|---|
| **Actual fraud** | 35 | 15 |
| **Actual legit** | 70 | 9,880 |

2. Name TP, FP, FN, TN from the table, and say what each means for the bank in plain words.
3. Compute accuracy, precision, recall and F1.
4. The bank lowers the threshold. Now FN = 5 and FP = 400. Recompute precision and recall. Which version would you pick, and what would you need to know about costs to decide?

**Part C: ROC vs. PR**
5. A model on 56,864 legitimate transactions makes 1,000 false positives and catches 80 of 98 frauds. Compute the false positive rate and the precision. Why would the ROC curve look good while the model is, in practice, annoying?
6. In one or two sentences: which of ROC-AUC and PR-AUC would you report on this dataset, and why?

**Part D: Distance and PCA (a few sentences each)**
7. Why is an anomaly "far away" from normal transactions, in distance terms?
8. Why would a feature measured in the thousands (like Amount) cause trouble for distance-based methods if left unscaled?
9. In your own words, what does PCA do? Why does it matter that V1-V28 are already PCA outputs?

## Done when
- [ ] Work is committed on branch `day02-imbalance-stats`
- [ ] `submission.md` answers all questions, with arithmetic shown
- [ ] PR opened using the pull request template

## Notes
_Write questions or blockers for your instructor here._
