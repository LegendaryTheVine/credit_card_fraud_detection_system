# Study notes

Teaching notes for the 3-week fraud detection course. There is one note per day, in the same order as `assignments/`. Each note has two parts:

- **Part 1: Lesson.** Learning objectives, why the day matters, the concepts explained with examples, a summary, and "check your understanding" questions.
- **Part 2: How to attempt each task.** For every task and question in the assignment: what it is asking for, a step-by-step approach, hints, common mistakes, and a self-check to run before you open your PR.

The notes show you how to get to an answer. They do not give you the answer. Your submission should be in your own words, with your own numbers, from your own code.

## How to use these notes
1. **Before the session:** study Part 1 (20-30 minutes). Try the "check your understanding" questions without looking.
2. **During the session:** keep it open. Write your questions in your own notes, not in this folder.
3. **When you do the assignment:** work through Part 2 with the assignment `README.md` open beside it.
4. **Before you open the PR:** go through the "Self-check" list. If you cannot tick an item, fix it or say why in the PR.

## Index
Start here: [00 - Setup and workflow](00-setup-and-workflow.md) · [Glossary](glossary.md)

**Week 1: Foundations and data**
| Day | Note | You will produce |
|---|---|---|
| 1 | [Framing the problem](week1/day01-framing.md) | Written answers, no code |
| 2 | [Statistics for imbalanced problems](week1/day02-imbalance-stats.md) | Calculations by hand |
| 3 | [EDA](week1/day03-eda.md) | `eda.ipynb` + business framing |
| 4 | [Data preparation](week1/day04-data-prep.md) | Split and scaling code in `src/` |
| 5 | [Supervised baseline](week1/day05-baseline.md) | Logistic regression + raw predictions |

**Week 2: Models and evaluation**
| Day | Note | You will produce |
|---|---|---|
| 6 | [Better supervised model](week2/day06-better-model.md) | Random forest / boosting + feature importance |
| 7 | [Evaluation, done right](week2/day07-evaluation.md) | Cost-based threshold choice |
| 8 | [Unsupervised framing](week2/day08-unsupervised-framing.md) | Short write-up + exploratory notebook |
| 9 | [Isolation Forest](week2/day09-isolation-forest.md) | Anomaly score for every transaction |
| 10 | [Supervised vs. unsupervised](week2/day10-supervised-vs-unsupervised.md) | Comparison notebook + thesis |

**Week 3: Responsible AI, product, and story**
| Day | Note | You will produce |
|---|---|---|
| 11 | [Responsible AI](week3/day11-responsible-ai.md) | First draft of `docs/model_card.md` |
| 12 | [Packaging](week3/day12-packaging.md) | A working API in `app/` |
| 13 | [Demo build](week3/day13-demo-build.md) | A clickable demo |
| 14 | [Docs and presentation prep](week3/day14-docs-and-presentation-prep.md) | Final model card + slide draft |
| 15 | [Final presentation](week3/day15-final-presentation.md) | The presentation |

## The thread that runs through the course
Every day builds on the one before. If you understand these five sentences, you understand the course:
1. Fraud is **rare** (about 1 in 580 transactions), so accuracy is a useless score and you need precision, recall and PR-AUC.
2. The two mistakes, **missing a fraud** and **blocking a real customer**, have different costs, and the business decides how to trade them off.
3. A **supervised** model learns known fraud from labels; an **unsupervised** model flags anything unusual without labels. They answer different questions.
4. The **threshold** turns a score into a decision. Choosing it is a business decision, made with numbers.
5. A model is only useful if someone can **trust, run and explain** it, so the model card, API and presentation matter as much as the score.

## Rules that apply every day
- Never commit `data/creditcard.csv` or model files (`*.pkl`, `*.joblib`). They are gitignored; keep it that way.
- Never look at the test set to make a decision (choosing features, thresholds, or models). The test set is for the final score only.
- Every notebook must run top to bottom on a fresh kernel (`Kernel > Restart & Run All`).
- Every plot gets a one-line takeaway underneath it: what you see, and what you will do because of it.
- Use `random_state=42` (or another fixed number) everywhere randomness appears, so your results can be reproduced.
