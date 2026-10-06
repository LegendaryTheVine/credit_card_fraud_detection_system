# Credit Card Fraud Detection: Student Workspace

Your workspace for the 3-week ML course. You will build a fraud detector end to end: business framing, a supervised model, an unsupervised anomaly detector, a comparison, and a demo.

## Setup
```
python -m venv .venv
.venv\Scripts\activate        # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```
Download the dataset as described in `data/README.md`.

## Layout
- `assignments/` - one folder per day: read its `README.md`, fill in `submission.md`
- `notes/` - teaching notes for every day: the lesson, then how to attempt each task. Start with `notes/README.md`
- `src/` - reusable code you grow over the course
- `notebooks/` - scratch exploration
- `app/` - the API and demo (Days 12-13)
- `docs/` - model card and presentation

## Workflow for every day
0. Read the day's teaching note in `notes/` before the session
1. `git checkout main && git pull`
2. `git checkout -b dayNN-name` (the branch name is given in each assignment README)
3. Do the work, commit often
4. `git push -u origin dayNN-name` and open a Pull Request to `main`
5. Fill in the PR template. Your instructor reviews, comments, and merges.
6. Pull `main` and start the next day.

Do not commit the dataset or trained model files.
