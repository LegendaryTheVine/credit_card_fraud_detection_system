# Day 1: Theory: framing the problem

**Week 1** · 90 minutes · No code, no data today.

## Goal for the session
By the end, the student can explain in their own words: why fraud detection is a *measurable* AI task, why rules alone are not enough, and why this project builds both a supervised and an unsupervised model.

## Session outline
| Time | Segment |
|---|---|
| 0-10 | Welcome, course shape (15 days, one branch + PR per day), what is in and out of scope |
| 10-30 | AI vs. classical rules vs. ML |
| 30-55 | What makes fraud a *measurable* AI task |
| 55-75 | Supervised vs. unsupervised framing, and why we need both |
| 75-90 | Assignment handoff + PR workflow walkthrough |

## 1. AI vs. classical rules vs. ML (20 min)
Talking points:
- **Rules**: a human writes the logic. "Decline if amount > $5,000 and country != home country." Transparent, fast to build, brittle: fraudsters learn the rules, and every new pattern needs a human to write a new rule.
- **ML**: the logic is *learned from examples*. You supply data (and sometimes labels); the model finds the pattern. Handles many weak signals at once, but needs data and can be wrong in ways that are hard to explain.
- **AI** is the umbrella term; ML is the part of AI that learns from data. Deep learning, CV, NLP and GenAI are ML subfields we are deliberately skipping.
- Practical reality: production fraud systems use **both**. Rules for known, hard policies; ML for subtle patterns; humans for borderline cases.

Check for understanding: "Give me one fraud case a rule catches well and one it misses."

## 2. What makes fraud a measurable AI task (25 min)
A task is measurable when you can answer four questions:
1. **What is the input?** A transaction: Time, Amount, V1-V28 (anonymized).
2. **What is the output?** A fraud score and/or a fraud / not-fraud flag.
3. **What is "correct"?** A ground-truth label (the `Class` column).
4. **What does being wrong cost?** A missed fraud costs money and trust; a false alarm blocks a real customer. These costs are not equal, and the student should say so in their own words.

Introduce the dataset (preview only, do not open it): 284,807 transactions, 492 frauds, about 0.17%. Ask: "If I told you a model is 99.8% accurate, would you be impressed?" Park the answer; Day 2 resolves it.

Business-framing exercise (10 min, student talks, instructor scribbles): "You are the head of fraud at a bank. What would you want this model to do for you? What would make you shut it off?"

## 3. Supervised vs. unsupervised, and why both (20 min)
- **Supervised**: learn from labeled examples (fraud / not fraud). Strong when you have plenty of labeled history. Weakness: only recognizes patterns similar to what it has seen; labels arrive late and are incomplete.
- **Unsupervised**: no labels; find transactions that look unlike the rest (anomalies). Strength: can flag a brand-new fraud pattern. Weakness: "unusual" is not the same as "fraud"; more false alarms.
- **Why both**: supervised is the precise tool for known fraud; unsupervised is the early-warning net for the unknown. Week 2 builds one of each and compares them head to head.
- Analogy that works: a border officer with a list of known smugglers (supervised) vs. one who notices that someone's behavior is odd (unsupervised).

## Assignment handoff (15 min)
- Walk the student through `student/README.md`: clone, branch, commit, push, PR, template.
- Do a **dry run** with them: create branch `day01-framing`, edit `submission.md`, push, open a PR. Day 1's PR is mostly about learning the loop.
- Remind them to set up the environment (`requirements.txt`) and download the Kaggle dataset before Day 3.

## Common pitfalls
- Student treats "AI" and "ML" as interchangeable or "AI" as magic. Keep returning to: learns from examples vs. follows written rules.
- Student frames success as "high accuracy". Do not correct it yet; let Day 2 do it.
- Student thinks unsupervised is simply "worse supervised". It answers a different question.

## Expected deliverable
`submission.md` with answers to the assignment questions (see `student/assignments/week1/day01-framing/README.md`). Answer key: `instructor/solutions/week1/day01-framing/answer-key.md`.

## Review focus
Is the framing in their own words? Do they name both costs (missed fraud, false alarm)? Do they say *why* both model types are needed rather than just that they are?
