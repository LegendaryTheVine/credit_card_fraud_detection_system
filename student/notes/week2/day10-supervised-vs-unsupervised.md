# Day 10 notes: Supervised vs. unsupervised, head to head

Assignment: `assignments/week2/day10-supervised-vs-unsupervised/` · Branch: `day10-supervised-vs-unsupervised`

## Learning objectives
By the end of this lesson you should be able to:
- Compare a supervised and an unsupervised model fairly on the same test set
- Use both threshold-free (PR-AUC) and fixed-budget (precision and recall at the top k) comparisons
- Analyze where two models agree and disagree, and explain why
- Interpret what the anomaly detector catches that the supervised model misses, and vice versa
- Write a clear, evidence-based thesis on when to deploy which approach, or both

# Part 1: Lesson

## Why this day matters
This is the payoff of Week 2. You reveal the labels and find out what the unsupervised model actually caught. The goal is not to crown a winner. It is to understand what each approach is **for**, which is exactly what a leader needs to decide how to invest.

## The concepts

### 1. A fair comparison
Both models must be judged:
- on the **same test rows** (your Day 4 split),
- using **scores** where higher means more suspicious (fraud probability for supervised; flipped anomaly score for unsupervised),
- with the **same metrics** and the **same alert budgets**.

The two kinds of score are on different scales (a probability vs. an arbitrary anomaly number). Do not compare raw values. Compare **rankings**: who puts fraud nearer the top.

### 2. Threshold-free comparison
PR-AUC (`average_precision_score`) and ROC-AUC work on any score, so you can compute them for both models. Plot both PR curves on one chart, with the random baseline at the fraud rate. Expect the supervised model to win on these, since it was trained to find exactly this kind of fraud. The interesting question is by how much, and where on the curve.

### 3. Fixed-budget comparison: precision and recall at k
Leaders think in budgets: "we can review k alerts". So for several budgets (e.g. top 50, 100, 500 test transactions, or the top 0.1%, 0.5%, 1%):
- **precision@k** = share of the k flagged that are fraud,
- **recall@k** = share of all test fraud that is in the top k.

```python
top_k = scores.sort_values(ascending=False).index[:k]
precision_at_k = y_test.loc[top_k].mean()
recall_at_k = y_test.loc[top_k].sum() / y_test.sum()
```
Put both models and several k values in one table. This is often the most persuasive table in the whole project.

### 4. Agreement and disagreement
At a chosen budget k, every **real fraud** in the test set falls into one of four groups:
| | Unsupervised flags it | Unsupervised misses it |
|---|---|---|
| **Supervised flags it** | caught by both | supervised only |
| **Supervised misses it** | unsupervised only | missed by both |

Also look at false alarms: are the two models' false alarms the same transactions, or different ones?

Then **investigate each group**:
- **Caught by both:** probably extreme, obvious frauds.
- **Supervised only:** frauds that look normal overall but match a learned fraud pattern. The anomaly detector cannot see them because they are not unusual.
- **Unsupervised only:** frauds that are unusual but unlike most training fraud. In real life this is where *new* fraud types would show up. Even a few here make the case for running both.
- **Missed by both:** frauds that look normal and unlike known fraud. What would you need to catch them (more features, customer history)?

Compare the groups on Amount, Time/hour, and a couple of top V features (e.g. medians per group). A scatter of supervised score vs. anomaly score for test rows, with fraud highlighted, shows the whole picture in one plot.

Keep the sample sizes in view: the test set has only about 100 frauds, so a group may contain a handful. Describe, don't over-generalize.

### 5. Why the result is biased towards supervised
This dataset favors the supervised model: the test fraud comes from the same two days and the same fraud patterns as the training fraud. In production, fraud **changes** and labels arrive **late**. The supervised model's advantage would shrink for new patterns, which is exactly what the unsupervised model is for. Your thesis should say this.

### 6. Deployment patterns
Common real-world designs to consider in your thesis:
- **Supervised only:** best precision on known fraud; blind to new patterns.
- **Unsupervised only:** when labels do not exist yet (a new product, a new market).
- **Both, in parallel:** supervised drives most alerts; the anomaly detector feeds a smaller "investigate" queue for new patterns.
- **Combined score:** use the anomaly score as an extra feature in the supervised model.
- **Feedback loop:** analysts label anomaly alerts, and those labels retrain the supervised model.

## Summary
- Compare on the same test rows, with rankings rather than raw scores.
- PR-AUC for the whole curve; precision@k and recall@k for business budgets.
- The agreement/disagreement table shows what each model is for.
- Investigate each group; be careful with tiny groups.
- The dataset favors supervised learning. In production, new fraud and late labels change the balance.
- The usual real answer is "both, for different jobs". Your thesis should argue it with evidence.

## Check your understanding
1. Why can't you compare a fraud probability and an anomaly score directly?
2. What do precision@100 and recall@100 each tell a fraud manager?
3. Which group in the agreement table is the strongest argument for keeping the unsupervised model?
4. Why does this dataset flatter the supervised model?
5. Name two ways to combine the two models in production.

# Part 2: How to attempt each task

Create `notebooks/day10_comparison.ipynb`.

### Task 1. Assemble the comparison table
1. Recreate (or load) the test-set scores from your best supervised model (Day 6/7) and Isolation Forest (Day 9), indexed by the original row index.
2. Join them with `y_test` into one DataFrame: `supervised_score`, `anomaly_score`, `Class`.
3. Check: same number of rows, no missing values, and both scores "higher = more suspicious".

### Task 2. Threshold-free metrics
PR-AUC and ROC-AUC for both models in a table; both PR curves on one plot with the baseline. Takeaway.

### Task 3. Fixed-budget metrics
Precision@k and recall@k for 3-4 values of k. Include the k matching your Day 7 threshold (how many alerts it produced on test) and your Day 9 flagging rule. Takeaway.

### Task 4. Agreement analysis
1. Pick one budget k (justify it).
2. Build the 2x2 table for real frauds, plus the overlap of false alarms.
3. Profile each group (count, median Amount, hour, a few V features).
4. Scatter: supervised score vs. anomaly score, frauds highlighted (log axes may help).
5. Look at a few individual frauds from "unsupervised only" and "missed by both" and describe them.

### Task 5. The thesis
In `submission.md`, write a short thesis (about 300-500 words) on when to use each approach. A strong thesis:
- opens with a one-sentence recommendation,
- cites 2-3 specific numbers from your tables,
- explains what each model is good and bad at, with evidence from the agreement analysis,
- addresses the dataset's bias towards supervised and what changes in production (new fraud, late labels),
- recommends a deployment pattern and says what you would monitor to know it is working.

### `submission.md` (suggested structure)
- **Setup:** models, test set, score conventions
- **Results:** AUC table and precision/recall@k table
- **Where they agree and disagree:** the 2x2 table and group profiles
- **Thesis**

## Common mistakes
- Comparing raw score values across models.
- Using different test rows for the two models.
- Forgetting the anomaly score sign flip, which makes the detector look worse than random.
- Declaring a winner from AUC alone, without the budget view or the disagreement analysis.
- Drawing strong conclusions from groups of 3-5 frauds.

## Self-check before the PR
- [ ] Both models scored on identical test rows, same score direction
- [ ] AUC table and PR curves for both
- [ ] Precision@k / recall@k table for several budgets
- [ ] Agreement table with group profiles and examples
- [ ] Thesis with a recommendation, evidence, limitations and a deployment pattern
- [ ] Branch `day10-supervised-vs-unsupervised`, PR opened

## Going further (optional)
Add the anomaly score as an extra feature to your supervised model and re-run cross-validation on the training set. Does it help? (Fit Isolation Forest inside each training fold to avoid leakage.)
