import requests

def test_greet_injection_attempt():
    malicious_input = "<script>alert('x')</script>"
    r = requests.get(f"http://localhost:5000/greet?name={malicious_input}")
    assert r.status_code == 200
    # The response should not contain raw script tags
    assert "<script>" not in r.text
    assert "alert" not in r.text