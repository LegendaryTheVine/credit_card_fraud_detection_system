# Rubric: Day 1 - Framing the problem

Score each criterion 0-2 (0 = missing, 1 = partial, 2 = meets). **Pass: 7+ of 10 and no 0 on criteria 2 or 3.** Otherwise: Revise.

| # | Criterion | 2 = meets | 1 = partial | 0 = missing |
|---|---|---|---|---|
| 1 | Rules vs. ML (Q1) | Correct distinction (written vs. learned logic) plus one example a rule catches and one it misses | Distinction right, examples missing or vague | Confuses the two or copies jargon |
| 2 | Measurable task (Q2) | Names input, output, correct, **and** cost of being wrong in *both* directions (missed fraud, false alarm) | Names the four parts but only one error cost | Only mentions "accuracy" or omits cost |
| 3 | Supervised vs. unsupervised (Q3-4) | Correct definitions, a fraud scenario for each, and *why* both are needed | Definitions right, no scenario or no "why both" | Treats unsupervised as "worse supervised" or mixes them up |
| 4 | Business framing (Q5) | Own words; says what it should do and gives a concrete shutoff trigger | Generic ("catch fraud") with no trigger | Blank or copied |
| 5 | Process | Branch `day01-framing`, PR template filled, environment installed, dataset downloaded | One of these missing | PR opened wrongly or nothing set up |

**Feedback prompts:** Did they put it in their own words? Do they know a false alarm has a cost?
