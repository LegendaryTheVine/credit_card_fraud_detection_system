# Day 3 notes: Project kickoff: exploratory data analysis (EDA)

Assignment: `assignments/week1/day03-eda/` · Branch: `day03-eda` · Notebook: `eda.ipynb`

## Learning objectives
By the end of this lesson you should be able to:
- Load the dataset and run a disciplined first inspection (shape, types, missing values, duplicates)
- Show a severe class imbalance in a way that a reader can actually see
- Explore a skewed money column, and know why log scales help
- Explain what the `Time` column really measures, and derive hour-of-day from it
- Read a correlation heatmap and a feature-vs-label correlation chart without confusing correlation with cause
- Turn every finding into a decision for a later day
- Write the business framing of fraud in money and customer terms

# Part 1: Lesson

## Why this day matters
EDA is not "make lots of plots". It is asking questions of the data whose answers **change what you do next**. Every finding today should point forward: how you split the data (Day 4), how you scale it (Day 4), how you judge models (Day 7), and what the unsupervised models assume (Day 8). The test for every plot: *"What will I do differently because of this?"*

## The concepts

### 1. Meet the dataset
The data is two days of European card transactions from September 2013, published by the ULB Machine Learning Group.

| Column | What it is |
|---|---|
| `Time` | Seconds elapsed since the first transaction in the file |
| `V1` ... `V28` | 28 anonymized features: the output of PCA on the bank's original (confidential) features |
| `Amount` | Transaction amount (in euros) |
| `Class` | The label: 1 = fraud, 0 = legitimate |

Two things are unusual about this dataset compared with real life: you cannot see the original features (merchant, country, card type...), and two days is a very short window. Keep both in mind whenever you draw a conclusion.

### 2. The first look: a checklist
Before any plot, answer four questions. They take a minute and catch most data problems.

```python
df.shape                 # how many rows and columns?
df.info()                # column types; are they all numeric?
df.isna().sum()          # missing values per column
df.duplicated().sum()    # fully identical rows
```

**Duplicates deserve thought, not a reflex.** An identical row could be a data error, or two genuinely identical transactions (same amount, same second, same features). Look at a few with `df[df.duplicated(keep=False)].head()` and check whether any are fraud. Today you *note* what you find. Whether to drop them is a Day 4 decision, and you must justify it.

### 3. Showing class imbalance
`df["Class"].value_counts()` gives counts; `value_counts(normalize=True)` gives shares. When one class is 0.17%, a plain bar chart shows one tall bar and something you cannot see. Ways to make the small class visible:
- a log-scale y axis (`ax.set_yscale("log")`)
- writing the ratio in words ("about 1 fraud in every N transactions")
- annotating the bars with their counts

Ask what the imbalance means for later. What happens to the number of frauds in a test set if you split the data randomly and you are unlucky?

### 4. Skewed distributions and log scales
Money is almost always **right-skewed**: many small values, a few huge ones. Signs of skew in `describe()`: the mean is far above the median, and the max is many times the 75th percentile.

A normal histogram of a skewed column squashes everything into one bar on the left. Two fixes:
- `np.log1p(amount)`, i.e. log(1 + x), spreads out the small values and handles zeros safely (log(0) is undefined; log1p(0) = 0).
- Or keep the raw values and put the x axis on a log scale.

Why skew matters later: linear models and distance-based methods are pulled around by extreme values. That feeds into Day 4's scaling decision.

**Comparing groups.** `df.groupby("Class")["Amount"].describe()` gives the summary per class side by side. When comparing distributions of very different sizes (284k vs. 492), use `density=True` / `stat="density"` in histograms so the fraud distribution is not flattened by the much larger legit one.

**Small-sample caution.** Any pattern in the fraud class comes from only 492 rows, from two days, at one bank. A difference you see is a *hint*, not a law.

### 5. Understanding Time
Read the column definition again: seconds since the first transaction. It is **not** a clock time and **not** a date. Check its maximum and convert it to hours to see how long the data spans.

To look at daily rhythm you can derive an approximate hour of day:
```python
hour = (df["Time"] // 3600) % 24
```
This assumes the file starts at midnight, which we do not know for sure, so call it "hours since start, modulo 24" in your write-up.

Two useful views:
- **Volume per hour by class**: how many transactions in each hour, separately for fraud and legit.
- **Fraud share per hour**: `df.groupby(hour)["Class"].mean()`. Counts and rates can tell different stories. If legit traffic drops sharply at some hours and fraud does not, the *rate* changes even if the fraud *count* does not.

### 6. Correlation and its limits
**Correlation** (Pearson, −1 to +1) measures how much two columns move together in a straight line.
- `df[v_cols].corr()` + `sns.heatmap(...)` shows how the V features relate to each other. Before you plot it, predict what you will see given that V1-V28 come from PCA (Day 2). Then check.
- `df.corrwith(df["Class"])` (or `df.corr()["Class"]`), sorted, shows which features move most with the label. Sort by **absolute** value, since a strong negative relationship is as useful as a strong positive one.
- Then draw **boxplots by class** for the two features with the biggest difference, to see what the separation actually looks like.

Two cautions:
- Correlation with `Class` means the feature **separates** fraud from legit in this data. It does not mean the feature **causes** fraud.
- Pearson correlation only sees straight-line relationships. A feature can matter to a tree model while having low correlation.

### 7. Business framing
The second deliverable is not technical. You will turn the two error types from Day 1 into money and customer impact:
- **A missed fraud** costs the transaction amount, chargeback and handling fees, investigation time, and trust.
- **A false alarm** costs a declined purchase, a support call, possibly a frozen card, and sometimes a customer who stops using the card.

Putting a number on each is uncomfortable because you do not know the real values. That is fine: state your numbers as **assumptions** and give a reason for each ("I assume a false alarm costs about X because a support call costs roughly Y..."). On Day 7 you will plug these numbers into a cost calculation to choose a threshold, so pick numbers you can defend.

## Summary
- EDA = questions that change later decisions. Every plot gets a takeaway and a "so what".
- First look: shape, types, missing values, duplicates. Note duplicates; decide on Day 4.
- Severe imbalance needs a visible chart and leads directly to a stratified split.
- Amount is skewed: use log views and expect to scale it.
- Time is elapsed seconds over about two days, not a clock.
- V1-V28 are PCA outputs. Look at how they relate to each other and to `Class`, and remember correlation is not cause.
- Business costs are stated as labeled assumptions, in money and customers, not in ML terms.

## Check your understanding
1. Why is `np.log1p` safer than `np.log` for amounts?
2. Why use density rather than counts when comparing fraud and legit histograms?
3. Why might the fraud *rate* at an hour change even if the fraud *count* does not?
4. What does it mean that a feature is strongly negatively correlated with `Class`?
5. Name one reason a pattern in the fraud class might not hold next month.

# Part 2: How to attempt each task

Work in `eda.ipynb`. Keep the starter's section headings. Under every plot or table write a markdown cell: **"Takeaway: ... So what: ..."**

### Task 1. First look
1. Run the four checks from section 2 of the lesson, one per cell.
2. Write down: number of rows and columns, column types, missing values (yes/no and where), number of duplicate rows.
3. Investigate duplicates a little: how many involve fraud? Show a couple.
4. **Do not drop or change anything.** Write "Decision deferred to Day 4" and the question you will need to answer.

### Task 2. Class balance
1. Show counts and percentages (`value_counts()` and `value_counts(normalize=True)`).
2. Make a chart in which the fraud class is visible (log scale or annotations).
3. Write the ratio in words.
4. Takeaway: what this means for splitting the data and for judging models.

### Task 3. Amount
1. `df["Amount"].describe()`; note mean vs. median vs. max.
2. Histogram of raw Amount, then of `np.log1p(Amount)`. Explain in one line what the log view shows that the raw one hides.
3. Compare by class: `groupby("Class")["Amount"].describe()` and overlaid density histograms (or boxplots) on the log scale.
4. Takeaway: what differs between fraud and legit, and the small-sample caveat.

### Task 4. Time
1. Write one sentence on what `Time` measures. Check the max and convert it to hours or days.
2. Create the hour feature in a **new variable**, not by overwriting `Time`.
3. Plot transactions per hour separately for each class (two subplots, or normalize each class so the shapes are comparable).
4. Optionally plot the fraud rate per hour.
5. Takeaway, with the caveat that there are only two days of data.

### Task 5. V1-V28
1. Correlation heatmap of V1-V28 only. Use a diverging colormap centered at 0 (`cmap="coolwarm", center=0`). Write what you predicted, then what you saw.
2. Correlation of every feature with `Class`, sorted by absolute value, as a horizontal bar chart.
3. Boxplots by class of the two most different features. You may want `showfliers=False` or a clipped y-axis so the boxes are readable.
4. Takeaway: which features separate the classes, and what you *cannot* say about them.

### Submission questions
| Q | How to attempt it |
|---|---|
| 1. Fraud rate and "always not fraud" accuracy | Take the numbers from Task 2. Show the calculation as on Day 2. |
| 2. Two things that affect Day 4 | Pick two findings from Tasks 1-5. For each: the finding, then the preparation decision it forces, then why. |
| 3. Amount, and what it does not prove | What you saw, then the limits: sample size, two days, one bank, correlation vs. cause. |
| 4. Time and the hourly pattern | One sentence on what Time is, then what the hourly plots showed, then a caveat. |
| 5. Correlation structure of V1-V28 | Describe the heatmap, explain *why* it looks like that (link to PCA from Day 2), and say what anonymization stops you from doing. |
| 6. Business framing | No ML words. Fill in the three headings. Every number labeled "assumption" with a one-line reason. |

## Common mistakes
- Plotting everything and concluding nothing.
- Treating Time as the time of day without noticing it is elapsed seconds.
- Over-reading patterns from 492 fraud rows.
- Dropping duplicates or scaling columns "to be safe". Those decisions belong to Day 4.
- Calling a correlated feature a "cause of fraud".
- Business framing that says "maximize F1" instead of talking about money and customers.
- Committing the CSV. Check `git status`.

## Self-check before the PR
- [ ] `Restart & Run All` works with no errors
- [ ] Every plot has a takeaway and a "so what"
- [ ] Nothing in the data was dropped or changed
- [ ] All six questions answered; Q6 numbers labeled as assumptions
- [ ] `data/creditcard.csv` is not in the commit
- [ ] Branch `day03-eda`, PR opened

## Going further (optional)
Plot `Amount` against one of the top V features, colored by class (sample the legit rows so the plot is readable). Do frauds sit in a region of their own? This is a preview of how a model "sees" the data.
