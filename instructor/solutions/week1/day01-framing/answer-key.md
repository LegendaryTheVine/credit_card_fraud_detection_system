# Day 1 answer key (guide, not a script)

1. **Rules vs. ML.** Rules: logic written by a human; ML: logic learned from examples. A rule catches "card used in two countries within an hour"; it misses a new pattern nobody has written a rule for, or a combination of many weak signals.
2. **Measurable task.** Input: a transaction (Time, Amount, V1-V28). Output: fraud score and/or flag. Correct: matches the ground-truth `Class` label. Cost of being wrong: missed fraud = direct financial loss + customer trust; false alarm = declined card, frozen account, support cost, annoyed customer. The two costs differ, and a good answer says so.
3. **Supervised vs. unsupervised.** Supervised learns from labeled fraud/not-fraud examples; best when plenty of labeled history exists and fraud looks like past fraud. Unsupervised has no labels and finds what is unusual; best for a brand-new fraud pattern or when labels do not exist yet.
4. **Why both.** Supervised is precise on known patterns but blind to novel ones; unsupervised can flag novel behavior but "unusual" is not "fraud", so it has more false alarms. They complement each other, and Week 2 compares them.
5. **Head of fraud.** Open-ended. Strong answers mention catching fraud *and* limiting false alarms, ideally with a concrete trigger for shutting it off (e.g. too many real customers blocked, or fraud losses not falling).

**Red flags:** only mentions "accuracy" as success; cannot say what a false alarm costs; treats unsupervised as "supervised without labels, so worse".
