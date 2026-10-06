EXPECTED_FIELDS = {"description", "schedule", "max_participants", "participants"}


def test_get_activities_returns_all_activities_with_expected_fields(client):
    # Arrange
    expected_names = {"Chess Club", "Programming Class", "Gym Class"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert expected_names <= set(activities)
    for details in activities.values():
        assert EXPECTED_FIELDS <= set(details)


def test_signup_new_student_returns_success_message(client):
    # Arrange
    activity_name = "Soccer Team"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}


def test_signup_new_student_adds_participant_to_activity(client):
    # Arrange
    activity_name = "Soccer Team"
    email = "new.student@mergington.edu"

    # Act
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    participants = client.get("/activities").json()[activity_name]["participants"]
    assert email in participants


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Underwater Basket Weaving"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": "student@mergington.edu"}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_duplicate_student_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": existing_email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_duplicate_student_does_not_add_second_entry(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    participants = client.get("/activities").json()[activity_name]["participants"]
    assert participants.count(existing_email) == 1


def test_signup_activity_name_with_space_is_url_decoded(client):
    # Arrange
    activity_name = "Programming Class"
    email = "space.test@mergington.edu"

    # Act
    response = client.post(
        "/activities/Programming%20Class/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    participants = client.get("/activities").json()[activity_name]["participants"]
    assert email in participants


def test_unregister_signed_up_student_returns_success_message(client):
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}


def test_unregister_signed_up_student_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"

    # Act
    client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    participants = client.get("/activities").json()[activity_name]["participants"]
    assert email not in participants


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Underwater Basket Weaving"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup", params={"email": "student@mergington.edu"}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_student_not_signed_up_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.registered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}


def test_unregister_student_after_signup_removes_them(client):
    # Arrange
    activity_name = "Soccer Team"
    email = "round.trip@mergington.edu"
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    participants = client.get("/activities").json()[activity_name]["participants"]
    assert email not in participants
