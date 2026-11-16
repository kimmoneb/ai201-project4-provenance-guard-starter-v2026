
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
