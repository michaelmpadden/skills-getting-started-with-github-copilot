def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_static_index_page_is_served(client):
    # Arrange
    path = "/static/index.html"

    # Act
    response = client.get(path)

    # Assert
    assert response.status_code == 200
    assert "Mergington High School" in response.text


def test_static_files_are_served_with_no_cache_header(client):
    # Arrange
    path = "/static/app.js"

    # Act
    response = client.get(path)

    # Assert
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-cache"


def test_api_responses_do_not_get_no_cache_header(client):
    # Arrange
    path = "/activities"

    # Act
    response = client.get(path)

    # Assert
    assert "cache-control" not in response.headers
