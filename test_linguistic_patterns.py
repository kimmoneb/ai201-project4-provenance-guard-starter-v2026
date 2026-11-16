
from linguistic_patterns import analyze_patterns


def test_vocabulary():
    result = analyze_patterns(
        "We need to delve into this intricate problem."
    )
    assert result["ai_vocabulary"] == ["delve", "intricate"]


def test_em_dash():
    result = analyze_patterns(
        "I went outside—it was raining."
    )
    assert result["em_dash_count"] == 1


def test_oxford_comma():
    result = analyze_patterns(
        "I bought apples, bananas, and oranges."
    )
    assert result["oxford_comma_count"] == 1


def test_negative_parallelism():
    result = analyze_patterns(
        "It's not just about speed, but about accuracy."
    )
    assert result["negative_parallelism_count"] == 1


def test_no_patterns():
    result = analyze_patterns(
        "I went to the store yesterday."
    )
    assert result["ai_vocabulary"] == []
    assert result["em_dash_count"] == 0
    assert result["oxford_comma_count"] == 0
    assert result["negative_parallelism_count"] == 0


if __name__ == "__main__":
    test_vocabulary()
    test_em_dash()
    test_oxford_comma()
    test_negative_parallelism()
    test_no_patterns()
    print("All 5 linguistic pattern tests passed!")
