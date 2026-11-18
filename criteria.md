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


---

# Unit 9 Capstone — Provenance Guard 2.0


# Unit 9 — Provenance Guard 2.0

## Project Goal
Improve the existing AI-writing detector by adding a
research-based linguistic pattern analyzer.

The analyzer will examine AI-associated vocabulary,
em dashes, Oxford commas, and sentence structures.

## Five Acceptance Criteria

1. Pattern Detection
   Correctly identify at least 90% of manually
   annotated linguistic patterns across 20 passages.

2. False Positive Protection
   On at least 20 human-written passages, no more
   than 10% should be incorrectly classified as AI.
   The false-positive rate must not increase.

3. Classification Improvement
   Improve balanced accuracy by at least 3 percentage
   points compared with the original detector, using
   the same test set of at least 20 human and 20 AI passages.

4. API Reliability
   At least 95% of valid requests must return HTTP 200
   with the classification and linguistic pattern results.
   Invalid text inputs must return HTTP 400.

5. Observability
   Log the timestamp, classification, processing time,
   request outcome, and pattern counts for every
   evaluated submission, without adding raw text
   to the monitoring fields.



## False Positive Investigation

During my initial evaluation of 20 human-written and 20 AI-generated samples, the detector incorrectly classified one of my human-written passages as AI.

The passage received a model score of 0.7981, a style score of 0.6946, and a combined score of 0.7463, exceeding the AI classification threshold of 0.65.

Both existing signals contributed to the incorrect classification. The new linguistic analyzer found no AI-associated vocabulary or em dashes in this passage.

This suggests that conventional human writing can receive high AI-likelihood scores even without the linguistic patterns being investigated. My next step is to evaluate whether additional linguistic features can improve classification while maintaining a low false-positive rate.



## Final Evaluation — Unit 9

### Criterion 1: Linguistic Pattern Detection
Result: 20/20 selected test cases passed (100%).
Verdict: Passed the selected checks, although the tests do not measure all possible false positives.

**Three-Trial Evaluation**

- **Trial 1:** 20/20 test cases passed (100%).
- **Trial 2:** 20/20 test cases passed (100%).
- **Trial 3:** 20/20 test cases passed (100%).

**Source:** `evaluate_patterns.py`, which calls `analyze_patterns()` from `linguistic_patterns.py` and compares the output against expected values in `linguistic_test_data.py`.

**Verdict:** Passed. All three trials exceeded the 90% target. However, these trials reused the same 20 selected cases, demonstrating repeatability rather than accuracy across independent datasets.

### Criterion 2: False-Positive Protection
Result: 1 of 20 human-written passages was classified as AI (5%).
Verdict: Met the 10% false-positive limit. The before-and-after comparison on the same samples was not independently verified.

**False-Positive Protection Evaluation**

**Target:** No more than 10% of human-written passages should be incorrectly classified as AI, and the false-positive rate should not increase after the extension.

**Measured Result:** Of the 20 human-written passages evaluated, 11 were classified as human, 8 as unsure, and 1 as AI.

The observed false-positive rate was:

1 / 20 × 100 = **5%**

**Source:** `writing_comparison_results.json`, generated by `compare_writing.py`.

**Scoring Verification:** The classification formula in `scoring.py::combine_signals()` assigns 50% weight to the GPT-2 model and 50% to stylometry. The linguistic pattern analyzer provides additional information but does not affect the combined score.

**Verdict:** The observed false-positive rate meets the 10% threshold. The unchanged scoring logic supports the expectation that the extension does not introduce additional false positives, but an independent before-and-after evaluation has not been completed.

**Remaining Work:** Complete three documented evaluation trials and verify the before-and-after results using the same passages.


### Criterion 3: Classification Improvement

**Target:** Improve balanced accuracy by at least 3 percentage points compared with the original detector, using at least 20 human-written and 20 AI-generated passages.

**Results:** I evaluated 40 passages, including 20 human-written and 20 AI-generated samples.

- Human-written: 11 classified as human, 1 as AI, and 8 as unsure.
- AI-generated: 8 classified as AI, 4 as human, and 8 as unsure.

Treating unsure predictions as incorrect, human recall was 55% and AI recall was 40%, resulting in a balanced accuracy of **47.5%**.

**Diagnosis:** The linguistic analyzer adds explanatory features but does not change the classification score. The four monitored pattern types were not detected in the 40 comparison samples, limiting my ability to evaluate their usefulness for improving predictions.

**Verdict:** Not met. I did not demonstrate the required 3-percentage-point improvement over the original detector.

**Next Improvement:** I would test a more diverse collection of human-written and AI-generated passages containing the monitored linguistic patterns. I would then evaluate whether incorporating these features into the scoring system improves balanced accuracy without increasing false positives.

**Source:** `compare_writing.py`, `writing_comparison_results.json`, `linguistic_patterns.py`, and `scoring.py::combine_signals()`.

### Criterion 4: API Reliability

**Target:** At least 95% of valid requests must return HTTP 200 with classification and linguistic pattern results. Invalid text inputs must return HTTP 400.

**Result:** During the 40-sample comparison, all 40 valid submissions completed successfully after requests were paced to respect rate limits. I also tested nine additional valid submissions, all of which returned classification and linguistic pattern results.

During invalid-input testing, I discovered that submitting a JSON list caused an HTTP 500 error because the application attempted to call `.get()` on a list. I added an `isinstance(payload, dict)` validation check and confirmed that the same input returned HTTP 400.

I also verified that submitting an empty string returned HTTP 400. After identifying that rejected requests were missing from the audit log, I updated the logging logic and confirmed that an empty-text rejection was recorded.

**Verdict:** Passed the observed valid-request tests and the tested invalid-input cases. However, the 95% reliability target has not been established through a dedicated, repeatable reliability test covering different request types and operating conditions.

### Criterion 5: Observability

**Target:** Record the timestamp, classification, processing time, request outcome, and linguistic pattern counts for every evaluated submission without storing raw text in the monitoring fields.

**Result:** I verified 10 successful audit records containing timestamps, classification results, HTTP status codes, processing times, and linguistic pattern counts. I also identified a logging gap: invalid text requests returned HTTP 400 but were not recorded.

I updated `app.py` to log rejected text submissions and repeated the empty-text test. The application returned HTTP 400 and recorded a rejected request with a processing time of 0.06 milliseconds and the reason `empty_or_invalid_text`.

**Verdict:** Passed the selected successful-request logging checks and the empty-text rejection test. Full coverage remains unverified because other failure paths, including non-object JSON requests, are not yet logged.

**Three-Trial Evaluation**

I tested observability across three trials using both valid and rejected submissions. All six requests produced corresponding records in `logs/audit.jsonl`.

- **Trial 1:** Valid request logged with HTTP 200 and a processing time of 47.54 ms. Rejected request logged with HTTP 400 and a processing time of 0.05 ms.
- **Trial 2:** Valid request logged with HTTP 200 and a processing time of 46.95 ms. Rejected request logged with HTTP 400 and a processing time of 0.05 ms.
- **Trial 3:** Valid request logged with HTTP 200 and a processing time of 47.46 ms. Rejected request logged with HTTP 400 and a processing time of 0.05 ms.

All three successful requests were classified as `unsure` and recorded the four linguistic pattern counts. The Oxford comma count was 1, while the other three pattern counts were 0.

Rejected submissions were recorded with the status `rejected` and the reason `empty_or_invalid_text`. Raw submission text was not included in these records.

**Verdict:** Passed for the tested valid and empty-text rejection paths. Broader logging coverage, including other malformed requests, has not been fully verified.

**Evidence:** `logs/audit.jsonl`, `app.py`, and `results/run_2026-11-17_2040_unit9_reliability.md`.

### Remaining Limitations
- The 40 comparison passages were short and did not contain the monitored linguistic patterns.
- Linguistic patterns are not definitive evidence of AI authorship.
- One human-written passage was incorrectly classified as AI.
- One observed submission took 9.49 seconds to process.
- The analyzer is not yet incorporated into classification scoring.

### Next Improvements
1. Evaluate on a larger, more varied dataset.
2. Improve pattern-matching precision and test false positives.
3. Investigate the false-positive classification.
4. Measure API latency and reliability across multiple requests.
5. Test whether adding linguistic features improves classification before changing the scoring formula.



## API Validation: Diagnose, Fix, and Retest

During API testing, I discovered that submitting a JSON list instead of an object caused an HTTP 500 error.

**Diagnosis:** The `/submit` endpoint called `.get()` on the incoming payload without first checking whether it was a dictionary. Since Python lists do not support `.get()`, the application raised an AttributeError.

**Fix:** I added an `isinstance(payload, dict)` check before extracting the text. Invalid JSON structures now return HTTP 400 instead of crashing the application.

**Retest:** I repeated the same request using `["invalid", "input"]`. The API successfully returned HTTP 400 with the message "JSON body must be an object."

**Outcome:** The bug was resolved, improving API robustness. Both empty-text requests and non-object JSON requests now return HTTP 400.
