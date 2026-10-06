# Day 9 notes: Isolation Forest

Assignment: `assignments/week2/day09-isolation-forest/` · Branch: `day09-isolation-forest`

## Learning objectives
By the end of this lesson you should be able to:
- Explain how Isolation Forest finds anomalies, and why it isolates them faster than normal points
- Train an Isolation Forest without using the label and produce an anomaly score for every transaction
- Handle scikit-learn's sign conventions so that "higher score = more anomalous"
- Explain the `contamination` setting and why you cannot tune it properly without labels
- Optionally build a Local Outlier Factor model and compare it
- Choose a flagging rule without labels

# Part 1: Lesson

## Why this day matters
Day 8 built intuition with distances. Today you build a real unsupervised detector that scales to all 284k transactions. Its scores are what you will put head to head with the supervised model on Day 10. The label stays hidden all day.

## The concepts

### 1. The idea: anomalies are easy to isolate
Imagine playing "guess the transaction" by cutting the data with random lines:
- pick a random feature,
- pick a random split value between that feature's min and max,
- split the data in two, and repeat on each side until every point is alone.

A transaction in the dense crowd needs **many** cuts before it is alone. An unusual transaction, sitting far out on some feature, is often separated after **a few** cuts.

An **isolation tree** records how many cuts (the *path length*) each point needed. An **Isolation Forest** builds many such trees on random subsamples and averages the path lengths. **Short average path = anomaly.**

Why it is popular:
- no distances, so it is fast and scales to large data,
- works on subsamples (`max_samples`, default 256 rows per tree), so training is cheap,
- does not need scaling (like all tree methods, cuts are unit-free). Scaling does no harm, though, so you can reuse your Day 4 pipeline for consistency.

### 2. The key settings
```python
from sklearn.ensemble import IsolationForest

iso = IsolationForest(
    n_estimators=200,       # number of trees
    max_samples=256,        # rows per tree ("auto" = min(256, n))
    contamination="auto",   # only affects predict(); see below
    random_state=42,
    n_jobs=-1,
)
iso.fit(X_train)            # features only, no y
```

**`contamination`** is the share of data you expect to be anomalous. It only sets the cut-off that `predict()` uses; it does **not** change the scores. Without labels you cannot measure the true contamination, so either keep `"auto"` and choose your own cut-off from the scores, or set it from a business assumption (e.g. analyst capacity) and say so.

### 3. Getting the score the right way round
scikit-learn gives you:
| Method | Meaning |
|---|---|
| `score_samples(X)` | higher = **more normal** |
| `decision_function(X)` | score_samples shifted by the cut-off; negative = anomaly |
| `predict(X)` | **-1** = anomaly, **+1** = normal (not 1/0!) |

For the rest of the course you want "higher = more suspicious", like a fraud probability, so define:
```python
anomaly_score = -iso.score_samples(X)
```
Write this convention down in your notebook. Mixing up the sign is the most common bug on this day and on Day 10.

### 4. Fit on what, score what?
- **Fit on training features only** (no label). That mirrors production, where the model learns "normal" from past data.
- **Score every transaction**: train and test. The deliverable is a score for every row.
- Keep the **test** scores aside for the Day 10 comparison with the supervised model on exactly the same rows.

Note that the training data contains ~400 frauds. Isolation Forest does not know that; it is robust to a small amount of contamination. (In a real system you might also try training on transactions known to be legit. That would be a semi-supervised setup and uses labels, so not today.)

### 5. Choosing the flagging rule without labels
Options, all defensible if you explain them:
- **Top-k% by score**: e.g. flag the 0.2% most anomalous.
- **Capacity-based**: if analysts can review N alerts per day, pick the cut-off that produces N alerts per day's worth of transactions.
- **Shape of the scores**: a histogram or sorted-score plot sometimes shows a natural break.
Whichever you choose, choose it on **training** scores and apply it unchanged to test.

### 6. Local Outlier Factor (optional)
LOF compares how dense a point's neighborhood is with how dense its neighbors' neighborhoods are. A point in a sparse spot next to dense neighbors gets a high outlier factor.
- `LocalOutlierFactor(n_neighbors=20, novelty=True)` lets you `fit` on training data and score new data with `score_samples` (same sign convention: higher = more normal).
- LOF uses distances, so **scale first**, and it is slow on large data. Fit on a sample.
- Compare its top-ranked transactions with Isolation Forest's. Agreement suggests robust anomalies; disagreement shows each method's own idea of "unusual".

### 7. Sanity checks without the label
How do you know the model is doing something sensible when you cannot check against fraud?
- **Stability:** retrain with a different `random_state`. Do the top 1% change a lot?
- **Inspect the top-scored rows:** are they extreme on some features (huge Amount, extreme V values)? Does that look "unusual" to a human?
- **Distribution:** is there a long tail of high scores, or is everything similar?

## Summary
- Isolation Forest cuts the data at random; anomalies are isolated in few cuts.
- Fit on training features without the label; score every transaction.
- Use `-score_samples` so higher means more suspicious; `predict` returns -1/+1.
- `contamination` only sets a cut-off; without labels it is an assumption.
- Choose the flagging rule on training scores and apply it unchanged to test.
- Check stability and inspect the top-scored rows, still without the label.

## Check your understanding
1. Why does an anomaly usually need fewer random cuts to isolate?
2. What does `predict()` return for an anomaly?
3. Does changing `contamination` change the anomaly scores?
4. Why does Isolation Forest not need scaling, while LOF does?
5. How can you check your detector is stable without using labels?

# Part 2: How to attempt each task

Create `notebooks/day09_isolation_forest.ipynb`. Consider putting the training function in `src/models.py` (e.g. `train_isolation_forest(X_train, random_state=42)`).

### Task 1. Prepare features without the label
Same Day 4 split and preprocessing. Drop `Class`. Confirm by printing the column list that `Class` is not there.

### Task 2. Train the Isolation Forest
1. Fit on `X_train` only.
2. Compute `anomaly_score = -iso.score_samples(...)` for train and test.
3. Store the scores in a DataFrame aligned with the original row index (you will join them to labels on Day 10). Save them to a file in a gitignored location if you like, or make sure the notebook can recompute them.

### Task 3. Look at the scores
1. Histogram of training scores. Takeaway: is there a tail?
2. The 20 highest-scoring transactions with their Amount and a few top V features. Takeaway: what makes them unusual?
3. Stability: retrain with two other `random_state` values and measure the overlap of the top 1% (e.g. `len(set_a & set_b) / len(set_a)`).

### Task 4. Choose a flagging rule
1. Decide the rule (top-k%, capacity, or natural break) and justify it in one paragraph.
2. Compute the cut-off on training scores.
3. Apply it to test and report how many test transactions are flagged. Not how many are fraud: you still do not know.

### Task 5 (optional). Local Outlier Factor
Scaled features, fit on a sample of training data with `novelty=True`, score the test set, and compare the top-ranked lists with Isolation Forest's.

### `submission.md` (suggested structure)
- **How Isolation Forest works:** a short explanation in your own words
- **Settings and why:** n_estimators, max_samples, contamination
- **Score convention:** state it clearly
- **What the top anomalies look like:** 3-5 observations
- **Stability check result**
- **Flagging rule:** choice, reason, number flagged on test
- **(Optional) LOF comparison**
- **Prediction for Day 10:** what share of your flagged transactions do you expect to be fraud, and why?

## Common mistakes
- Passing `y` to `fit` or keeping `Class` in the feature matrix.
- Treating `predict()` output as 1 = fraud. It is -1 = anomaly.
- Forgetting to flip the sign of `score_samples`.
- Choosing the cut-off by peeking at test labels.
- Running LOF on all rows without a sample.

## Self-check before the PR
- [ ] No label used anywhere (search the notebook for `Class` and `y_`)
- [ ] Scores for every transaction, higher = more anomalous, aligned to row index
- [ ] Stability check done
- [ ] Flagging rule chosen on training data and justified
- [ ] Branch `day09-isolation-forest`, PR opened, no model files committed

## Going further (optional)
Train Isolation Forest on only V1-V28 (no Amount, no Time) and compare the top anomalies. Which features drive "unusualness" here?
