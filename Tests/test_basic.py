import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app


def test_index():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["message"] == "LMS backend is running"
