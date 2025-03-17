from src.analyzer import analyze_user
from src.auth import get_api

def test_analyze_user():
    api = get_api()
    result = analyze_user(api, "elonmusk")  # Test with a known user
    assert result in ["larping", "genuine", "unknown"], "Analysis returned invalid result"
    print(f"Test passed: Analyzed elonmusk as {result}")

if __name__ == "__main__":
    test_analyze_user()