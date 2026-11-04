# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.

<!-- Your criterion. It must name a number. -->
## 1. False Positives

Of 10 human-written submissions, no more than 2 should be incorrectly classified as high-confidence AI.

**Why this target:**

I chose this target because AI detection systems can make mistakes, and falsely accusing someone of using AI could affect their credibility, especially in academic settings. I want my system to prioritize fairness and reduce the risk of false accusations while recognizing that no detection system is perfect.




---

## 2.

<!-- Your criterion. -->
## 2. Score Spread

The average combined score for 10 AI-generated submissions should be at least 0.3 higher than the average score for 10 human-written submissions.

**Why this target:**

I chose this target because I want the system to demonstrate a noticeable difference between human-written and AI-generated text. A difference of 0.3 would suggest that the two signals are helping distinguish writing patterns, while recognizing that some human and AI writing may overlap.



---

## 3.

<!-- Your criterion. -->
## 3. Label Coverage

The system should successfully produce all three labels (human, unsure, and AI) through the /submit endpoint using different text submissions.

**Why this target:**

I chose this target because I want to make sure the system can recognize different writing patterns instead of classifying everything as either human or AI. The unsure label is especially important because it acknowledges uncertainty and helps reduce the risk of false accusations.






---

## 4.

<!-- Your criterion. -->

## 4. Appeal Path

100% of valid appeals should receive an "under_review" status and be recorded in the audit log with the content ID, creator ID, reasoning, and timestamp.

**Why this target:**

I chose this target because writers should have a reliable way to challenge a classification they believe is incorrect. Every valid appeal should be documented to ensure transparency and accountability. Missing an appeal could prevent someone from having their work fairly reviewed.



---

## 5.

<!-- Your criterion. -->



## 5. Invalid Input

100% of submissions with missing or empty text should return an HTTP 400 Bad Request response instead of crashing the system.

**Why this target:**

I chose this target because the system should handle invalid submissions safely and consistently. Missing or empty text should not cause the application to crash or produce misleading classifications. Returning a clear error message helps users understand what went wrong and makes the API more reliable.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
