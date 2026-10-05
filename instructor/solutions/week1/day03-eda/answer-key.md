# Day 3 answer key

Figures are from the public Kaggle dataset; verify against the student's file.

1. 492 / 284,807 = **about 0.173%** fraud (about 1 in 580). Always-"not fraud" accuracy = 284,315 / 284,807 = **99.83%**.
2. Any two of: (a) severe imbalance -> use a **stratified** split so the test set has frauds; (b) Amount is heavily skewed and Time is a raw counter -> scale/transform them (V1-V28 already PCA output); (c) duplicate rows (~1,000) -> decide whether to drop them before splitting so they cannot land in both train and test; (d) whether to resample or tune thresholds.
3. Amount is right-skewed (median well below mean, long tail to ~25,700). Fraud transactions tend to be *smaller* in the public data. What it does not prove: the pattern comes from only 492 frauds, and it describes this data, not all fraud. Amount alone cannot separate the classes.
4. `Time` = seconds since the first transaction in the dataset, covering about 2 days; it is not a time of day. By hour, legit volume falls overnight while fraud is steadier, so the fraud *share* rises at night. Only 2 days of data, so treat as a hint.
5. Off-diagonal correlations among V1-V28 are near zero because PCA components are uncorrelated by construction. A few features (V17, V14, V12, V10 on the public data) correlate most with Class. Cannot: interpret what any V feature means in business terms, so explanations to stakeholders are limited.
6. Open-ended. A strong answer lists concrete costs for each side (missed fraud: lost amount, chargeback and investigation cost, trust; false alarm: declined card, support call, customer churn), says which is worse *and under what conditions*, and gives labelled assumptions, e.g. "missed fraud ~ average fraud amount plus a fee; false alarm ~ a few dollars of support cost plus churn risk".

**Red flags:** drops duplicates or scales columns on Day 3; calls correlated features "causes"; reads Time as time of day; business framing written as "maximize F1".
