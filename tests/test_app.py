from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # Ensure known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Test Club"
    email = "tester@example.com"

    # set up a test activity
    activities[activity] = {
        "description": "Test activity",
        "schedule": "Now",
        "max_participants": 5,
        "participants": []
    }

    # Signup
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 400

    # Unregister
    res = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert res.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregistering again should return 404
    res = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert res.status_code == 404

    # Clean up
    del activities[activity]
