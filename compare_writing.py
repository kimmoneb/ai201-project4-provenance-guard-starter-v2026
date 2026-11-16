import time
import csv
import json
import urllib.request
import urllib.error
from collections import Counter

API_URL = "http://127.0.0.1:5000/submit"

results = []

with open("writing_comparison.csv", newline="", encoding="utf-8") as file:
    samples = list(csv.DictReader(file))

for sample in samples:
    time.sleep(7)
    payload = json.dumps({
        "text": sample["text"],
        "creator_id": "unit9_comparison"
    }).encode("utf-8")

    request = urllib.request.Request(
        API_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            prediction = json.load(response)

        results.append({
            "id": sample["id"],
            "actual": sample["source"],
            "predicted": prediction["guess"],
            "patterns": prediction["linguistic_patterns"]
        })

    except urllib.error.HTTPError as error:
        print(f"Sample {sample['id']} failed: HTTP {error.code}")

# Save the successful results for later analysis
with open("writing_comparison_results.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=2)

print(f"\nSuccessfully analyzed {len(results)} of {len(samples)} samples.")

for source in ["human", "ai"]:
    group = [r for r in results if r["actual"] == source]
    counts = Counter(r["predicted"] for r in group)

    print(f"\n{source.upper()} WRITING ({len(group)} samples)")
    print(f"  Classified human: {counts['human']}")
    print(f"  Classified AI:    {counts['ai']}")
    print(f"  Classified unsure:{counts['unsure']}")

    if group:
        print(
            "  Average em dashes:",
            round(
                sum(r["patterns"]["em_dash_count"] for r in group)
                / len(group), 2
            )
        )
        print(
            "  Average AI vocabulary matches:",
            round(
                sum(len(r["patterns"]["ai_vocabulary"]) for r in group)
                / len(group), 2
            )
        )

        print(
    "  Average Oxford commas:",
    round(
        sum(r["patterns"]["oxford_comma_count"] for r in group)
        / len(group), 2
    )

    
    )

    print(
        "  Average negative parallelism:",
        round(
            sum(r["patterns"]["negative_parallelism_count"] for r in group)
            / len(group), 2
        )
    )
