import requests

def test_healthz():
    r = requests.get("http://localhost:5000/healthz")
    assert r.status_code == 200


def test_root():
    r = requests.get("http://localhost:5000/")
    assert r.status_code == 200