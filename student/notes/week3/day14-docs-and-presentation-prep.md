# Day 14 notes: Documentation and presentation prep

Assignment: `assignments/week3/day14-docs-and-presentation-prep/` · Branch: `day14-docs-and-presentation-prep` · Deliverables in `docs/`

## Learning objectives
By the end of this lesson you should be able to:
- Turn the model card draft into a final, reviewer-ready document
- Structure a short technical presentation for a non-technical leadership audience
- Choose the few numbers and charts that carry the story
- Explain what a production fraud system needs beyond the model: real-time scoring, drift monitoring, a human review queue
- Anticipate the hard questions and prepare honest answers

# Part 1: Lesson

## Why this day matters
Leaders do not read notebooks. What they see is the model card and the presentation. If the work is good but the story is unclear, the decision will go the wrong way. Today you turn three weeks of work into something a decision-maker can act on.

## The concepts

### 1. Finalizing the model card
Revisit your Day 11 draft with fresh eyes:
- **Consistency:** every number matches your final model and threshold (Days 7, 10, 12). Check each one against its notebook.
- **Specificity:** replace vague words ("good performance", "some limitations") with numbers and concrete cases.
- **Audience:** a risk manager or auditor should understand every sentence. Define any technical term once.
- **Honesty:** limitations are clear and prominent, not buried.
- **Traceability:** say which data, split and code produced each number, and the model version from the API.

### 2. The shape of a leadership presentation
Use the outline in `docs/presentation-outline.md`. A good rule is **one idea per slide**, with a headline that *states the point* ("The model catches about X% of fraud while flagging Y in 1,000 transactions"), not a topic label ("Results").

| Section | Purpose | Typical length |
|---|---|---|
| Problem and business framing | Why this matters in money and customers; the two costs | 1-2 slides |
| Approach | Supervised and unsupervised, in one sentence each, and why both | 1-2 slides |
| Results | The few numbers that matter; one chart | 2-3 slides |
| Demo | Live, following your Day 13 script | 3-5 minutes |
| Limitations | Honest and specific | 1 slide |
| Production next steps | What it would take to deploy | 1 slide |

Aim for about 10-15 minutes plus questions.

### 3. Choosing numbers and charts
Leadership remembers two or three numbers. Choose them deliberately:
- a **catch rate** (recall at your threshold),
- an **alert quality** figure (precision, or "1 in N alerts is real fraud"),
- a **money** figure (estimated cost vs. no model), clearly labeled as based on assumptions.

Good charts for this audience: the precision@k / recall@k table from Day 10 as a simple bar chart; the cost-vs-threshold curve from Day 7 with your choice marked. Avoid ROC curves, heatmaps and anything that needs a long explanation. Every chart needs a headline that says what to see.

Translate every metric: not "recall 0.82" but "we catch about 8 in 10 frauds".

### 4. What production would need
The model is maybe 10% of a production fraud system. Cover at least these three:
- **Real-time scoring:** the decision must be made during the payment, in milliseconds, with high availability and a fallback (e.g. rules) if the model is down.
- **Drift monitoring:** customer behavior and fraud tactics change. Monitor the input distributions, the score distribution, the alert rate, and (once labels arrive) precision and recall over time. Agree in advance on what triggers retraining.
- **Human review queue:** borderline and anomaly-only alerts go to analysts; their decisions become new labels; those labels retrain the model. Size the queue from your alert volumes.

Also worth a mention: retraining schedule, label delay, audit logs and model versioning, regulatory explainability requirements, A/B testing (or shadow mode) before full rollout, and using the bank's original (non-anonymized) features.

### 5. Preparing for questions
Write down the ten hardest questions you could be asked, and a short honest answer for each. Likely ones:
- "Why not just use rules?"
- "What happens with a fraud type you've never seen?"
- "How many customers will we annoy?"
- "Is it fair?"
- "How do we know it still works in six months?"
- "Why should we trust numbers from 2013 data?"
"I don't know, but here is how we would find out" is a strong answer.

## Summary
- Final model card: consistent numbers, specific, plain-spoken, honest, traceable.
- One idea per slide, with headlines that state the point.
- Two or three translated numbers and one or two simple charts carry the story.
- Production needs real-time scoring, drift monitoring and a human review loop, not just a model.
- Prepare the hard questions in advance.

## Check your understanding
1. What is the difference between a topic headline and a point headline?
2. Which three numbers would you choose to lead with, and why?
3. What is drift, and what would you monitor to detect it?
4. Why does a human review queue improve the model over time?
5. How would you answer "is it fair?" honestly?

# Part 2: How to attempt each task

### Task 1. Finalize `docs/model_card.md`
1. Re-read the Day 11 draft and your instructor's feedback.
2. Re-check every number against its source; add the model version and threshold.
3. Tighten language; define terms; make sure limitations and "where not to trust it" are specific.
4. Ask: could an auditor reproduce each claim from the repo?

### Task 2. Draft the presentation in `docs/`
1. Expand `docs/presentation-outline.md` into slide-by-slide notes: headline, the one visual or number, and what you will say (2-3 bullets).
2. Build the slides in the tool you prefer (PowerPoint, Google Slides, Markdown-based slides). Save a PDF or the source in `docs/` (keep the file size reasonable).
3. Export the charts you need from your notebooks as PNGs into `docs/img/`.

### Task 3. Production next steps slide
Cover real-time scoring, drift monitoring and the human review queue, each with one concrete detail from your project (e.g. expected alerts per day at your threshold → analyst capacity needed).

### Task 4. Q&A prep
List 8-10 hard questions with short answers in `submission.md` (or `docs/qa-prep.md`).

### Task 5. First rehearsal
Present once out loud, timed, including the demo. Note where you ran long or lost the thread, and fix it.

### `submission.md` (suggested structure)
- **What changed in the model card** since Day 11
- **Presentation structure:** one line per slide
- **The three headline numbers** and how each was computed
- **Q&A prep**
- **Rehearsal notes:** timing and what you changed

## Common mistakes
- Numbers in the slides that do not match the model card.
- Too many slides, too many metrics, ROC curves for executives.
- Topic headlines ("Results") instead of point headlines.
- Leaving limitations to the last 30 seconds.
- Treating "production" as "put the model on a server".

## Self-check before the PR
- [ ] Model card final: every number checked and sourced
- [ ] Slide draft in `docs/` following the outline, with point headlines
- [ ] Production slide covers real-time scoring, drift monitoring, review queue
- [ ] Q&A prep written
- [ ] One timed rehearsal done
- [ ] Branch `day14-docs-and-presentation-prep`, PR opened

## Going further (optional)
Write a one-page executive summary (problem, recommendation, three numbers, risks, ask) that could be read without the presentation.
