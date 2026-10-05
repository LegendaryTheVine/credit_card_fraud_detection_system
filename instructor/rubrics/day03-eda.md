# Rubric: Day 3 - EDA

Score each criterion 0-2. **Pass: 11+ of 14 and no 0 on criteria 1, 5 or 6.** Otherwise: Revise.

| # | Criterion | 2 = meets | 1 = partial | 0 = missing |
|---|---|---|---|---|
| 1 | Class balance (Q1) | Correct rate (~0.17%), 99.83% baseline accuracy, small class made visible in the plot | Numbers right, plot hides fraud class | Wrong or missing |
| 2 | First look discipline | Reports shape, types, nulls, duplicates; changes nothing | Reports but alters data | Skipped |
| 3 | Amount analysis (Q3) | Skew shown (raw + log), compared by class, notes small-sample caution | Plots without interpretation | Missing |
| 4 | Time understanding (Q4) | States Time is elapsed seconds; hourly plot by class with takeaway | Plot but treats Time as clock time | Missing |
| 5 | V1-V28 (Q5) | Explains near-zero correlations (PCA), shows correlation with Class, notes interpretability limit | Heatmap without explanation | Missing |
| 6 | Business framing (Q6) | Own words; costs on both sides; says which is worse and when; labelled assumed numbers; no ML jargon | One side only, or no numbers | Missing or jargon only |
| 7 | Process and notebook hygiene | Runs top to bottom, takeaway under every plot, dataset not committed, PR template filled, Q2 links findings to Day 4 | Minor gaps | Notebook broken or data committed |

**Common errors:** plotting everything and concluding nothing; claiming correlated features cause fraud; premature cleaning.
