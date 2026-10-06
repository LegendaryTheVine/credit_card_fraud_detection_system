# Glossary

Plain-English definitions of the terms used in the course. When the notes use a term for the first time, it is defined here.

**Accuracy** - Share of all predictions that are correct. Misleading when one class is rare.

**Anomaly / outlier** - A data point that looks very different from most others. Unusual is not the same as fraudulent.

**Anomaly score** - A number saying how unusual a transaction looks. Higher means more unusual (check the sign convention of each library).

**AUC (area under the curve)** - One number that summarizes a whole curve across all thresholds. See ROC-AUC and PR-AUC.

**Baseline** - The first simple model. Later models must beat it to be worth their extra complexity.

**Class / label** - The answer column. Here `Class = 1` is fraud and `Class = 0` is legitimate.

**Class imbalance** - One class is far more common than the other. Here roughly 580 legitimate transactions for every fraud.

**`class_weight`** - A model setting that makes mistakes on the rare class count more during training, without changing the data.

**Confusion matrix** - A 2x2 table of actual vs. predicted: TP, FP, FN, TN.

**Cost-based threshold** - Picking the threshold that minimizes total business cost: (missed frauds x cost of a miss) + (false alarms x cost of a false alarm).

**Cross-validation (CV)** - Splitting the training data into several folds and training/validating on each in turn, to get a more reliable estimate without touching the test set.

**Data leakage** - Information from the test set (or from the future) sneaking into training, which makes results look better than they will be in real life.

**Drift** - The data in production slowly changes compared with the training data, so the model gets worse over time.

**F1 score** - Harmonic mean of precision and recall. High only if both are high.

**False negative (FN)** - A fraud the model missed. Costs money.

**False positive (FP)** - A legitimate transaction the model flagged. Costs customer trust and support time.

**False positive rate (FPR)** - FP / all legitimate transactions. The x-axis of a ROC curve.

**Feature** - An input column the model uses (Time, Amount, V1-V28).

**Feature importance** - How much each feature contributes to a model's predictions. Says nothing about cause.

**Isolation Forest** - An unsupervised model that randomly splits the data; points that get isolated in few splits are anomalies.

**Local Outlier Factor (LOF)** - An unsupervised model that compares how dense a point's neighborhood is to its neighbors' neighborhoods.

**Logistic regression** - A simple linear model that outputs a probability. A good, explainable baseline.

**Model card** - A short document that says what a model does, how well, on what data, and where it should not be trusted.

**Overfitting** - The model memorizes training data and does worse on new data.

**PCA (principal component analysis)** - Rotates the data onto new axes ordered by how much variation they hold. V1-V28 are PCA outputs.

**Pipeline** - A scikit-learn object that chains preprocessing and the model, so the same steps run in training and in production.

**Precision** - Of the transactions we flagged, how many were really fraud? TP / (TP + FP).

**PR-AUC / average precision** - Area under the precision-recall curve. The headline metric for this project. A random model scores about the fraud rate (~0.0017).

**Random forest** - Many decision trees trained on random samples of the data, voting together.

**Recall (sensitivity, true positive rate)** - Of the real frauds, how many did we catch? TP / (TP + FN).

**ROC-AUC** - Area under the ROC curve (recall vs. FPR). The chance a random fraud scores higher than a random legitimate transaction. Can look flattering on imbalanced data.

**SMOTE** - Creates synthetic fraud examples by interpolating between real ones. Only ever applied to training data.

**Stratified split** - A train/test split that keeps the same fraud rate in both parts.

**Supervised learning** - Learning from labeled examples.

**Test set** - Data held back until the very end to give an honest final score.

**Threshold** - The score cut-off above which we flag a transaction as fraud. 0.5 is a default, not a rule.

**True negative (TN)** - A legitimate transaction correctly let through.

**True positive (TP)** - A fraud correctly flagged.

**Undersampling** - Throwing away some majority-class rows to balance the training data.

**Unsupervised learning** - Finding structure (groups, outliers) without labels.

**Validation set** - Part of the training data used to make choices (model, threshold) so the test set stays untouched.
