# Day 15 notes: Final presentation

Assignment: `assignments/week3/day15-final-presentation/` · Branch: `day15-final-presentation` · Deliverables in `docs/`

## Learning objectives
By the end of this lesson you should be able to:
- Present an ML project to leadership as a business decision, not a technical tour
- Tell a clear story across framing, two approaches, results, demo and next steps
- Deliver a live demo calmly, with a fallback
- Handle questions honestly, including ones you cannot fully answer
- Reflect on what you learned and what you would do differently

# Part 1: Lesson

## Why this day matters
This is where three weeks of work become a decision. Imagine your own leadership is in the room: they need to understand the problem, trust the evidence, see it working, and know what it would take to go further. Being clear and honest matters more than being impressive.

## The concepts

### 1. The story arc
A strong presentation follows one line of argument:
1. **The problem:** fraud costs money; blocking real customers costs trust. Both matter, and they pull in opposite directions.
2. **Why it is hard:** fraud is about 1 in 580 transactions, so "99.8% accurate" means nothing; we measure catches and false alarms instead.
3. **What we built:** a supervised model that learns known fraud, and an anomaly detector that flags the unusual. Why both.
4. **What it achieves:** your two or three headline numbers, in plain language.
5. **See it work:** the demo.
6. **What it cannot do:** honest limitations.
7. **What it would take:** production next steps and your recommendation.

Every slide should move this argument forward. If a slide does not, cut it.

### 2. Delivery
- **Open with the problem, not yourself or the dataset.** The first 30 seconds decide whether people listen.
- **Say the point first,** then the evidence: "We catch about 8 in 10 frauds. Here's how we measured that."
- **Speak to the decision-maker's concerns:** money, customers, risk, effort.
- **Slow down on the key numbers.** Pause after each.
- **Point at what matters** on a chart ("look at this bar").
- **Keep to time.** Leave room for questions; they are where trust is built.

### 3. Running the demo live
- Start the app **before** the presentation and have the page open in a tab.
- Follow your Day 13 script exactly. Narrate what the audience should notice.
- Include one case the model gets wrong. It makes the limitations real and builds credibility.
- If something breaks, do not debug live: say "let me show you the recording" and switch to your backup.

### 4. Handling questions
- Listen to the whole question; restate it briefly if it is complex.
- Answer directly, in one or two sentences, then stop.
- If you don't know: "I don't know. Here is how I would find out." Never guess with false confidence.
- If a question exposes a real weakness, agree with it and say what you would do about it. That is a strength, not a failure.
- Use your Day 14 Q&A prep.

### 5. Honest next steps
End with a clear recommendation and a clear ask. For example: what you recommend (pilot in shadow mode? more data? the original features?), what it needs (people, data, time), and how success would be measured. Tie it to the production needs from Day 14: real-time scoring, drift monitoring, a human review queue.

### 6. Reflection
After presenting, reflect while it is fresh: what went well, what you would change, which concepts finally "clicked", and which ones you would still like to understand better. This is how the course turns into lasting skill.

## Summary
- One argument: problem → why it's hard → what we built → results → demo → limitations → next steps.
- Point first, evidence second, in business language.
- Rehearsed demo with a fallback; show at least one mistake.
- Answer questions directly and honestly.
- Finish with a recommendation and an ask.

## Check your understanding
1. What should the first 30 seconds of your presentation contain?
2. Why include a case the model gets wrong in the demo?
3. What do you do if the demo crashes?
4. How do you answer a question you cannot answer?
5. What is your recommendation, in one sentence?

# Part 2: How to attempt each task

### Task 1. Final materials in `docs/`
1. Apply your instructor's Day 14 feedback to the slides and model card.
2. Final check that every number on the slides matches the model card and notebooks.
3. Save the final slides (source or PDF) and any images in `docs/`. Keep file sizes reasonable.

### Task 2. Final rehearsal
1. Run the full presentation out loud with the demo, timed, at least once more.
2. Start the demo from a fresh terminal using the README to confirm it still works.
3. Check that the backup recording or screenshots are where you expect them.

### Task 3. Present
Follow the arc. Keep to time. Take questions.

### Task 4. Reflection in `submission.md`
Write short answers to:
1. **What went well** in the presentation and the project?
2. **What would you do differently** with another week? (Technically and in how you worked.)
3. **The three most important things you learned** in this course.
4. **Questions asked** during the presentation and how you answered them; would you answer differently now?
5. **What you would need** to take this into production for real.

## Common mistakes
- Starting with the dataset or the algorithm instead of the business problem.
- Reading the slides aloud.
- Running over time and squeezing out questions.
- Hiding limitations or getting defensive about them.
- Ending without a recommendation.

## Self-check before the PR
- [ ] Final slides and model card in `docs/`, numbers consistent
- [ ] Demo tested from a fresh start; backup ready
- [ ] Presentation rehearsed and within time
- [ ] Reflection written in `submission.md`
- [ ] Branch `day15-final-presentation`, PR opened

## After the course
Keep the repository. Its README, model card, API and slides are a portfolio piece. Consider adding a short top-level summary of what you built and the key results, so someone landing on it understands it in a minute.
