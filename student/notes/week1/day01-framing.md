# Day 1 notes: Framing the problem

Assignment: `assignments/week1/day01-framing/` · Branch: `day01-framing` · No code, no data.

## Learning objectives
By the end of this lesson you should be able to:
- Explain the difference between a rule-based system and a machine learning system, with examples
- Describe any prediction task with four questions: input, output, what is correct, cost of being wrong
- Explain supervised and unsupervised learning and when each is the better tool
- Argue why a fraud system benefits from both

# Part 1: Lesson

## Why this day matters
Before you build anything you need to know what "working" means. Most failed ML projects fail here: the team optimizes a number nobody in the business cares about. Today you learn to describe fraud detection as a task you can measure, and you learn why this project builds two different kinds of model.

## The concepts

### Rules vs. machine learning
- A **rule** is logic a person writes: "decline if the amount is over 5,000 and the card is used abroad". Rules are transparent, quick to write and easy to audit. They are also brittle: fraudsters learn them and work around them, and every new pattern needs someone to notice it and write a new rule.
- A **machine learning model** learns the logic from examples. It can combine dozens of weak signals that no person would think to write as a rule. The price: it needs data, it can be wrong in ways that are hard to explain, and it is only as good as the examples it learned from.
- **AI** is the umbrella term. ML is the part of AI that learns from data. In this course "AI" always means ML; there is no magic.
- Real fraud systems use **both**: rules for hard policy ("never allow transactions from a sanctioned country"), ML for subtle patterns, people for borderline cases.

### What makes a task measurable
You can measure a task when you can answer four questions:
1. **Input:** what information do we have when we decide?
2. **Output:** what do we produce? A yes/no flag? A score?
3. **Correct:** how do we know afterwards whether we were right?
4. **Cost of being wrong:** what happens when we are wrong, *in each direction*?

The fourth question is the one people skip. There are two kinds of wrong, and they do not cost the same.

### Supervised vs. unsupervised
- **Supervised:** you have past examples *with the answer attached* (this was fraud, this was not). The model learns to recognize patterns like the ones it has seen.
- **Unsupervised:** you have no answers. The model looks for structure, for example transactions that look unlike everything else.
- An analogy: a border officer with a list of known smugglers' habits (supervised) vs. an officer who notices that someone just behaves oddly (unsupervised). Each catches people the other misses.

## Summary
- Rules are written by people; ML logic is learned from examples. Real systems use both, plus human review.
- A task is measurable when you can name its input, output, ground truth and the cost of each kind of error.
- In fraud there are two errors (missed fraud, blocked customer) and they do not cost the same.
- Supervised learning recognizes known fraud; unsupervised learning flags the unusual, including fraud nobody has seen yet.

## Check your understanding
Try these from memory before you start the assignment. If you cannot answer one, re-read that section.
1. Why do fraud rules decay over time?
2. What are the four questions that make a task measurable?
3. Who pays for a missed fraud? Who pays for a false alarm?
4. Why can't a supervised model catch a brand-new fraud pattern reliably?
5. Why is "unusual" not the same as "fraud"?

# Part 2: How to attempt each task

### Setup tasks (do these today)
1. Create the virtual environment and install requirements: see [00 - Setup](../00-setup-and-workflow.md#1-environment).
2. Download the dataset into `data/`. You will not use it until Day 3, but a 150 MB download plus a Kaggle login can take a while, so do not leave it to the last minute.
3. Do the git loop once end to end. Today's PR is as much about learning the workflow as about the answers.

### Q1. Rules vs. ML, with one fraud example each way
- **What it asks:** the difference in your own words, plus two concrete examples.
- **Approach:**
  1. One or two sentences on the difference. Focus on *who writes the logic* (a person vs. learned from data).
  2. A fraud a rule catches well. Think: what fraud has a simple, fixed signature you could write as one "if" statement?
  3. A fraud a rule misses. Think: what fraud looks normal on any single signal, but odd when you combine several? Or a pattern that is brand new?
- **Hint:** good examples are specific. "Fraud with unusual behavior" is too vague; describe the transaction.

### Q2. Input, output, correct, cost of being wrong
- **What it asks:** the four questions above, applied to credit card fraud.
- **Approach:** write four short labeled lines. For "cost of being wrong" write **two** answers: one for a fraud we miss, one for a real customer we block. Name who pays each cost (the bank, the customer, the merchant).
- **Hint:** for "correct", ask yourself *how* and *when* the bank finds out a transaction was fraud. Is it immediate? Is it always found out?

### Q3. Supervised vs. unsupervised, with a situation for each
- **Approach:** define each in one sentence. Then give a fraud situation where each is the better choice. Ask yourself: in this situation, do I have reliable labels for this kind of fraud? Has it happened before?
- **Hint:** think about what happens on the first day a new fraud technique appears.

### Q4. Why build both?
- **Approach:** do not just say "both are useful". Say what each one is good at, what each one is bad at, and how one covers the other's weakness.
- **Self-test:** if your answer would still be true for "why build two random forests?", it is not specific enough.

### Q5. Head of fraud: what do you want, and what would make you shut it off?
- **Approach:** step out of the data scientist's chair. Write 3-5 sentences as someone accountable for losses *and* for customer complaints.
  - What do you want it to do? Think in outcomes: losses, customers, analyst workload.
  - What makes you shut it off? Think about the failure that would hurt you most in front of your boss or the press.
- **Hint:** "high accuracy" is not an answer a head of fraud would give. You will see why on Day 2.

## Common mistakes
- Using "AI" as if it means something mysterious. Keep it concrete: learned from examples vs. written by a person.
- Naming only one kind of error.
- Treating unsupervised learning as a worse version of supervised. It answers a different question.
- Writing in jargon. If your answer would confuse a non-technical manager, simplify it.

## Self-check before the PR
- [ ] All five answers are in my own words, not copied from slides
- [ ] Q1 has two concrete fraud examples
- [ ] Q2 names both kinds of wrong and who pays for each
- [ ] Q4 says *why* both, not just *that* both
- [ ] Environment installed, dataset downloaded (not committed!)
- [ ] Branch `day01-framing`, PR opened with the template filled in

## Going further (optional)
Think about how labels are created in real life: someone reports fraud, a chargeback is filed, an analyst investigates. What does that mean for how complete and how timely the labels are? This comes back on Days 8-10.
