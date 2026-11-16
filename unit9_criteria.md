
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