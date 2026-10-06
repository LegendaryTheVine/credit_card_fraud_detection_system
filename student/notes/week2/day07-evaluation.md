# Day 7 notes: Evaluation, done right

Assignment: `assignments/week2/day07-evaluation/` · Branch: `day07-evaluation` · Code goes in `src/evaluate.py`

## Learning objectives
By the end of this lesson you should be able to:
- Build confusion matrices at several thresholds and explain how they change
- Compute precision, recall and F1 by hand once, then confirm with scikit-learn
- Plot and interpret ROC and precision-recall curves, and explain why PR-AUC is the headline here
- Turn your Day 3 cost assumptions into a total-cost function
- Choose a threshold that minimizes expected cost on validation data, and report it honestly on the test set
- Explain your threshold choice to a non-technical stakeholder

# Part 1: Lesson

## Why this day matters
A model produces scores. A business needs decisions. The **threshold** connects the two, and choosing it is where the model meets money. Today you bring together Day 2 (metrics), Day 3 (cost assumptions) and Days 5-6 (scores) into a single defensible decision.

## The concepts

### 1. One model, many confusion matrices
A model does not have *a* confusion matrix. It has one for every threshold. As the threshold falls:
- TP and FP rise (more alerts),
- FN and TN fall,
- recall rises, precision usually falls.

Seeing three or four matrices side by side (e.g. thresholds 0.9, 0.5, 0.1, 0.01) makes the trade-off concrete in a way a single number never does.

```python
from sklearn.metrics import confusion_matrix
y_pred = (scores >= threshold).astype(int)
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
```
Careful: scikit-learn's layout is `[[TN, FP], [FN, TP]]`, so the legit row comes first. That is not the order used in the Day 2 tables.

### 2. By hand, then by library
Do it once by hand from one confusion matrix, using the Day 2 formulas. Then confirm with `precision_score`, `recall_score`, `f1_score`. If they disagree, you have found a bug in your understanding or your code. Both are worth finding.

### 3. Curves and areas
- `roc_curve(y_true, scores)` → FPR and TPR per threshold; `roc_auc_score` summarizes it.
- `precision_recall_curve(y_true, scores)` → precision and recall per threshold; `average_precision_score` (PR-AUC) summarizes it.
- Draw the **random baseline** on each: the diagonal on ROC, a horizontal line at the fraud rate on PR.
- Plot baseline and Day 6 model on the same axes. Where on the PR curve does one model beat the other? A model can win at high recall and lose at high precision.

From Day 2: ROC-AUC is often 0.95+ for every reasonable model here, which hides real differences. PR-AUC shows them. Report PR-AUC as the headline and ROC-AUC as secondary.

### 4. From metrics to money
F1 treats a missed fraud and a false alarm as equally bad. The business does not. Use your Day 3 assumptions:

```
total cost(threshold) = FN(threshold) × cost_of_missed_fraud  +  FP(threshold) × cost_of_false_alarm
```

Refinements you can add if you want (state them as assumptions):
- cost of a missed fraud = that transaction's actual `Amount` + a fixed fee, instead of a flat number,
- every alert (TP or FP) costs analyst review time,
- a caught fraud still costs something (handling).

Sweep thresholds from 0 to 1 (e.g. `np.linspace(0, 1, 501)`, or the thresholds from `precision_recall_curve`), compute total cost at each, and plot cost against threshold. The minimum is your **cost-optimal threshold**. Compare it with "do nothing" (flag nothing: cost = every fraud missed), and "flag everything".

### 5. Where to choose the threshold
Choosing a threshold is a modeling decision, so it must **not** be made on the test set. Options:
- Split the training set into train and **validation** (stratified), fit on train, choose the threshold on validation, then refit on the full training set if you like.
- Or use out-of-fold scores from cross-validation (`cross_val_predict(..., method="predict_proba")`) on the training set and choose the threshold on those.

Then apply that **fixed** threshold to the test set and report the confusion matrix, precision, recall and total cost. If the test cost is much worse than the validation cost, say so. It is a finding, not a failure.

### 6. Sensitivity: how fragile is the choice?
Your costs are guesses. Re-run the optimum with the false-alarm cost halved and doubled. If the chosen threshold barely moves, your decision is robust. If it swings wildly, say that the business needs better cost estimates before go-live. This is exactly the kind of insight leadership values.

### 7. Translate the result
A stakeholder does not want "threshold 0.37". They want something like: *"Out of every 100,000 transactions we would flag about N for review; about M of those are real fraud; we would catch about R% of fraud; estimated cost X vs. Y with no model."* Write that sentence for your chosen threshold.

## Summary
- Every threshold gives a different confusion matrix; the curves summarize all of them.
- PR-AUC is the headline; ROC-AUC flatters on imbalanced data.
- Total cost = FN × miss cost + FP × false alarm cost. Minimize it over thresholds.
- Choose the threshold on validation or out-of-fold data; report it once on the test set.
- Check how sensitive the choice is to your cost assumptions.
- Translate the result into alerts, catches and money.

## Check your understanding
1. What happens to FP and FN as you lower the threshold?
2. In scikit-learn's confusion matrix, which cell is top-left?
3. Why is choosing the threshold on the test set a form of leakage?
4. If false alarms got twice as expensive, would the optimal threshold go up or down? Why?
5. What does the horizontal baseline on a PR curve represent?

# Part 2: How to attempt each task

### Task 1. Helpers in `src/evaluate.py`
Write small, reusable functions, for example:
- `metrics_at_threshold(y_true, scores, threshold)` → dict with TP, FP, FN, TN, precision, recall, F1
- `total_cost(y_true, scores, threshold, cost_fn, cost_fp)` → number
- `cost_curve(y_true, scores, thresholds, cost_fn, cost_fp)` → array of costs
You will reuse these on Day 10 and in the model card.

### Task 2. Confusion matrices at several thresholds
For your best model (and optionally the baseline), on validation data: show matrices at 3-4 thresholds in one table. Takeaway: describe the trade-off in words.

### Task 3. By hand once, then sklearn
Pick one matrix. Compute precision, recall and F1 by hand in a markdown cell (formula, numbers, result). Then compute them with sklearn and show they match.

### Task 4. ROC and PR curves
Both models on the same plot, with random baselines. Report ROC-AUC and PR-AUC in a table. Write which one you would put in front of leadership and why.

### Task 5. Cost-based threshold
1. Restate your Day 3 cost assumptions (update them if your thinking changed, and say why).
2. Plot total cost vs. threshold on validation data. Mark the minimum.
3. Compare with three reference points: flag nothing, default 0.5, best-F1 threshold.
4. Sensitivity: halve and double the false alarm cost; report where the optimum moves.
5. Apply the chosen threshold to the **test set once**; report the matrix, precision, recall and cost.

### `submission.md` (suggested structure)
- **Hand vs. sklearn check:** one short block
- **Curves:** the AUC table and which metric you would lead with
- **Cost assumptions:** the numbers and a reason for each
- **Chosen threshold:** value, how it was chosen (which data), and the comparison table
- **Test result:** confusion matrix and cost on test
- **Sensitivity:** how robust the choice is
- **One-paragraph stakeholder summary** in plain language

## Common mistakes
- Choosing the threshold on the test set.
- Mixing up the sklearn matrix layout.
- Using F1 as if it were the business objective.
- Reporting a threshold with no translation into alerts and money.
- Forgetting that a SMOTE- or class-weighted model's scores are not calibrated probabilities: a threshold of 0.9 is not "90% sure".

## Self-check before the PR
- [ ] Helper functions in `src/evaluate.py`
- [ ] Hand calculation matches sklearn
- [ ] ROC and PR curves with baselines, both models
- [ ] Threshold chosen on validation / out-of-fold data, not test
- [ ] Cost curve plotted, with sensitivity check
- [ ] Plain-language summary for a stakeholder
- [ ] Branch `day07-evaluation`, PR opened

## Going further (optional)
Real teams often have a fixed **alert budget** ("analysts can review 200 alerts a day"). Instead of a cost, choose the threshold that produces that many alerts per 100,000 transactions, and report the recall you get. Compare it with your cost-optimal choice.
