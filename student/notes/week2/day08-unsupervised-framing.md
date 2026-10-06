# Day 8 notes: Unsupervised framing

Assignment: `assignments/week2/day08-unsupervised-framing/` · Branch: `day08-unsupervised-framing`

## Learning objectives
By the end of this lesson you should be able to:
- Explain why a fraud team would want a model that does not need labels
- Describe clustering and distance-based outlier detection in plain words
- Explain the core assumption behind anomaly detection, and when it fails
- Use PCA and nearest-neighbor distances to explore the data **without** looking at the label
- Explain why the PCA features in this dataset suit distance-based methods

# Part 1: Lesson

## Why this day matters
Everything so far depended on the `Class` column. In real life labels are **late** (a chargeback can take weeks), **incomplete** (some fraud is never reported), and **backward-looking** (they only describe fraud that has already happened). Today you put the label away and ask: *can we find suspicious transactions just by what "normal" looks like?*

## The concepts

### 1. The rules for today
Pretend `Class` does not exist. Drop it at the start:
```python
X = df.drop(columns="Class")
```
Do not look at it, color plots by it, or use it to choose anything. It comes back on Day 10. This discipline is the point of the exercise: in production, an unsupervised model really does not have it.

(One practical exception: use the same train/test split as Days 4-7, so that Day 10's comparison uses the same test rows. Splitting by row indices is not using the label for modeling.)

### 2. The core assumption
Anomaly detection assumes:
1. most transactions are normal, and normal transactions resemble each other;
2. fraud is **rare** and **different**.

It fails when fraud is designed to look normal (a fraudster who mimics the cardholder) or when lots of legitimate behavior is unusual (a customer on holiday, a one-off large purchase). That is why "anomalous" and "fraudulent" overlap but are not the same set. Keep this distinction in every sentence you write today.

### 3. Clustering intuition
**Clustering** groups points that are close to each other. **k-means** is the simplest: pick k centers, assign each point to its nearest center, move each center to the middle of its points, repeat.

How it relates to outliers: a point **far from every cluster center** does not fit any normal group. Distance to the nearest center is a crude anomaly score.

Limitations: you must choose k; k-means assumes round, similar-sized clusters; it uses every point, outliers included, to place the centers.

### 4. Distance-based outlier reasoning
A more direct idea: **how far is a point from its nearest neighbors?**
- For each transaction, find its k nearest neighbors (`sklearn.neighbors.NearestNeighbors`).
- Its anomaly score = distance to the k-th neighbor (or the average of the k distances).
- Normal transactions live in crowded areas, so their neighbors are close. Isolated transactions have distant neighbors.

**Local Outlier Factor (LOF)** refines this by comparing a point's neighborhood density with its neighbors' density. It is good when normal data has both dense and sparse regions.

Computation: nearest-neighbor search on 284k points in 30 dimensions is slow. **Work on a random sample** (e.g. 20,000-50,000 rows) for exploration today.

### 5. Why this fits the PCA features
- Distance needs comparable scales. V1-V28 are centered around zero and already uncorrelated, which suits Euclidean distance.
- Amount and Time are not on the same scale and will dominate unless scaled. Use the same treatment as Day 4 (fit on train).
- PCA puts the most variation in the first components. Points that are extreme on *any* component stand out in distance terms.
- The same property that hurt explanation on Day 6 helps here: you do not need to know what V14 means to notice that a transaction is far from everyone else.

### 6. Seeing it: 2D projections
You cannot plot 30 dimensions, but you can:
- plot two V features against each other (e.g. V1 vs. V2) for a sample,
- run PCA again on your scaled features to get 2 components and scatter those,
- color the points by **your anomaly score** (not by the label). Do the high-score points sit at the edges?

Remember: a 2D plot hides most of the structure. A point can look central in 2D and still be far away in 30D.

### 7. The question of "how many to flag?"
Without labels, you must decide what share of transactions to call anomalous. Options: a fixed share (e.g. the top 0.1% or 0.5%), a share matching your analysts' capacity, or a natural "elbow" in the sorted scores. Think about this today; you will set it on Day 9.

## Summary
- Labels are late, incomplete and backward-looking, so an unsupervised model is a useful complement.
- Today the label is hidden. Using it would defeat the point.
- Anomaly detection assumes fraud is rare and different. When fraud mimics normal behavior, it fails.
- Clustering (distance to the nearest center) and nearest-neighbor distance are simple anomaly scores.
- PCA features suit distance methods; Amount and Time must be scaled.
- Unusual ≠ fraud. The flagged set will include odd but honest customers.

## Check your understanding
1. Name three reasons fraud labels are imperfect in practice.
2. What are the two assumptions behind anomaly detection?
3. Describe a fraud that anomaly detection would miss, and an honest transaction it would flag.
4. Why does k-means need you to choose k, and why is that awkward here?
5. Why must Amount be scaled before computing distances?

# Part 2: How to attempt each task

Create `notebooks/day08_unsupervised.ipynb` (or a notebook in the assignment folder).

### Task 1. Set up without the label
1. Load the data, use your Day 4 split, and **drop `Class`** from the features straight away. Keep `y_train`/`y_test` in variables you do not touch today.
2. Apply your Day 4 scaling (fit on train).
3. Take a random sample of the training features (e.g. 30,000 rows, `random_state=42`) for the slower steps.

### Task 2. Look at the shape of normal
1. Scatter two V features against each other for the sample. Takeaway: where is the dense core?
2. PCA to 2 components on the sample; scatter. Takeaway.

### Task 3. A simple distance-based score
1. `NearestNeighbors(n_neighbors=k)` with k around 5-20, fit on the sample.
2. Score = distance to the k-th neighbor.
3. Histogram of scores (log scale probably helps). Is there a long tail?
4. Re-draw the 2D plot colored by this score. Do the high scores sit at the edges?
5. Look at the 10 highest-scoring transactions: what do their Amount and Time look like?

### Task 4 (optional). Clustering view
k-means with a few values of k (e.g. 3, 5, 8). Score = distance to the nearest center. Do the two methods agree on the top outliers? (Compare the overlap of their top 1%.)

### Task 5. The written explanation
In `submission.md`, answer in your own words:
1. Why would a fraud team want a model that does not use labels? (Use the three label problems.)
2. How does distance-based outlier detection work? Explain it to a non-technical colleague.
3. Why do the PCA features suit this approach, and why did you need to scale Amount/Time?
4. What kinds of fraud will this miss, and what kinds of honest transactions will it flag?
5. How would you decide how many transactions to flag, without labels?
6. What did your exploration show? 3-5 observations with references to plots.

## Common mistakes
- Peeking at the label ("let me just check if the outliers are fraud"). Wait for Day 10.
- Computing distances on unscaled Amount.
- Running nearest neighbors on all 284k rows and waiting forever. Sample.
- Writing "the anomalies are the frauds". They are candidates.
- Over-trusting a 2D plot.

## Self-check before the PR
- [ ] `Class` dropped at the top and never used
- [ ] Scaling applied (fit on train)
- [ ] At least one anomaly score computed and visualized, with takeaways
- [ ] Written explanation covers why, how, fit with PCA, and limits
- [ ] Branch `day08-unsupervised-framing`, PR opened

## Going further (optional)
Try k = 5, 20 and 50 for the neighbor score. How much does the list of top-100 outliers change? A method whose results depend heavily on an arbitrary setting needs care in production.
