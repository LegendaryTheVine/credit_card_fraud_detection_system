# Day 3: Project kickoff: EDA

**Week 1** · 90-120 minutes · First hands-on day. Student drives the keyboard; instructor navigates.

## Goal for the session
The student loads the Kaggle dataset, explores it with a purpose (not a tour of every plot), and writes the business framing in their own words: cost of a missed fraud vs. cost of a false alarm.

## Before the session
- Student's Day 1-2 PRs reviewed and merged (or at least feedback given).
- Student has the environment installed and `data/creditcard.csv` in place. If not, spend the first 15 minutes fixing that.
- Numbers quoted below are what the public dataset is known to contain; **confirm them against the student's actual file** during the session and correct this plan if they differ.

## Session outline
| Time | Segment |
|---|---|
| 0-10 | Review Day 2 feedback; recap why accuracy fails |
| 10-25 | Load the data; first look (shape, dtypes, nulls, duplicates) |
| 25-45 | Class balance |
| 45-70 | Amount and Time distributions, split by class |
| 70-90 | Correlation structure of V1-V28 |
| 90-110 | Business framing written in the student's own words |
| 110-120 | Assignment handoff |

## Teaching stance
EDA here means asking questions that change a later decision. For each plot, ask the student: **"What would you do differently because of this?"** Every finding should connect forward: stratified split and resampling (Day 4), scaling Amount/Time (Day 4), thresholds (Day 7), unsupervised assumptions (Day 8).

## 1. Load and first look (15 min)
Student runs, narrating what they expect first:
- `df.shape` -> about 284,807 rows, 31 columns (Time, V1-V28, Amount, Class)
- `df.dtypes`, `df.isna().sum()` -> all numeric, no missing values
- `df.duplicated().sum()` -> the public dataset has about 1,000 duplicate rows. Discuss: are duplicates real repeated transactions or errors? Do not drop them silently; leave the decision to Day 4 and have the student note it.

## 2. Class balance (20 min)
- `df["Class"].value_counts()` and `value_counts(normalize=True)` -> about 284,315 vs. 492, a fraud rate near 0.17%.
- Plot it, then notice that a bar chart makes the fraud bar invisible. Ask the student to find a better way to show it (log scale, or just state the ratio: roughly 1 fraud per 580 transactions).
- Connect to Day 2: what does the always-"not fraud" model score? (99.83%.)
- Forward link: a random split could give the test set very few frauds, or none. This is the reason for the **stratified split** on Day 4.

## 3. Amount and Time (25 min)
**Amount**
- `df["Amount"].describe()`: heavily right-skewed: median far below the mean (public data: median about 22, mean about 88, max about 25,700).
- Histogram, then log-scale histogram (`np.log1p`). Discuss why skew matters for distance and linear models.
- Compare by class: `df.groupby("Class")["Amount"].describe()`. Public data shows fraud medians that are *smaller*, not larger. Ask: "Does that match your intuition? Why might fraudsters test a card with small amounts?" Caution the student not to over-read a pattern in 492 points.
**Time**
- It is seconds since the first transaction, spanning about 2 days (max about 172,800 s). It is not a clock time. Convert to hour-of-day (`(Time // 3600) % 24`) as an exploration aid.
- Plot transactions per hour by class. Legit volume dips at night; fraud is flatter, so the fraud share is higher at night. Discuss, with the caveat: only 2 days of data.
- Forward link: scaling (Day 4); whether raw Time is a sound feature to keep.

## 4. V1-V28 correlation structure (20 min)
- Correlation heatmap of V1-V28: close to zero off-diagonal, because PCA components are uncorrelated by construction. Ask the student what this tells them. (Day 2 payoff.)
- Then correlation of each feature with `Class` (sorted bar chart). A handful of V features (e.g. V17, V14, V12, V10 on the public data) correlate most with fraud. Frame as "which features separate fraud", not "which features cause fraud".
- Boxplots of one or two top features by class, to see the separation.
- Limitation: V1-V28 are anonymized, so we cannot say what V17 *means*. Plant this seed for Day 6.

## 5. Business framing in the student's own words (20 min)
Student writes, you do not dictate. Prompt questions:
- What does a missed fraud cost? (the transaction amount, chargeback fees, investigation time, customer trust)
- What does a false alarm cost? (declined card, support call, frozen account, a customer who stops using the card)
- Which is worse? It depends. Ask them to put a made-up but plausible number on each, labelled as an assumption. Day 7 uses these numbers for threshold tuning.
- What would success look like to a leader who is not technical?

## Assignment handoff
Walk through the student README. They finish the notebook and written framing on their own branch and open a PR.

## Common pitfalls
- Plotting everything and concluding nothing. Push each plot to a decision.
- Treating Time as clock time of day without noticing it is elapsed seconds.
- Reading too much into 492 fraud points (small-sample patterns).
- Dropping duplicates or scaling columns "just to be safe". Decisions belong to Day 4.
- Writing the business framing as ML language ("maximize F1") instead of money and customers.
- Calling correlated-with-Class features "causes of fraud".

## Expected deliverable
`notebooks/` or the Day 3 folder contains `eda.ipynb`, plus `submission.md` with findings and business framing. Reference: `instructor/solutions/week1/day03-eda/`. Rubric: `instructor/rubrics/day03-eda.md`.
