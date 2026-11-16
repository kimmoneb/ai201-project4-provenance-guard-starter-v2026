
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

### Criterion 2: False-Positive Protection
Result: 1 of 20 human-written passages was classified as AI (5%).
Verdict: Met the 10% false-positive limit. The before-and-after comparison on the same samples was not independently verified.

### Criterion 3: Classification Improvement
Result: The linguistic analyzer adds explanatory features but does not change the classification score. None of the four monitored pattern types appeared in the 40 comparison samples.
Verdict: Not met. No improvement of at least 3 percentage points was demonstrated.

### Criterion 4: API Reliability
Result: All 40 comparison submissions completed successfully after pacing requests to respect rate limits. The API returned classifications and linguistic patterns.
Verdict: Partially verified. A separate invalid-input test and reliability percentage are still needed.

### Criterion 5: Observability
Result: Verified an audit entry containing timestamp, prediction, HTTP status, processing time, outcome, and linguistic pattern counts.
Verdict: Passed the single-request verification. Consistency across multiple requests remains untested.

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
