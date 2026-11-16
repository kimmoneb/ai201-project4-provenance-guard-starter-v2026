
from linguistic_patterns import analyze_patterns
from linguistic_test_data import TEST_CASES

passed = 0

for i, case in enumerate(TEST_CASES, start=1):
    actual = analyze_patterns(case["text"])
    expected = case["expected"]

    # Compare only the fields specified in each test case
    correct = all(
        actual[key] == value
        for key, value in expected.items()
    )

    if correct:
        passed += 1

    print(f"Sample {i}: {'PASS' if correct else 'FAIL'}")

accuracy = passed / len(TEST_CASES) * 100

print(f"\nPattern detection tests: {passed}/{len(TEST_CASES)}")
print(f"Pass rate: {accuracy:.1f}%")
