# Day 3: Project kickoff: EDA

**Week 1** · Branch name to use: `day03-eda`

## Objective
Load the Kaggle dataset, explore it with a purpose, and write the business framing for fraud detection in your own words.

## Before you start
- `data/creditcard.csv` is in place (see `data/README.md`) and your environment is installed.
- Use the starter notebook `eda.ipynb` in this folder. Put any reusable loading code in `src/data.py`.

## Tasks (in `eda.ipynb`)
1. **First look:** shape, column types, missing values, duplicate rows. Note what you find. Do **not** drop or change anything yet.
2. **Class balance:** counts and percentages of fraud vs. not fraud. Show it in a way that makes the small class visible.
3. **Amount:** summary statistics, a histogram, and a log-scale version. Compare Amount for fraud vs. not fraud.
4. **Time:** state in one sentence what `Time` actually measures. Plot transactions per hour of the day by class.
5. **V1-V28:** a correlation heatmap; each feature's correlation with `Class`; boxplots by class for the two features that look most different.

## Questions (answer in `submission.md`)
1. What is the fraud rate? What accuracy would a model that always predicts "not fraud" get?
2. Name two things in the data that affect how you will split or prepare it on Day 4, and say why.
3. What did you learn about Amount? What does the pattern *not* prove?
4. What does `Time` measure, and what did you see by hour?
5. What does the correlation structure of V1-V28 look like, and why? What can you not do with these features?
6. **Business framing (your own words, no ML jargon):** what does a missed fraud cost? What does a false alarm cost? Which is worse, and what number (clearly labelled as an assumption) would you put on each?

## Done when
- [ ] `eda.ipynb` runs top to bottom on a clean kernel
- [ ] Every plot has a one-line takeaway beneath it
- [ ] `submission.md` answers all six questions
- [ ] Work is committed on branch `day03-eda`; the dataset is **not** committed
- [ ] PR opened using the pull request template

## Notes
_Write questions or blockers for your instructor here._
