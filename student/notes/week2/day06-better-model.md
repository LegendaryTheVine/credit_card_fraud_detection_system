# Day 6 notes: A better supervised model

Assignment: `assignments/week2/day06-better-model/` · Branch: `day06-better-model` · Code goes in `src/models.py`

## Learning objectives
By the end of this lesson you should be able to:
- Explain how a decision tree makes predictions, and why one tree on its own overfits
- Explain how a random forest (bagging) and gradient boosting (boosting) fix that in different ways
- Train a random forest or gradient boosting model and compare it fairly with your baseline
- Use cross-validation instead of the test set to make modeling choices
- Compute and interpret built-in and permutation feature importance
- Explain what anonymized V1-V28 features cost you when explaining a model

# Part 1: Lesson

## Why this day matters
Logistic regression draws one straight boundary between fraud and legit. Real fraud patterns are rarely that simple: "small amount AND unusual V14 AND night-time" is the kind of combination trees capture naturally. Today you try a more flexible model, and you learn to ask the right question: *is it better enough to justify being harder to explain?*

## The concepts

### 1. Decision trees
A decision tree asks a sequence of yes/no questions: "Is V14 < -3.2? If yes, is Amount < 5?..." Each question splits the data into two groups that are purer (more all-fraud or all-legit) than before. A transaction's prediction is the fraud share in the leaf it ends up in.

Strengths: captures interactions and non-linear patterns; no scaling needed (a split is a split, whatever the units); easy to read when small.
Weakness: a deep tree memorizes the training data (**overfitting**). Small changes in the data give a very different tree.

### 2. Random forest: many trees, averaged (bagging)
- Train hundreds of trees, each on a random bootstrap sample of the rows, considering a random subset of features at each split.
- Average their votes.
- Each tree overfits in a different way; averaging cancels much of the noise. Result: more accurate and much more stable than a single tree.

Key settings in `RandomForestClassifier`:
| Parameter | Meaning | Starting point |
|---|---|---|
| `n_estimators` | number of trees | 200-300 |
| `max_depth` / `min_samples_leaf` | limit tree size to reduce overfitting | try `min_samples_leaf` 1, 5, 20 |
| `class_weight` | `"balanced"` or `"balanced_subsample"` for imbalance | follow your Day 4 decision |
| `n_jobs=-1` | use all CPU cores | always |
| `random_state` | reproducibility | 42 |

### 3. Gradient boosting: trees that fix each other's mistakes
- Build small trees **one after another**; each new tree focuses on the errors the previous ones made.
- Often the most accurate option for tabular data, but more sensitive to settings, and can overfit if you train too long.
- In scikit-learn, `HistGradientBoostingClassifier` is fast on 280k rows. Key settings: `learning_rate`, `max_iter`, `max_leaf_nodes`, `class_weight`.

Pick **one** (forest or boosting) for the main comparison. Trying both is a bonus.

### 4. Fair comparison
The comparison with the baseline is only fair if:
- both models use the **same** train/test split (your Day 4 function),
- both get the same treatment of imbalance (or you compare that deliberately),
- you compare on the same metric: **PR-AUC** (`average_precision_score`) on scores, not accuracy,
- any tuning happens **without** the test set.

**Cross-validation** is how you tune without the test set. `StratifiedKFold(n_splits=5)` splits the *training* data into 5 parts; the model is trained on 4 and scored on the 5th, five times over. `cross_val_score(model, X_train, y_train, cv=cv, scoring="average_precision")` gives you five scores; report the mean and the spread. The spread tells you how much of a difference between models is real and how much is noise. With only ~400 training frauds, it is not small.

Then, once you have decided, score each final model **once** on the test set.

On run time: a forest on 228k rows with 5-fold CV can take minutes. Use `n_jobs=-1`, start with fewer trees, and do not tune a big grid.

### 5. Feature importance, and its traps
**Built-in importance (`model.feature_importances_`)** measures how much each feature reduced impurity across all splits. It is fast, but biased towards features with many distinct values, and it is computed on training data.

**Permutation importance** (`sklearn.inspection.permutation_importance`) shuffles one feature at a time on held-out data and measures how much the score drops. It is slower but more honest: "how much does the model actually rely on this feature for new data?" Use `scoring="average_precision"` and a sample of the data if it is slow.

Interpreting importance:
- Importance means **the model uses it**, not that it **causes** fraud.
- Correlated features share importance, so each one can look less important than it is. (Less of an issue for V1-V28, which are uncorrelated.)
- Compare with your Day 3 correlation chart and Day 5 coefficients. Agreement across methods is reassuring; disagreement is worth a sentence.

### 6. The cost of anonymous features
Your model might say "V14 is the most important feature". You cannot tell a fraud analyst, a regulator or a customer what V14 *is*. Each V feature is a mixture of the bank's original features. Consequences:
- You can **rank** features but not **explain** them in business terms.
- You cannot check whether a feature is a proxy for something sensitive (Day 11).
- You cannot use domain knowledge to engineer better features.
Amount and Time are the only features you can talk about in plain language. In a real project the bank would have the original features and you would explain using those.

## Summary
- Trees capture interactions; one tree overfits; forests average many trees, boosting chains them.
- Compare models on the same split and the same metric (PR-AUC), and tune with cross-validation, never on the test set.
- Built-in importance is quick but biased; permutation importance on held-out data is more trustworthy.
- Importance shows reliance, not causation.
- With PCA features you can rank but not explain. That is a real cost when a decision affects a customer.

## Check your understanding
1. Why does a single deep tree overfit, and how does a forest reduce that?
2. What is the main difference between bagging and boosting?
3. Why do trees not need scaled features?
4. Why is cross-validation spread worth reporting when there are only ~400 training frauds?
5. What can you tell a business stakeholder about "V14 is the most important feature"? What can't you tell them?

# Part 2: How to attempt each task

### Task 1. Add the model to `src/models.py`
Write `train_random_forest(...)` (or `train_gradient_boosting(...)`) next to your baseline function, with sensible defaults and `random_state`.

### Task 2. Compare with the baseline using cross-validation
1. Set up `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`.
2. Run `cross_val_score(..., scoring="average_precision")` for the baseline and the new model on **training data only**.
3. Make a small table: model, mean PR-AUC, std. Takeaway: is the difference bigger than the spread?
4. If you try a few settings (e.g. `min_samples_leaf`), keep it small (2-4 options) and use CV to choose.
5. If you used SMOTE, put it in an `imblearn.pipeline.Pipeline` so it is only applied to the training folds.

### Task 3. Final scores on the test set
Fit both final models on the full training set, score the test set once, and report PR-AUC (and ROC-AUC as secondary) for both. Do not change anything afterwards because of these numbers.

### Task 4. Feature importance
1. Plot built-in importances (top 15).
2. Compute permutation importance on the test set or a validation set (top 15).
3. Put them next to the Day 3 correlations and Day 5 coefficients. Which features appear in all of them?
4. Write what you can and cannot conclude.

### `submission.md` (suggested structure)
- **Model chosen and settings:** what and why
- **Comparison table:** CV mean ± std and test PR-AUC for baseline vs. new model
- **Is it better enough?** Your judgment, considering accuracy gain vs. explainability, training time and complexity
- **Feature importance:** top features, agreement across methods, what it does and does not mean
- **What anonymized features cost us:** 3-5 sentences, with a concrete example of a question you cannot answer

## Common mistakes
- Tuning on the test set.
- Comparing models trained on different splits.
- Reporting accuracy.
- Calling importances "causes" or "what fraudsters do".
- Running a huge grid search that takes hours. Small, deliberate experiments are better.

## Self-check before the PR
- [ ] Same split as Days 4-5
- [ ] CV results with mean and spread for both models
- [ ] Test set used once, at the end
- [ ] Two kinds of feature importance, compared
- [ ] A clear written judgment on whether the extra complexity is worth it
- [ ] Branch `day06-better-model`, PR opened, no model files committed

## Going further (optional)
Train a single shallow tree (`max_depth=3`) and draw it with `sklearn.tree.plot_tree`. It is less accurate, but you can show it to someone. How much accuracy are you giving up for that?
