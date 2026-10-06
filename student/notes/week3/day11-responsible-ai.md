# Day 11 notes: Responsible AI, applied

Assignment: `assignments/week3/day11-responsible-ai/` · Branch: `day11-responsible-ai` · Deliverable: first draft of `docs/model_card.md`

## Learning objectives
By the end of this lesson you should be able to:
- Explain what fairness means for a fraud model, and why you cannot fully measure it on this dataset
- Check model performance across meaningful slices of the data
- Explain a model's behavior at the global level (what matters overall) and the local level (why this transaction)
- Describe the cost of a false positive from the customer's point of view
- Write a model card that is honest about limitations

# Part 1: Lesson

## Why this day matters
A fraud model makes decisions about people's money. A wrongly blocked card can leave someone stranded at a petrol station, abroad, or unable to pay rent. Responsible AI is not a separate checklist added at the end. It is asking, with evidence, **who gets hurt when this model is wrong, and would we know?**

## The concepts

### 1. Fairness in fraud detection
A model is unfair if its errors fall disproportionately on some group of people, for example if customers from one area, age group or income level are flagged far more often for the same behavior.

Common ways to measure it (when you have group information):
- **False positive rate per group:** are honest customers in group A blocked more often than in group B?
- **Recall per group:** is fraud against group A caught less often?
- **Alert rate per group:** what share of each group gets flagged at all?

**The honest problem with this dataset:** there are no demographic or location features, and V1-V28 are anonymized mixtures of unknown original features. So:
- you **cannot** measure fairness across protected groups here,
- you **cannot** rule out that some V feature is a **proxy** for something sensitive (e.g. a feature that encodes location, which correlates with ethnicity or income).
Saying this clearly is the correct, responsible answer. Pretending fairness was checked would be the irresponsible one.

### 2. What you can do: slice analysis
You can check whether performance is uneven across slices you *can* see, as a stand-in:
- **Amount bands:** e.g. under 10, 10-100, 100-1,000, over 1,000. Do small-amount customers get more false alarms?
- **Hour of day:** are night-time customers blocked more?
For each slice, at your Day 7 threshold: number of transactions, frauds, false positive rate, recall. Watch the sample sizes; fraud counts per slice will be small.

If you find uneven false-positive rates, ask: is it justified by real risk, and who are the customers who bear it?

### 3. Explainability: global and local
- **Global** ("how does the model work overall?"): Day 6 feature importance and Day 5 coefficients.
- **Local** ("why was *this* transaction flagged?"): what a customer, an analyst or a regulator actually asks.

Ways to get local explanations with the tools you have:
- **Logistic regression:** contribution of each feature = coefficient × (scaled) feature value. Sort them; the largest positive contributions are "reasons" for the score.
- **Tree models:** compare the transaction's feature values with typical legit values for the top-importance features. Or change one feature at a time back to a typical value and see how much the score drops (a simple "what-if").
- **SHAP** is the standard library for this, but it is not in `requirements.txt`. Optional; check with your instructor before adding it.

The limit again: the explanation will say "V14 was unusually low". That helps a data scientist and means nothing to a customer. Write down what a useful explanation would require (the original features).

### 4. The real cost of a false positive
From the customer's side, a false alarm can mean:
- a declined payment at a bad moment (travel, emergencies, large purchases),
- time on the phone proving who they are,
- a frozen card and no access to money,
- embarrassment, loss of trust, switching banks.
The harm is not spread evenly: someone with one card and no savings is hurt more than someone with three cards. That is a fairness issue even without demographic data.

Mitigations worth knowing: step-up verification (an SMS or app confirmation) instead of a hard decline; human review for borderline scores; a fast appeal path; monitoring complaint rates.

### 5. Where not to trust the model, especially the unsupervised one
- **Unsupervised:** "unusual" is not "fraud". It will flag honest unusual behavior (a big one-off purchase, travel). It must never decline a card on its own: route its alerts to review.
- **Supervised:** it only knows fraud patterns from two days in 2013. New fraud patterns, new products, or other countries are outside what it has seen.
- **Both:** performance will drift as behavior changes; scores are not calibrated probabilities if you used class weights or SMOTE.

### 6. Model cards
A **model card** is a short, honest document that travels with a model so others can decide whether to trust it for their purpose. Good model cards are specific (numbers, data, dates), plain-spoken, and spend at least as much space on limitations as on strengths. Your template in `docs/model_card.md` has the sections you need.

## Summary
- Fairness = are errors spread unevenly across groups of people? This dataset cannot answer that for protected groups, and saying so is the responsible answer.
- Slice analysis by Amount and hour is a partial check you can do.
- Explain globally (importance) and locally (per-transaction reasons). Anonymized features limit both.
- A false positive has real, unequal human costs. Design mitigations, not just thresholds.
- The unsupervised model should never act alone; the supervised one is limited to the patterns it has seen.
- A model card's value is in its honesty about limitations.

## Check your understanding
1. Why can't you measure fairness across protected groups with this dataset?
2. What is a proxy feature, and why is it a risk here?
3. What is the difference between a global and a local explanation?
4. Name two ways to reduce the harm of false positives besides changing the threshold.
5. Why should the unsupervised model not be allowed to decline cards on its own?

# Part 2: How to attempt each task

### Task 1. Slice analysis
1. Use your final supervised model, its test-set scores, and your Day 7 threshold.
2. Define Amount bands (`pd.cut`) and hour-of-day bands (e.g. night/morning/afternoon/evening).
3. For each slice: transactions, frauds, flagged, false positive rate, recall. One table per slicing.
4. Takeaway: is any slice treated noticeably worse? Is the sample big enough to say?

### Task 2. Explain a few individual decisions
1. Pick three test transactions: a true positive, a false positive, and a false negative.
2. For each, list the top 3-5 reasons using one of the methods in section 3.
3. Write how you would explain the false positive to the customer, and note what you cannot say because of anonymization.

### Task 3. The cost of a false positive, in human terms
Write one paragraph from a customer's point of view, then one paragraph on mitigations you would recommend.

### Task 4. First draft of `docs/model_card.md`
Fill in every section. Prompts:
| Section | What to write |
|---|---|
| What the model does | Inputs, outputs (score + flag), the threshold and how it was chosen, intended use (decision support for fraud analysts, or automatic declines?) |
| Data | Source, period (2 days, Sept 2013, European cardholders), size, fraud rate, anonymization, preprocessing, train/test split |
| Performance | PR-AUC (headline), ROC-AUC, precision/recall at your threshold, cost estimate, with which data they were measured on |
| Limitations | Short time window, old data, anonymized features, small fraud count, random rather than time-based split, uncalibrated scores, fairness not measurable |
| Where it should not be trusted unsupervised | When the anomaly detector should and should not be used; human review requirements |
| Cost of a false positive for a real customer | Your Task 3 paragraph, plus mitigations |

### `submission.md` (suggested structure)
- **Slice analysis results** and what they mean
- **Three explained decisions**
- **What we cannot check, and why**
- **Link to the model card draft** and anything you were unsure how to write

## Common mistakes
- Claiming the model is "fair" because it has no demographic features. Proxies can still carry bias, and you cannot check.
- Slice tables without sample sizes.
- A model card that reads like marketing.
- Explanations that just list V-numbers without admitting they mean nothing to a customer.

## Self-check before the PR
- [ ] Slice tables for Amount and hour, with counts
- [ ] Three individual decisions explained
- [ ] Every model card section filled in, with numbers
- [ ] Limitations section at least as long as the performance section
- [ ] Branch `day11-responsible-ai`, PR opened

## Going further (optional)
Read one published model card (Google's original "Model Cards for Model Reporting" paper has examples) and compare its structure with yours. What did they include that you did not?
