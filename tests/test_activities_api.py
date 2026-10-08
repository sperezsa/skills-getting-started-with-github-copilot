def test_get_activities_returns_all_activities(client, activities_data):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == activities_data


def test_signup_adds_participant(client, activities_data):
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_signup_rejects_duplicate_participant(client, activities_data):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert activities_data[activity_name]["participants"].count(email) == 1


def test_signup_rejects_unknown_activity(client):
    response = client.post(
        "/activities/Unknown%20Activity/signup",
        params={"email": "new.student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant(client, activities_data):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }
    assert email not in client.get("/activities").json()[activity_name]["participants"]
    assert "daniel@mergington.edu" in activities_data[activity_name]["participants"]


def test_remove_participant_from_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown%20Activity/participants/student%40mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_rejects_unregistered_student(client):
    response = client.delete(
        "/activities/Chess%20Club/participants/unknown%40mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
