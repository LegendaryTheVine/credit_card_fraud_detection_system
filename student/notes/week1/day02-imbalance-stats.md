# Day 2 notes: Statistics for imbalanced problems

Assignment: `assignments/week1/day02-imbalance-stats/` · Branch: `day02-imbalance-stats` · Calculator and paper. No dataset.

## Learning objectives
By the end of this lesson you should be able to:
- Show with numbers why accuracy is meaningless when fraud is 0.17% of transactions
- Read a confusion matrix and name each cell in business terms
- Compute accuracy, precision, recall, F1 and false positive rate by hand
- Explain the precision/recall trade-off and the role of the threshold
- Explain why ROC-AUC flatters an imbalanced problem and why PR-AUC is the better headline
- Describe distance, scaling and PCA in plain words

# Part 1: Lesson

## Why this day matters
When fraud is 0.17% of transactions, the usual way of scoring a model breaks. If you do not understand why, you will pick the wrong model and the wrong threshold and not notice. Today's arithmetic is the foundation for Days 5, 7 and 10.

## The concepts

### The confusion matrix
Every prediction lands in one of four boxes. Rows are what really happened; columns are what the model said.

| | Predicted fraud | Predicted legit |
|---|---|---|
| **Actual fraud** | TP (true positive) | FN (false negative) |
| **Actual legit** | FP (false positive) | TN (true negative) |

Learn them in business terms:
- **TP:** fraud, and we flagged it. A good catch.
- **FN:** fraud, and we let it through. Money lost.
- **FP:** a real customer, and we flagged them. A blocked card and an annoyed customer.
- **TN:** a real customer, and we let them through. Business as usual.

Memory trick: the second word (positive/negative) is what the model *said*. The first word (true/false) is whether it was *right*.

### The formulas
| Metric | Formula | Plain English |
|---|---|---|
| Accuracy | (TP + TN) / total | Share of all predictions that were right |
| Precision | TP / (TP + FP) | Of my alerts, how many were real fraud? |
| Recall | TP / (TP + FN) | Of the real fraud, how much did I catch? |
| F1 | 2·TP / (2·TP + FP + FN) | One number that is high only if precision and recall are both high |
| False positive rate (FPR) | FP / (FP + TN) | Of all real customers, what share did I bother? |

Notice: precision and recall never use TN. FPR and accuracy do. That difference is the key to the whole day.

### A worked example (different numbers from your assignment)
A model is tested on 20,000 transactions, 40 of them fraud.

| | Predicted fraud | Predicted legit |
|---|---|---|
| **Actual fraud** | 30 | 10 |
| **Actual legit** | 90 | 19,870 |

- Check the table adds up: 30 + 10 + 90 + 19,870 = 20,000. Fraud row: 30 + 10 = 40. Good.
- Accuracy = (30 + 19,870) / 20,000 = 19,900 / 20,000 = **99.5%**
- Precision = 30 / (30 + 90) = 30 / 120 = **0.25** (only 1 in 4 alerts is real fraud)
- Recall = 30 / (30 + 10) = 30 / 40 = **0.75** (we catch 3 in 4 frauds)
- F1 = 60 / (60 + 90 + 10) = 60 / 160 = **0.375**
- FPR = 90 / (90 + 19,870) = 90 / 19,960 = **0.0045**, i.e. 0.45%

The story: accuracy says 99.5% and FPR says "only 0.45% of customers bothered", which both sound great. Precision says three out of four alerts are false alarms, which an analyst team would feel every day.

### Precision and recall trade off through the threshold
A model gives each transaction a score. The **threshold** decides which scores become alerts.
- Lower the threshold: more alerts, so you catch more fraud (recall up) but more alerts are false (precision down).
- Raise it: fewer, more confident alerts (precision up), more fraud slips through (recall down).
There is no "correct" threshold in the abstract. It depends on what a miss costs vs. what a false alarm costs. Day 7 turns this into a calculation.

### ROC vs. PR curves
- A **ROC curve** plots recall against FPR for every threshold. Because FPR divides by the huge number of legitimate transactions, even a lot of false alarms gives a tiny FPR. So ROC curves look flattering on imbalanced data.
- A **PR curve** plots precision against recall. It ignores TN, so it is not flattered by the huge legit class. A random model's PR-AUC is about the fraud rate (~0.0017), not 0.5. That makes it an honest headline metric here.

### Distance and scaling
- Treat each transaction as a point in space, with one axis per feature. **Distance** between points measures how different two transactions are.
- Normal transactions crowd together; anomalies sit far away. This is the idea behind the unsupervised models in Week 2.
- If one feature is measured in thousands and the others in single digits, the big one dominates every distance calculation. Picture measuring "how different are two people" with height in millimetres and age in decades.

### PCA in one paragraph
With 30 features you cannot draw the space. **PCA** rotates the axes so the first new axis captures the most variation, the second the next most, and so on. The new axes are uncorrelated with each other. Think of choosing the camera angle that shows the most detail of a 3D object. In this dataset the bank already applied PCA to hide the original features (for privacy), and V1-V28 are the result.

## Summary
- With a rare positive class, accuracy mostly measures the majority class. Use precision, recall, F1 and PR-AUC.
- Precision = "of my alerts, how many were real"; recall = "of the real fraud, how much I caught".
- The threshold trades precision for recall. The right trade depends on business cost, not on maths.
- FPR divides by all legitimate transactions, so it stays tiny even with many false alarms; that is why ROC curves look flattering.
- Distance-based methods need features on comparable scales. V1-V28 are already PCA outputs: uncorrelated, but not interpretable.

## Check your understanding
Try these from memory before you start the assignment. If you cannot answer one, re-read that section.
1. Which two cells of the confusion matrix does precision use? Which does recall use?
2. A model flags 200 transactions; 50 are fraud; there were 100 frauds in total. What are precision and recall?
3. If you lower the threshold, what usually happens to precision, to recall, and to the number of alerts?
4. What is the PR-AUC of a model that guesses at random on this dataset, roughly?
5. Why would an unscaled Amount column dominate a distance calculation?

# Part 2: How to attempt each task

**Show your arithmetic for every calculation.** Write the formula, then the numbers substituted in, then the result. A correct number with no working gets little credit; a wrong number with clear working is easy to fix in review.

### Part A, Q1: the "always not fraud" model
1. Work out how many transactions it gets right. (It says "not fraud" every time, so which ones are correct?)
2. Accuracy = correct / total. Give it as a percentage to two decimal places.
3. How many frauds does it catch? Write recall for it.
4. Finish with one sentence on what this shows about accuracy. Use your own words.

### Part B, Q2: name TP, FP, FN, TN
- Read the four numbers off the table. Use the "row = actual, column = predicted" rule.
- For each, write a plain-English sentence about what it means for the bank or the customer.

### Part B, Q3: accuracy, precision, recall, F1
- Use the formula table above and follow the worked example step by step.
- Sanity checks: precision and recall are between 0 and 1. F1 lies between them and closer to the smaller one.

### Part B, Q4: lower the threshold
1. The fraud row still adds up to 50, so if FN changes, TP changes too. Work out the new TP first.
2. The legit row still adds up to 9,950. Work out the new TN if you need it.
3. Recompute precision and recall.
4. Put the two versions side by side in a small table.
5. To decide, say what information you would need: what does one missed fraud cost, and what does one false alarm cost? You can sketch the comparison: (FN x cost of a miss) + (FP x cost of a false alarm) for each version, with made-up costs clearly labeled as assumptions.

### Part C, Q5: FPR and precision
1. FPR = FP / all legitimate transactions. You are given both numbers.
2. Precision = TP / (TP + FP). You are given TP (frauds caught) and FP.
3. Compare the two numbers and explain why one looks great and the other does not. Hint: what is in each denominator?
4. Translate precision into an analyst's day: "out of every N alerts, about M are real".

### Part C, Q6: which AUC to report
One or two sentences: pick one, and justify it with what you found in Q5.

### Part D, Q7-Q9: distance and PCA
- Write a few sentences each, in your own words, using the ideas above. A small sketch (a cloud of dots with a few far away) is welcome; describe it in words if you cannot embed it.
- Q8: use a concrete example with numbers, e.g. two transactions that differ by 1 on a V feature and by 500 on Amount.
- Q9: two parts: what PCA does, *and* why it matters that it is already done. Think about what you gain (for distance-based methods) and what you lose (for explaining the model).

## Common mistakes
- Swapping precision and recall. Use the plain-English versions: precision = "of my alerts", recall = "of the real fraud".
- Reading the table the wrong way round (columns as actual).
- Forgetting that changing FN also changes TP when the total number of frauds is fixed.
- Rounding too early. Keep four decimal places until the end.
- Saying ROC-AUC is "wrong". It is not wrong; it answers a question that is less useful when the positive class is tiny.

## Self-check before the PR
- [ ] Every calculation shows formula, substitution, result
- [ ] My confusion matrix totals add up
- [ ] Q4 has a side-by-side comparison and names the costs I would need
- [ ] Q5 explains the gap between FPR and precision using the denominators
- [ ] Part D answers are in my own words
- [ ] Branch `day02-imbalance-stats`, PR opened

## Going further (optional)
F1 weighs precision and recall equally. Look up the F-beta score: how would you choose beta if a missed fraud cost ten times more than a false alarm?
