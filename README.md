# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. The writer submits their text and creator ID through the `/submit` endpoint.
2. The system validates the submission to ensure the text is provided and is not empty.
3. `detector.py` analyzes how predictable the text is and generates a model score.
4. `stylometry.py` examines sentence length, vocabulary diversity, and punctuation patterns to generate a style score.
5. `scoring.py::combine_signals` combines both scores to estimate how AI-like the writing appears.
6. `scoring.py::score_to_label` converts the score into a human, unsure, or AI classification.
7. The system records the decision in an audit log and returns the result to the writer, who can appeal if they disagree.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**

The style signal examines writing patterns, including sentence length variation, vocabulary diversity, and punctuation usage.

**Why that might differ between human and AI writing:**

AI-generated writing may have more consistent sentence structures and repetitive patterns, while human writing can vary in sentence length, word choice, and punctuation. However, these patterns are not always consistent across writers.

**What it can't see:**

The style signal cannot understand the meaning of the writing or determine who actually wrote it. For example, adding punctuation, introducing typos, or changing sentence structures can affect the score without changing whether the text was written by a human or AI.


### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

The system uses a weighted average to combine the model and style signals into one final score between 0 and 1. Both signals have equal importance. I chose this approach because relying too heavily on one signal could increase the risk of false positives. When the signals disagree, the final score reflects that uncertainty rather than automatically classifying the writing as AI-generated.

**The numbers:**

Model signal weight = 0.5  
Style signal weight = 0.5

Final score = (0.5 × model score) + (0.5 × style score)

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**

For example, suppose the model signal produces a score of 0.90, suggesting the writing is highly predictable and potentially AI-generated. However, the style signal produces a score of 0.10, suggesting the writing patterns are more human-like. The combined score would be 0.50. Instead of relying on either signal alone, the system accounts for their disagreement. Depending on the configured thresholds, this score could fall into the unsure category.

### False-Positive Scenario

Imagine a student who writes an assignment entirely on their own but uses simple vocabulary and short sentences. The model might consider their writing highly predictable and assign it a high AI score. Suppose the combined score is 0.85 and the system classifies the assignment as high-confidence AI.

Even though the student wrote the assignment themselves, they could face questions about academic integrity. This demonstrates why a high AI score should not automatically be treated as proof of AI usage.

I think the student should have the opportunity to appeal the decision and request a human review. The reviewer could examine supporting evidence, such as drafts, revision history, and the student's explanation. If the decision is incorrect, the classification should be corrected, and the outcome documented in the audit log.

This approach would help reduce the harm caused by false positives while making the system more transparent and accountable.

### API Endpoint Contracts

**POST /submit**

The endpoint receives JSON containing `text` and `creator_id`. The system validates the submission, analyzes the writing, and returns JSON containing `content_id`, `guess`, `confidence`, `label`, `model_score`, and `style_score`. The content ID allows the submission to be tracked, while the scores and label explain the system's classification. Invalid submissions should receive an error response rather than causing the service to crash.

**POST /appeal**

The endpoint receives JSON containing `content_id` and `reasoning`. It checks whether the content ID exists in the audit log. If the submission exists, the system records the appeal, changes its status to `under_review`, and returns confirmation to the writer. An invalid content ID should receive an error response. The appeal does not automatically change the original classification; it creates an opportunity for further review.
---
**What it measures:**

The model signal uses GPT-2 to measure how predictable the submitted text is through perplexity. Lower perplexity produces a higher AI-likeness score.

**Why that might differ between human and AI writing:**

AI-generated writing may follow more predictable word patterns, while human writing can be less consistent. However, predictable writing does not necessarily mean AI was used.

**What it can't see:**

The model cannot determine who actually wrote the text. For example, a student using simple vocabulary or writing in a second language might receive a high AI score even if they wrote everything themselves.

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00–0.35 | This text appears more likely to have been written by a person. |
| unsure | Above 0.35, below 0.65 | We cannot confidently determine whether this text was written by a person or generated by AI. |
| high-confidence AI | 0.65–1.00 | This text shows patterns commonly associated with AI-generated writing, but the result is not definitive. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

I chose these three labels to avoid making definitive claims about whether someone used AI. Scores between 0.35 and 0.65 are classified as "unsure" because the model and writing-style signals may disagree. This helps reduce the risk of falsely accusing someone of using AI. Even when a score is high, the system acknowledges that its prediction is not definitive. Writers can also appeal a decision if they believe their work was incorrectly classified.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->
### Milestone 3 — Submit Test

Request:
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text":"I went to the store. It was raining heavily outside! I forgot my umbrella, so I ran home.","creator_id":"student1"}'


Result:
{
  "combined_score": 0.6088208109008646,
  "confidence": 0.22,
  "content_id": "8b6e121f-f877-4d18-b533-ae10f60bed23",
  "guess": "unsure",
  "label": "We cannot confidently determine whether this text was written by a person or generated by AI.",
  "model_score": 0.6472,
  "style_score": 0.5704416218017291
}
### Audit Log Test

Request:
curl "http://127.0.0.1:5000/log?limit=3"

Result:
- The submission appeared in the audit log.
- creator_id: student1
- model_score: 0.3492
- status: decided

### Invalid Input Test

An empty text submission returned HTTP 400 BAD REQUEST.
**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I spent the weekend studying for my data science exam.", "creator_id": "student1"}'
```

```json

```
{
  "content_id": "PASTE_YOUR_ACTUAL_CONTENT_ID_HERE",
  "guess": "unsure",
  "confidence": 0.5,
  "label": "The system is unsure whether this text was AI-generated.",
  "model_score": 0.3492,
  "style_score": 0.0
}

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id":"930019e1-7d1b-4c2f-82e1-ce95121187e1","reasoning":"I wrote this text myself."}'
```

```json
{
  "content_id": "930019e1-7d1b-4c2f-82e1-ce95121187e1",
  "status": "under_review",
  "message": "Your appeal has been received and is awaiting review."
}
```

**What the log shows afterwards**

```bash
**What the log shows afterwards**

Request:
```bash
curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "content_id": "930019e1-7d1b-4c2f-82e1-ce95121187e1",
  "creator_id": "student1",
  "event": "appeal",
  "reasoning": "I wrote this text myself.",
  "status": "under_review",
  "timestamp": "2026-11-04T03:28:48+00:00"
}
```

---

## How I Used AI

**Moment 1**

- **What I asked for:** I asked AI to help me understand how to implement and test the `/submit` endpoint, including combining the model and style scores.
- **What came back:** AI provided code examples, explained how the functions worked together, and suggested using curl commands to test the API.
- **What I changed:** I implemented the functions in my project, tested the endpoint using my own inputs, and verified that the response included the required scores, classification, and content ID.

**Moment 2**

- **What I asked for:** I encountered issues with the JSON responses when testing my API, so I asked AI to help me debug the errors and understand why my requests kept failing.
- **What came back:** AI helped me identify possible issues with my code, including missing arguments in the `log_appeal()` function and incorrect content IDs when testing the `/appeal` endpoint.
- **What I changed:** I reviewed the errors, updated my code to include the required `creator_id`, and tested the endpoint again using a valid content ID. After making these changes, the appeal request worked, and I verified that it was recorded in the audit log.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

*## Rate Limiting

**My limits:** 10 requests per minute, 200 requests per day.

**Why those numbers and not others:**

I chose these limits because I want legitimate writers to have enough opportunities to submit and review their work without making it easy for automated scripts to overwhelm the system. Ten requests per minute should be sufficient for normal use, while 200 per day limits repeated attempts to test or manipulate the detector.

**What a caller counts as:**

A caller is identified by their IP address. This means requests from the same IP address share the rate limit, even if they use different creator IDs.

**The run of status codes when I pushed past it:**

```text
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

Out of 15 requests, 10 were successful and 5 were rejected with HTTP 429. This confirms that the per-minute rate limit was enforced.

**Flood test results:** `results/flood_2026-11-13_1337.md`
<!-- python run_attacks.py --flood 15 -->


### Attack Test Results

I tested three attacks against the `/submit` endpoint. All three requests returned HTTP 200, with no crashes.

- **Paraphrasing — BROKE:** The detector returned "unsure" with confidence 0.28, showing that paraphrasing may make AI-generated text harder to identify.
- **Informal writing — BROKE:** The detector returned "unsure" with confidence 0.25, suggesting that informal language can reduce detection confidence.
- **Repetition — HELD:** The detector returned "ai" with confidence 0.82, meaning the repetitive writing was still flagged.

These results show that the API remained operational, but its classification was less decisive for paraphrased and informal text.
  
```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->


| Attack | Family | Result | Verdict |
|---|---|---|---|
| attack_01 | Paraphrasing | unsure (0.28) | BROKE |
| attack_02 | Informal writing | unsure (0.25) | BROKE |
| attack_03 | Repetition | ai (0.82) | HELD |
  

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

[
  {
    "combined_score": 0.6393833333333333,
    "content_id": "6c4fa166-da0a-4392-9304-8131ef8e4c84",
    "creator_id": "attacker_attack_01",
    "guess": "unsure",
    "label": "We cannot confidently determine whether this text was written by a person or generated by AI.",
    "model_score": 0.6121,
    "status": "decided",
    "style_score": 0.6666666666666666,
    "timestamp": "2026-11-13T19:02:56+00:00"
  },
  {
    "combined_score": 0.3727933142466865,
    "content_id": "67288d35-b754-4ddd-883b-6fb8f505f4c4",
    "creator_id": "attacker_attack_02",
    "guess": "unsure",
    "label": "We cannot confidently determine whether this text was written by a person or generated by AI.",
    "model_score": 0.3424,
    "status": "decided",
    "style_score": 0.403186628493373,
    "timestamp": "2026-11-13T19:02:56+00:00"
  },
  {
    "combined_score": 0.9117944444444445,
    "content_id": "4e4268cf-4f9f-478b-bc55-2d1fefc7697e",
    "creator_id": "attacker_attack_03",
    "guess": "ai",
    "label": "This text shows patterns commonly associated with AI-generated writing, but the result is not definitive.",
    "model_score": 0.9347,
    "status": "decided",
    "style_score": 0.888888888888889,
    "timestamp": "2026-11-13T19:02:56+00:00"
  },
  {
    "creator_id": "flood_tester",
    "event": "rejected",
    "limit": "10 per 1 minute",
    "reason": "rate_limited",
    "status": "rejected",
    "timestamp": "2026-11-13T18:37:05+00:00"
  },
  {
    "creator_id": "flood_tester",
    "event": "rejected",
    "limit": "10 per 1 minute",
    "reason": "rate_limited",
    "status": "rejected",
    "timestamp": "2026-11-13T18:37:05+00:00"
  },
  {
    "creator_id": "flood_tester",
    "event": "rejected",
    "limit": "10 per 1 minute",
    "reason": "rate_limited",
    "status": "rejected",
    "timestamp": "2026-11-13T18:37:05+00:00"
  },
  {
    "creator_id": "flood_tester",
    "event": "rejected",
    "limit": "10 per 1 minute",
    "reason": "rate_limited",
    "status": "rejected",
    "timestamp": "2026-11-13T18:37:05+00:00"
  },
  {
    "creator_id": "flood_tester",
    "event": "rejected",
    "limit": "10 per 1 minute",
    "reason": "rate_limited",
    "status": "rejected",
    "timestamp": "2026-11-13T18:37:05+00:00"
  },
  {
    "content_id": "930019e1-7d1b-4c2f-82e1-ce95121187e1",
    "creator_id": "student1",
    "event": "appeal",
    "reasoning": "I wrote this text myself.",
    "status": "under_review",
    "timestamp": "2026-11-04T03:28:48+00:00"
  },
  {
    "combined_score": 0.256243137254902,
    "content_id": "9eead158-adae-4f70-9449-cbbaa0af1c59",
    "creator_id": "student3",
    "guess": "human",
    "label": "This text appears more likely to have been written by a person.",
    "model_score": 0.2968,
    "status": "decided",
    "style_score": 0.21568627450980393,
    "timestamp": "2026-11-04T04:52:29+00:00"
  }
]

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:


The most concerning result was attack_03 (repetition), which received an AI classification with 0.82 confidence. The text simply repeated "My favorite color is Pink" three times, yet the detector identified it as AI-like.

This concerns me because a human writer could naturally repeat phrases, especially when learning a language or using simple sentence structures. If this system were used in education, a student could be unfairly accused of using AI based on writing style alone.

I would prioritize reducing these false positives and requiring human review before making decisions that could negatively affect someone.


---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->


| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False Positives | No more than 2/10 human samples labeled AI | 0/4 AI | 0/4 AI | 0/4 AI | PARTIAL |
| 2. Score Spread | AI average at least 0.30 higher | 0.106 | 0.106 | 0.106 | MISSED |
| 3. Label Coverage | All 3 labels produced | AI, unsure | AI, unsure | AI, unsure | MISSED |
| 4. Appeal Path | 100% valid appeals recorded as under_review | 1/1 passed | Not tested | Not tested | PARTIAL |
| 5. Invalid Input | 100% return HTTP 400 | 3/3 passed | 3/3 passed | 3/3 passed | PASSED |



**Real output from one trial**, pasted as text, naming the file and function
that produced it:


{
  "status": 200,
  "guess": "unsure",
  "confidence": 0.05,
  "model_score": 0.5066,
  "style_score": 0.4473889556089423,
  "label": "We cannot confidently determine whether this text was written by a person or generated by AI."
}

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

**Criterion 1 — False Positives:** None of my four human-written samples were classified as AI across the three trials. This is encouraging because my goal was to reduce false accusations. However, I only tested four distinct samples instead of ten, so I cannot fully confirm that I met my original target.

**Criterion 2 — Score Spread:** The difference between the average AI and human scores was approximately 0.106, below my target of 0.3. I believe the problem is related to how the model and stylometry signals overlap. The combining rule did not separate the two types of writing enough, which caused many AI-generated samples to fall into the unsure category.

**Criterion 3 — Label Coverage:** The detector produced AI and unsure labels but never human. This suggests that the label mapping or score thresholds may be too restrictive for the human category. I would investigate the thresholds and test more diverse human-written samples before making adjustments.

**Criterion 4 — Appeal Path:** I verified that a valid appeal received an under_review status and was recorded in the audit log with the content ID, creator ID, reasoning, and timestamp. This demonstrates that the appeal process worked for the request I tested. However, I only verified one appeal, so additional testing would be needed to confirm that it works consistently across three trials.

**Criterion 5 — Invalid Input:** All three trials passed, with the application returning HTTP 400 for empty, missing, and null text submissions. This shows that the input validation in my `/submit` route correctly rejects invalid requests without crashing the application. No changes were needed for this criterion.
---

## The Improvement


I adjusted the `HUMAN_THRESHOLD` in `config.py` from `0.35` to `0.45` to improve how the detector identifies human-written text. Before the change, all four human-written samples were classified as `unsure`. After the change, one sample was correctly classified as `human`, while the other three remained `unsure`.

I ran the evaluation again across three trials. None of the four human-written samples were incorrectly classified as AI, and all invalid-input tests continued returning HTTP 400. However, the score spread between human and AI-generated writing remained below the target of 0.30, and the label coverage test still did not produce all three labels.

This improvement helped the detector recognize some human-written text without increasing false positives in the tested samples. However, more testing with a larger and more diverse dataset is needed before concluding that the adjustment improves overall reliability.

**What I changed:**

I changed the `HUMAN_THRESHOLD` in `config.py` from `0.35` to `0.45` to help the detector better recognize human-written text. I kept the AI threshold at `0.65`.

**Which diagnosis pointed at it:**

During the initial evaluation, all four human-written samples were classified as `unsure`. This suggested that the threshold was too restrictive for identifying human writing. I wanted to see whether adjusting it would improve classification without increasing false accusations.



### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->


I reran the three attacks after changing the human classification threshold from `0.35` to `0.45`.

- **Paraphrasing:** HTTP 200, classified as `unsure`. No change from the original test.
- **Informal writing:** HTTP 200, classified as `human`. Previously classified as `unsure`.
- **Repetition:** HTTP 200, classified as `ai`. No change from the original test.

The results were saved in `results/attack_run_2026-11-13_1729_after.md`.

**Did it help, and how do I know:**

The threshold adjustment helped the detector recognize informal writing as human rather than uncertain. However, paraphrasing remained uncertain, and repetitive writing was still classified as AI, showing a potential false-positive risk.

The improvement made the detector more willing to identify human writing, but it did not resolve all the weaknesses identified in the attack tests. More diverse examples and further evaluation would be necessary before using this system in a real-world setting.



<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->
The attack tests showed that the detector still struggles with certain writing styles. Paraphrasing and informal writing both returned "unsure," suggesting that the model cannot always confidently distinguish between human and AI-generated text. Repetitive writing was classified as AI, which also raises concerns about potentially accusing human writers.

To improve the system, I would test it with a larger and more diverse dataset, adjust the classification thresholds, and evaluate false positives and false negatives. I stopped at this stage because the current tests identified limitations that would require more extensive evaluation.

**The trade I'd make if this ran for real:**

I would prioritize reducing false accusations against human writers, even if that means allowing more AI-generated content through. Students, job applicants, and other people whose writing is evaluated would bear the consequences of incorrect accusations.




<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->
rate limit
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
---
## MCP Integration

MCP integration was not implemented in this version of the project. The application continues to use its existing Flask API endpoints. I prioritized testing the detection system, rate limiting, and audit logging. Adding MCP would be a possible future improvement.



## Unit 9 Capstone — Linguistic Pattern Analysis

### Project Overview

For my Unit 9 capstone, I decided to extend my existing Provenance Guard application by adding a linguistic pattern analyzer. While working on the previous units, I noticed that detecting AI-generated writing is not always straightforward. Some human-written passages can be incorrectly classified as AI, while AI-generated text can sometimes appear human-like.

I wanted to explore whether examining additional linguistic features could provide more context about a classification rather than relying solely on the model and stylometry scores.

### What I Added

I created `linguistic_patterns.py` to identify four types of writing patterns:

- **AI-associated vocabulary:** Words such as "delve," "intricate," and "landscape."
- **Em dashes:** Counts occurrences of the em dash (—).
- **Oxford commas:** Identifies potential Oxford comma patterns.
- **Negative parallelism:** Looks for constructions such as "not just ..., but ..."

The analyzer runs alongside my existing GPT-2 detector and stylometry functions. The API now returns these linguistic features with the classification results.

I intentionally kept these features separate from the final classification score because the presence of a particular word or punctuation mark does not prove that a passage was generated by AI. Before assigning additional weight to these features, I would want to evaluate whether they improve classification accuracy without increasing false positives.


### Evaluation and Results

To evaluate my new linguistic analyzer, I created 20 test cases covering AI-associated vocabulary, em dashes, Oxford commas, negative parallelism, and passages without the selected patterns. All 20 tests passed, giving me a 100% pass rate on these specific checks. However, this does not mean the system can detect AI-generated writing with 100% accuracy.

I also compared 20 human-written passages with 20 AI-generated passages to understand how my existing detector performed.

| Classification | Human Writing (20) | AI Writing (20) |
|---|---:|---:|
| Human | 11 | 4 |
| AI | 1 | 8 |
| Unsure | 8 | 8 |

One human-written passage was incorrectly classified as AI, resulting in a 5% false-positive rate on this small dataset. I investigated this example and found that both the GPT-2 model and stylometry signals contributed to the incorrect classification.

Interestingly, none of the 40 comparison passages contained the four monitored linguistic patterns. This highlighted an important limitation: short passages may not provide enough linguistic evidence for meaningful pattern analysis.

**What worked:** The analyzer passed all 20 selected pattern tests, and the API successfully processed all 40 comparison submissions when requests were paced to respect rate limits.

**What did not work:** I did not achieve my target of improving balanced classification accuracy by at least three percentage points. Because the new linguistic features were not incorporated into the classification formula, they did not change the detector's predictions.

These results reinforced the importance of evaluating new features before using them to make decisions that could negatively affect human writers.


### Observability and Debugging

For Unit 9, I extended my existing audit logging system to make it easier to monitor the application and investigate incorrect classifications. Each successful submission now records the prediction, model and style scores, processing time, HTTP status, and counts of the linguistic patterns detected.

During testing, I verified that these fields appeared in the audit log. One submission took approximately 9.49 seconds to process. Although this was only one measurement, it showed why monitoring response time is important.

I also discovered a bug while testing invalid API requests. When I submitted a JSON list instead of an object, the application returned HTTP 500 because the code attempted to call `.get()` on a Python list. I added an `isinstance(payload, dict)` validation check and repeated the same test. The API then correctly returned HTTP 400.

This debugging process helped me understand the importance of testing not only successful requests but also unexpected inputs.

### Cost and Performance Considerations

My application currently runs locally using Flask and GPT-2. The linguistic pattern analyzer uses Python string matching and regular expressions, so it does not require additional model inference or paid API calls.

However, running GPT-2 still requires computing resources, and response time could become a challenge if multiple users submit text simultaneously. My comparison script also needed a seven-second delay between requests to avoid exceeding the configured rate limit of 10 requests per minute.

For a larger deployment, I would investigate model caching, response-time monitoring, persistent rate-limit storage, and more efficient inference. I would also consider the storage and privacy implications of retaining audit logs.

### Deployment and Reproducibility

The application currently runs locally rather than on a publicly hosted server. The Flask endpoints, audit logs, evaluation scripts, and saved results provide a reproducible local testing workflow.

The main project files include `app.py`, `linguistic_patterns.py`, `evaluate_patterns.py`, `compare_writing.py`, and `unit9_criteria.md`.

A future improvement would be deploying the service to a hosted environment with persistent logging and monitoring.


### How I Used AI — Unit 9

I used Claude to assist with troubleshooting, especially when I repeatedly encountered HTTP errors while testing my API endpoints. It helped me investigate possible causes, understand the error messages, and identify areas of my code that needed improvement. I reviewed the suggestions, made changes to my implementation, and tested the endpoints again to verify that the issues were resolved.

It served as learning and debugging resources throughout the project. I was responsible for evaluating the results, identifying the system's limitations, and deciding which changes were appropriate to implement.

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
