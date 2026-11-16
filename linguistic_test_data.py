
# Test passages with manually specified expected patterns.
# These are synthetic examples for testing detection,
# not evidence that a passage was written by AI.

TEST_CASES = [
    {"text": "We need to delve into this issue.", "expected": {"ai_vocabulary": ["delve"]}},
    {"text": "The intricate design took months.", "expected": {"ai_vocabulary": ["intricate"]}},
    {"text": "This was a pivotal moment.", "expected": {"ai_vocabulary": ["pivotal"]}},
    {"text": "The landscape changed quickly.", "expected": {"ai_vocabulary": ["landscape"]}},
    {"text": "The interplay between these factors matters.", "expected": {"ai_vocabulary": ["interplay"]}},
    {"text": "These results underscore the problem.", "expected": {"ai_vocabulary": ["underscore"]}},
    {"text": "I was tired—really tired.", "expected": {"em_dash_count": 1}},
    {"text": "She laughed—and then cried.", "expected": {"em_dash_count": 1}},
    {"text": "Wait—what happened?", "expected": {"em_dash_count": 1}},
    {"text": "The plan—although risky—worked.", "expected": {"em_dash_count": 2}},
    {"text": "I bought tea, coffee, and milk.", "expected": {"oxford_comma_count": 1}},
    {"text": "We studied Python, SQL, and Java.", "expected": {"oxford_comma_count": 1}},
    {"text": "She likes reading, writing, and coding.", "expected": {"oxford_comma_count": 1}},
    {"text": "Bring paper, pens, or pencils.", "expected": {"oxford_comma_count": 1}},
    {"text": "It's not just about speed, but about safety.", "expected": {"negative_parallelism_count": 1}},
    {"text": "This is not only useful, but necessary.", "expected": {"negative_parallelism_count": 1}},
    {"text": "We need not just data, but context.", "expected": {"negative_parallelism_count": 1}},
    {"text": "It's not just a tool, but a responsibility.", "expected": {"negative_parallelism_count": 1}},
    {"text": "I went to the store yesterday.", "expected": {}},
    {"text": "The dog slept beside the window.", "expected": {}},
]
