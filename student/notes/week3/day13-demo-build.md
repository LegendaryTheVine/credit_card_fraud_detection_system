# Day 13 notes: Building the demo

Assignment: `assignments/week3/day13-demo-build/` · Branch: `day13-demo-build` · Code goes in `app/`

## Learning objectives
By the end of this lesson you should be able to:
- Design a demo around the story you want to tell, not around the code
- Build a minimal web page that calls your API and shows the result
- Let a viewer pick real example transactions (fraud, legit, borderline) and see the score, the decision and the reasons
- Show the effect of the threshold interactively
- Make the demo reliable enough to run live, with a backup plan

# Part 1: Lesson

## Why this day matters
On Day 15 a non-technical audience will remember the demo more than any chart. A good demo makes the model **tangible**: "here is a transaction, here is what the model thinks, here is why, and here is what happens if we change the threshold". The goal is clarity and reliability, not visual polish.

## The concepts

### 1. Start from the story
Before writing code, write the 60-90 second script of what you will show. For example:
1. "Here is an ordinary purchase." → low score, approved.
2. "Here is a real fraud from the test set." → high score, flagged, with reasons.
3. "Here is a borderline case." → near the threshold. "This is why we need human review."
4. "If we lower the threshold..." → more caught, more false alarms.
5. (Optional) "Here is one only the anomaly detector caught." → links to Day 10.

Build only what this script needs.

### 2. Choosing the technology
Your requirements already include FastAPI, so the simplest option is **a single HTML page served by your API**:
- `app/static/index.html` with a little JavaScript that calls `/predict` using `fetch`,
- FastAPI serves it with `StaticFiles` or a route that returns the file.
No new dependencies, and the demo and API run with one command.

Alternatives: **Streamlit** or **Gradio** build a UI in pure Python but are new dependencies. Agree with your instructor first, and add them to `requirements.txt` if used.

### 3. Getting example transactions
Typing 30 numbers by hand is not a demo. Instead:
- Prepare a small file of hand-picked test transactions, e.g. `app/samples/examples.json`: a few obvious legit, a few caught frauds, a borderline case, a missed fraud, a false alarm. Label each with a short human description.
- Or add an endpoint such as `GET /examples` that returns them, and `GET /examples/{id}`.
- Let the user pick one from a dropdown, optionally edit the Amount, and press "Score".

Only commit a handful of rows, never the dataset.

### 4. What to show for each transaction
- **Score** as a number and a bar or gauge, with the **threshold** marked on it.
- **Decision**: approve / flag for review, in plain words and color (and not color alone, for accessibility).
- **True label** when it is a test example ("this was actually fraud"), so the audience sees right and wrong cases.
- **Reasons**: the top 3-5 contributing features (from Day 11), with an honest note that V-features are anonymized.
- Optional: the **anomaly score** next to the supervised score.

### 5. Making the threshold interactive
A slider for the threshold that re-applies it to the current score (no new API call needed) shows the trade-off instantly. Even better, show what that threshold means on the whole test set: precision, recall and alerts per 100,000 transactions. Precompute those per threshold in a small JSON file (from your Day 7 code) so the page can look them up.

### 6. Reliability
Live demos fail at the worst moment. Protect yourself:
- one command to start everything, written in `app/README.md`,
- the model loads at startup with a clear error if missing,
- example transactions are bundled, not fetched from the internet,
- you have **screenshots or a short screen recording** as a fallback,
- you have rehearsed it at least twice from a fresh terminal.

## Summary
- Write the demo script first; build only what it needs.
- The simplest stack: a static HTML page served by your FastAPI app, calling `/predict`.
- Use curated real examples, not typed numbers.
- Show score, threshold, decision, truth and reasons; make the threshold a slider.
- Rehearse, and keep a recorded fallback.

## Check your understanding
1. Why build from a demo script rather than from features?
2. Why is a dropdown of curated examples better than 30 input boxes?
3. What does a threshold slider teach the audience?
4. Why show the true label for test examples?
5. What is your plan if the demo crashes during the presentation?

# Part 2: How to attempt each task

### Task 1. Write the demo script
5-7 steps, in `submission.md` first. This is your spec.

### Task 2. Curate example transactions
1. From the test set and your Day 10/11 analysis, pick 5-8 transactions that tell the story (legit, caught fraud, borderline, false alarm, missed fraud, anomaly-only catch).
2. Save them with a short description and their true label to `app/samples/examples.json`.

### Task 3. Extend the API
1. `GET /examples` returning the curated list.
2. If you want reasons in the UI, extend `/predict` to return the top contributing features.
3. Serve the page: mount `app/static/` with `fastapi.staticfiles.StaticFiles`, or add a `GET /` route returning `index.html`.

### Task 4. Build the page
A minimal layout:
- a dropdown of examples and a "Score" button,
- a results panel: score bar with threshold marker, decision, true label, reasons,
- a threshold slider showing precision/recall/alerts at that threshold.
Keep the HTML/JS small and readable; plain JavaScript `fetch` is enough.

### Task 5. Rehearse and document
1. Start from a fresh terminal using only the README instructions.
2. Run through the script twice; time it.
3. Take screenshots or a short recording of each step as a backup.
4. Update `app/README.md` with how to start the demo.

### `submission.md` (suggested structure)
- **Demo script**
- **How to run it**
- **Screenshots** (or links to them)
- **What I would improve with more time**

## Common mistakes
- Building features the story does not need.
- A form with 30 empty number boxes.
- Showing only cases the model gets right. The interesting moments are the borderline and wrong ones.
- No fallback when something breaks.
- Committing large data files for the demo.

## Self-check before the PR
- [ ] Demo starts with one documented command
- [ ] Curated examples load; scoring works for each
- [ ] Score, threshold, decision, truth and reasons are visible
- [ ] Threshold slider works
- [ ] Screenshots or recording saved as a backup
- [ ] Branch `day13-demo-build`, PR opened

## Going further (optional)
Add a "simulate a stream" button that scores 100 random test transactions one after another and shows a running count of alerts and catches. It makes "real-time scoring" concrete.
