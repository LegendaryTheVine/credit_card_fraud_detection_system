# 00: Setup and workflow

Read this once before Day 1, and come back to it whenever git or your environment gets in the way.

## 1. Environment
From the root of your repo:
```
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
```
Check it worked:
```
python -c "import pandas, sklearn, imblearn, fastapi; print('ok')"
```
If you use VS Code or Jupyter, select the `.venv` interpreter / kernel. A very common problem is "it works in the terminal but not in the notebook", which almost always means the notebook uses a different Python.

## 2. The dataset
Follow `data/README.md`. When you are done, the file must be at `data/creditcard.csv`. Check it:
```
python -c "from src.data import load_data; df = load_data(); print(df.shape)"
```
Run that from the repo root. You should see 31 columns. If you get `FileNotFoundError`, the file is in the wrong folder or has a different name.

**Loading from a notebook.** Notebooks run from their own folder, so relative paths break easily. Two options:
- Use a relative path that matches where the notebook lives (the Day 3 starter does this: `../../../data/creditcard.csv`).
- Or reuse `src/data.py`, which always finds the file:
  ```python
  import sys
  from pathlib import Path
  sys.path.append(str(Path.cwd().parents[2]))   # go up to the repo root; adjust the number to your folder depth
  from src.data import load_data
  df = load_data()
  ```

The file is about 150 MB. Load it once at the top of a notebook and reuse `df`.

## 3. The daily git loop
Each day has its own branch. The name is in the assignment README.
```
git checkout main
git pull
git checkout -b day04-data-prep
# ... work ...
git add <files>
git commit -m "Day 4: stratified split and scaling"
git push -u origin day04-data-prep
```
Then open a Pull Request into `main` on GitHub and fill in the template.

Tips:
- Commit small and often, with messages that say what changed ("Add class balance plot"), not "update".
- Run `git status` before every commit. If you see `creditcard.csv` or a `.joblib` file, stop: do not add it.
- If yesterday's PR is not merged yet and today needs its code, branch from yesterday's branch instead of `main` and say so in the PR.

## 4. Writing a good submission
Each `submission.md` is graded on reasoning, not length.
- Answer every question under its heading.
- Lead with the answer, then the reason. "Accuracy is misleading here because ..." beats three paragraphs of build-up.
- Show numbers and say where they came from (which notebook cell, which split).
- Write for a smart non-technical reader. If your head of fraud could not follow it, rewrite it.
- If you are unsure, say what you think and why. "I'm not sure, but I think X because Y" is a good answer to discuss.

## 5. Notebook hygiene
- Imports and data loading at the top.
- A markdown heading for each task, matching the assignment numbering.
- A one-line takeaway under every plot and table.
- Before committing: `Kernel > Restart & Run All`. If anything fails, fix it.
- Code you will reuse on later days (loading, splitting, scaling, metrics) goes into `src/`, not copy-pasted between notebooks.

## 6. Where the code lives
| File | What goes in it | First used |
|---|---|---|
| `src/data.py` | Loading, train/test split | Day 3-4 |
| `src/features.py` | Scaling and feature preparation | Day 4 |
| `src/models.py` | Training functions for each model | Day 5 |
| `src/evaluate.py` | Metrics, curves, threshold and cost functions | Day 7 |
| `app/` | API and demo | Day 12-13 |
| `docs/` | Model card, presentation | Day 11-15 |

## 7. When you are stuck
1. Read the error message from the bottom up. The last line says what went wrong; the lines above say where.
2. Print shapes and a few rows (`X.shape`, `y.value_counts()`, `df.head()`). Most bugs are "the data is not what I think it is".
3. Write the blocker in the `## Notes` section of the assignment README and in the PR. A clear question is a good contribution.
