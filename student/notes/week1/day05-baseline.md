# Day 5 notes: Supervised baseline

Assignment: `assignments/week1/day05-baseline/` · Branch: `day05-baseline` · Code goes in `src/models.py`

## Learning objectives
By the end of this lesson you should be able to:
- Explain why every project starts with a simple baseline
- Explain how logistic regression turns features into a probability
- Train a logistic regression with scikit-learn on your Day 4 split
- Tell the difference between `predict` and `predict_proba`, and why the default 0.5 threshold is arbitrary
- Inspect raw model output (score distributions, top-scored transactions) before judging it with metrics
- Save a trained model without committing it

# Part 1: Lesson

## Why this day matters
A baseline is the yardstick for everything that follows. If a complicated model on Day 6 cannot clearly beat a simple one, the complexity is not worth it. Today is also deliberately **not** about metrics. You will look at what the model actually outputs, so that on Day 7 the numbers mean something to you.

## The concepts

### 1. What a baseline is for
A baseline is the simplest reasonable model. It gives you:
- a number to beat,
- a check that your pipeline works end to end (data in, predictions out),
- often a surprisingly strong result. Simple models are hard to beat on clean tabular data.

Logistic regression is the classic baseline for yes/no problems: fast, stable, and its coefficients can be read.

### 2. How logistic regression works (intuition)
1. It gives each feature a **weight** (coefficient) and adds them up, plus an intercept: `z = w1·V1 + w2·V2 + ... + b`. That is a straight-line score; it can be any number.
2. It squashes `z` through the **sigmoid** function, `1 / (1 + e^-z)`, which turns any number into something between 0 and 1. Large positive z gives a value near 1; large negative z gives a value near 0.
3. Training finds the weights that make the predicted probabilities match the labels as closely as possible (by minimizing *log loss*).

Reading the result: a positive weight means "higher values of this feature push towards fraud", a negative weight pushes towards legit. With scaled features, bigger absolute weights mean stronger influence. (With V1-V28 you can say *which* component matters, not *what it means*.)

### 3. Scores vs. decisions
- `model.predict_proba(X)[:, 1]` gives the **score**: the model's estimated probability of fraud for each row.
- `model.predict(X)` gives the **decision**: 1 if the score is at least 0.5, else 0.

0.5 is a convention, not a business decision. With 0.17% fraud, an unweighted model rarely becomes confident enough to pass 0.5, so `predict` might flag very little. With `class_weight="balanced"`, scores are pushed upward and 0.5 may flag a lot. In both cases, the **score** is the useful output; the threshold gets chosen on Day 7.

### 4. `class_weight`
`class_weight="balanced"` makes each fraud row count roughly as much as 580 legit rows during training. Effects:
- the model pays far more attention to fraud,
- scores shift upward, so they are no longer calibrated probabilities (a score of 0.8 does not mean "80% chance of fraud").
Whether you use it should follow from your Day 4 resampling decision.

### 5. Look before you measure
Before computing any metric, look at the raw output:
- **Score histograms by class** (log y-axis): do fraud scores sit to the right of legit scores? How much do they overlap? The overlap is where every future mistake lives.
- **The top-scored transactions**: sort the test set by score and look at the top 20-50 rows. How many are fraud? What do their Amounts look like?
- **Fraud with low scores**: which real frauds got the lowest scores? Those are the frauds this model cannot see.
- **How many rows `predict` flags** at the default threshold, compared with the number of real frauds.

This builds intuition: a model is a ranking machine, and the threshold is where you cut the ranking.

### 6. Convergence warnings
If you see `ConvergenceWarning`, the optimizer stopped before finishing. Fixes: make sure Amount/Time are scaled (Day 4), and raise `max_iter` (e.g. 1000). Do not just hide the warning.

### 7. Saving a model
```python
import joblib
joblib.dump(model, "models/baseline_logreg.joblib")
model = joblib.load("models/baseline_logreg.joblib")
```
`.joblib` files are gitignored on purpose: models are large binary files and can be regenerated. That means your **training code** must be able to recreate the model. That is the real deliverable.

## Summary
- A baseline is the simplest reasonable model: a yardstick and a pipeline check.
- Logistic regression = weighted sum of features, squashed through a sigmoid into a score between 0 and 1.
- `predict_proba` gives scores; `predict` applies a 0.5 threshold that has no business meaning.
- `class_weight="balanced"` makes the model care about fraud but distorts the probabilities.
- Look at score distributions and top-ranked transactions before reaching for metrics.
- Save models with joblib, never commit them, and keep the code that recreates them.

## Check your understanding
1. What does the sigmoid do, and why is it needed?
2. What is the difference between `predict` and `predict_proba`?
3. Why might an unweighted model flag almost nothing at the 0.5 threshold?
4. What does a negative coefficient on a feature mean?
5. Why is the training code more important than the saved `.joblib` file?

# Part 2: How to attempt each task

### Task 1. Training code in `src/models.py`
1. Write a function such as `train_logistic_regression(X_train, y_train, class_weight=None, random_state=42)` that builds, fits and returns the model. Use `max_iter=1000`.
2. Reuse your Day 4 `split_data` and scaling functions. Do not re-split in the notebook.

### Task 2. Train the baseline
1. In a notebook (e.g. `notebooks/day05_baseline.ipynb`): load, split, scale, train.
2. If you are using class weights or resampling (per your Day 4 decision), apply it to training data only.
3. Optional: train both an unweighted and a weighted version and compare their raw outputs.

### Task 3. Look at raw predictions (the core of today)
For the **test set**, produce:
1. A table of the first rows with `Class`, the score and the default `predict` output side by side.
2. Histograms of scores split by class (log y-axis, or density). Takeaway: how well separated are they?
3. The top 20 highest-scored transactions: how many are fraud?
4. The 10 frauds with the lowest scores: anything they have in common (Amount, Time)?
5. Counts: how many rows `predict` flags vs. how many frauds exist.
6. The coefficients, sorted, as a bar chart. Which features push towards fraud? Do they match the Day 3 correlation chart?

**Do not compute precision, recall, F1 or AUC today.** Describe what you see in words.

### Task 4. Save the model
`joblib.dump` to a `models/` folder (create it). Check `git status` to make sure the file is ignored.

### `submission.md` (suggested structure)
- **What I did:** the model, the settings, and why (link to Day 4)
- **What the raw output looks like:** 4-6 observations from Task 3, each pointing to a cell or plot
- **Surprises:** anything you did not expect
- **Questions for Day 7:** what you want the metrics to tell you

## Common mistakes
- Using `predict` and calling it done. The scores are the interesting part.
- Re-splitting the data with a different random state.
- Training on unscaled Amount/Time and ignoring the convergence warning.
- Jumping to accuracy or F1 today.
- Committing the `.joblib` file.

## Self-check before the PR
- [ ] Training function lives in `src/models.py`
- [ ] The Day 4 split and scaling are reused, not rewritten
- [ ] Score histogram by class, top-scored table, and lowest-scored frauds are in the notebook, each with a takeaway
- [ ] No metric conclusions yet
- [ ] Model saved locally, not committed
- [ ] Branch `day05-baseline`, PR opened

## Going further (optional)
Plot the scores of the top 500 transactions in rank order, coloring frauds. Where does the "mostly fraud" region end? You have just eyeballed a threshold; on Day 7 you will choose one properly.
