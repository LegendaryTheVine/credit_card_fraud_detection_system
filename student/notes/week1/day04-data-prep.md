# Day 4 notes: Data preparation

Assignment: `assignments/week1/day04-data-prep/` · Branch: `day04-data-prep` · Code goes in `src/data.py` and `src/features.py`

## Learning objectives
By the end of this lesson you should be able to:
- Explain why we hold back a test set and why it must stay untouched
- Do a stratified train/test split and verify it
- Explain data leakage and avoid the most common forms of it
- Scale `Amount` and `Time` correctly (fit on train only) and explain why V1-V28 need different treatment
- Compare the three ways of handling imbalance (undersampling, SMOTE, class weights + threshold tuning) and justify a choice
- Put preparation code in reusable functions

# Part 1: Lesson

## Why this day matters
Nearly every result you report later depends on today's decisions. A careless split or a leak makes every later metric optimistic, and you will not find out until the model fails in production. Today is about making the evaluation **honest**.

## The concepts

### 1. Why a test set?
A model is useful only if it works on transactions it has **never seen**. So you hide part of the data, the **test set**, train on the rest, and score on the hidden part at the very end.

The test set only stays honest if you never use it to *make a choice*: not to pick features, not to pick a model, not to pick a threshold. If you look at test results, change something and look again, you are slowly fitting to the test set. For choices, use a **validation** set carved out of training data, or cross-validation (Day 6-7).

A common split is 80% train / 20% test.

### 2. Stratification
Fraud is about 0.17% of rows. A purely random 20% split will *on average* contain the right number of frauds, but any particular split can be off. With so few positives, that noticeably changes your metrics. A **stratified split** forces the fraud rate to be the same in train and test.

```python
from sklearn.model_selection import train_test_split

X = df.drop(columns="Class")
y = df["Class"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
```
Always **verify**: print `y_train.mean()` and `y_test.mean()` and the number of frauds in each.

### 3. Data leakage
**Leakage** is when information the model would not have in real life gets into training. The common forms:
- **Preprocessing before splitting.** If you fit a scaler on all data, the training data has "seen" the test set's mean and spread. Rule: **split first, then fit any preprocessing on train only**, then *apply* it to test.
- **Resampling before splitting.** If you SMOTE first and then split, synthetic points built from test frauds end up in training. Rule: resample **training data only**.
- **Duplicates across the split.** If an identical row is in both train and test, the model is tested on something it memorized. This is why the duplicates you found on Day 3 matter.
- **Time leakage.** In real fraud systems you train on the past and test on the future. A random split mixes them. With two days of data we accept a random stratified split, but say so as a limitation.

### 4. Scaling
Many models care about feature scale (Day 2: distance is dominated by big numbers; logistic regression's optimization also behaves better on scaled data). Tree models (Day 6) do not care.

| Scaler | What it does | Good for |
|---|---|---|
| `StandardScaler` | subtract mean, divide by std | roughly symmetric data |
| `RobustScaler` | subtract median, divide by interquartile range | data with outliers, like Amount |
| `np.log1p` then a scaler | compress the skew first | very skewed data |

The correct pattern:
```python
from sklearn.preprocessing import RobustScaler

scaler = RobustScaler()
X_train[["Amount", "Time"]] = scaler.fit_transform(X_train[["Amount", "Time"]])   # fit on train
X_test[["Amount", "Time"]] = scaler.transform(X_test[["Amount", "Time"]])          # only transform test
```
(Work on copies, e.g. `X_train = X_train.copy()`, to avoid pandas warnings and surprises.)

**What about V1-V28?** They are already PCA outputs, centered around zero, with variances that decrease from V1 to V28. Re-standardizing them is not "wrong", but it changes their relative scale, which carries information about how much variation each component holds. Do not scale them *blindly*: decide, and write down why. Whatever you choose, apply it consistently.

**What about Time?** Ask whether raw Time even makes sense as a feature. It is "seconds since the file started": a new transaction tomorrow would have a value the model has never seen. Options: scale it and keep it, replace it with an hour-of-day feature, or drop it. Any of these is acceptable if you justify it.

The cleanest long-term approach is a scikit-learn `ColumnTransformer` + `Pipeline`, which bundles the scaling with the model so it is fitted on train and applied identically everywhere (including the API on Day 12). It is fine to start with the manual version today and move to a pipeline later.

### 5. Handling imbalance: three strategies
| Strategy | How | Pros | Cons |
|---|---|---|---|
| **Random undersampling** | Throw away legit rows until classes are balanced | Fast; small training set | Throws away a huge amount of information about normal behavior |
| **SMOTE** (oversampling) | Create synthetic frauds by interpolating between real frauds and their neighbors | Keeps all data; more fraud examples | Synthetic points may not look like real fraud; slower; easy to leak; changes predicted probabilities |
| **Keep the imbalance** + `class_weight="balanced"` + **threshold tuning** | Train on the real distribution; make fraud errors count more; choose the threshold on Day 7 | No synthetic data; probabilities stay meaningful; simplest | Default 0.5 threshold is meaningless; you must tune it |

Key point: **resampling changes the training data, never the test data.** The test set must look like the real world (0.17% fraud), or your metrics mean nothing.

If you use imbalanced-learn, its `Pipeline` (`from imblearn.pipeline import Pipeline`) applies SMOTE only during `fit`, which protects you from leakage inside cross-validation.

There is no single right answer. The grade is for a decision you can defend, ideally backed by a quick experiment on a validation split.

### 6. Reusable code
From today, preparation lives in `src/` so every later day uses exactly the same split. A shape to aim for:
```python
# src/data.py
def split_data(df, test_size=0.2, random_state=42):
    """Stratified train/test split. Returns X_train, X_test, y_train, y_test."""

# src/features.py
def fit_scaler(X_train): ...
def apply_scaler(scaler, X): ...
```
Write a short docstring for each function. Same `random_state` everywhere means everyone (you, your instructor, the Day 10 comparison) gets the identical test set.

## Summary
- Split first, stratified, with a fixed random state. Verify the fraud rate in both parts.
- Fit every preprocessing step on train only; apply it to test.
- Resample (if at all) only the training data. The test set keeps the real 0.17%.
- Amount needs scaling (robust or log); Time needs a decision; V1-V28 should not be rescaled blindly.
- Imbalance options: undersample, SMOTE, or class weights + threshold tuning. Pick one and justify it.
- Put it in `src/` so every later day reuses it.

## Check your understanding
1. Why is fitting a scaler on the whole dataset a leak?
2. What should the fraud rate in your test set be after SMOTE on the training set?
3. Why do tree models not need scaling?
4. Why is a random split less realistic than a time-based one for fraud?
5. What do you lose with random undersampling?

# Part 2: How to attempt each task

### Task 1. Decide on duplicates
1. Revisit your Day 3 finding. Decide: keep or drop. Things to consider: are any fraud? Could they be real repeated transactions? Could they land on both sides of the split?
2. If you drop, do it **before** splitting, and note how many rows and frauds you removed.
3. Write the decision and reason in `submission.md`.

### Task 2. Stratified split in `src/data.py`
1. Add a `split_data` function using `train_test_split(..., stratify=y, random_state=...)`.
2. In a notebook (e.g. `notebooks/day04_prep.ipynb`), call it and print the shapes, the number of frauds and the fraud rate in each part.
3. Paste those numbers into `submission.md`.

### Task 3. Scaling in `src/features.py`
1. Decide how to treat Amount (robust scaler? log then scale?), Time (keep, transform, or drop?) and V1-V28 (leave as is, or scale, and why?).
2. Write the functions so the scaler is **fitted on X_train only** and then applied to X_test.
3. Verify: after scaling, Amount in train should be centered (median about 0 for a robust scaler). Test will be close but not exactly the same. That is expected and is evidence you did it right.

### Task 4. The resampling decision
1. Write down the three options in your own words.
2. Optional but strongly recommended: a quick experiment. Carve a validation set from the training data, train a simple logistic regression with (a) nothing, (b) `class_weight="balanced"`, (c) SMOTE on the training part only, and compare **PR-AUC** (`sklearn.metrics.average_precision_score`) on the validation set. Never use the test set for this.
3. Write the justification: what you chose, why, what you gave up, and what result would make you change your mind.

### `submission.md` (suggested structure)
- **What I did:** split, scaling and duplicate decision in 3-5 bullets
- **Split check:** a small table of rows / frauds / fraud rate for train and test
- **Scaling decisions:** Amount, Time, V1-V28, one reason each
- **Resampling decision:** choice + justification (+ experiment results if you ran it)
- **Leakage I avoided:** list the specific traps and how your code avoids them

## Common mistakes
- Scaling or SMOTE-ing before the split.
- Resampling the test set.
- Forgetting `stratify=y`.
- Using `fit_transform` on the test set (it should be `transform`).
- Changing the test set's `random_state` between days, so results are not comparable.
- Overwriting `df` in place inside functions and getting confusing results in the notebook.

## Self-check before the PR
- [ ] `split_data` is in `src/data.py` and is stratified with a fixed random state
- [ ] Fraud rates printed for train and test, and they match closely
- [ ] Scaler fitted on train only
- [ ] Test set is not resampled
- [ ] Resampling decision justified in writing
- [ ] Notebook runs top to bottom; no data or model files committed
- [ ] Branch `day04-data-prep`, PR opened

## Going further (optional)
Rewrite your preparation as a `ColumnTransformer` inside a `Pipeline`. You will need this on Day 12, when the API must apply exactly the same preprocessing to a single incoming transaction.
