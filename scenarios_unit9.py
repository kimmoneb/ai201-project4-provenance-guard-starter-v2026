import csv

from linguistic_test_data import TEST_CASES


with open("writing_comparison.csv", newline="", encoding="utf-8") as file:
    writing_samples = list(csv.DictReader(file))

human_texts = [
    sample["text"]
    for sample in writing_samples
    if sample["source"] == "human"
]

ai_texts = [
    sample["text"]
    for sample in writing_samples
    if sample["source"] == "ai"
]


# Unit 9 capstone evaluation scenarios
SCENARIOS = [
    {
        "name": "Unit 9 - Linguistic Pattern Detection",
        "criterion": 1,
        "texts": [case["text"] for case in TEST_CASES],
    },
    {
    "name": "Unit 9 - Human Writing False Positives",
    "criterion": 2,
    "texts": human_texts,
    },
    {
        "name": "Unit 9 - Classification Comparison",
        "criterion": 3,
        "texts": human_texts + ai_texts,
    },
    {
        "name": "Unit 9 - API Reliability",
        "criterion": 4,
        "bodies": [
            {
                "text": "This is a valid writing sample for API testing.",
                "creator_id": "unit9_valid"
            },
            {
                "text": "",
                "creator_id": "unit9_empty"
            },
            {
                "text": None,
                "creator_id": "unit9_null"
            },
            {
                "creator_id": "unit9_missing"
            },
            {
                "text": ["invalid", "list"],
                "creator_id": "unit9_invalid_type"
            },
        ],
    },
    {
        "name": "Unit 9 - Observability",
        "criterion": 5,
        "bodies": [
            {
                "text": "The report includes research, analysis, and recommendations.",
                "creator_id": "unit9_observability_valid"
            },
            {
                "text": "",
                "creator_id": "unit9_observability_rejected"
            },
        ],
    },
]


def validate():
    problems = []

    for scenario in SCENARIOS:
        if not scenario.get("name"):
            problems.append("Scenario is missing a name.")

        if not scenario.get("texts") and not scenario.get("bodies"):
            problems.append(
                f"{scenario.get('name', 'Unknown')} has no test inputs."
            )

    return problems