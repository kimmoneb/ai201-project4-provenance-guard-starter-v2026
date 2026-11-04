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

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
