from note_api import db


def test_config(app):
    """Check if flask app is configured correctly for testing.

    Args:
        app (Flask): flask app instance for testing.
    """
    assert app.testing
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"


def test_create_note_success(client):
    """Test successful creation of a new note via POST request.
    Args:
        client (FlaskClient): To test http request.
    """
    response = client.post(
        "/notes",
        json={"title": "Test Note", "content": "This is content for testing."},
    )

    assert response.status_code == 201

    assert "Note created successfully" in response.get_data(as_text=True)


def test_create_note_invalid_data(client):
    """Test failure when required fields are missing."""

    response = client.post(
        "/notes",
        json={"title": "Missing content"},
        content_type="application/json",
    )
    assert response.status_code == 400
    assert "Invalid request" in response.get_data(as_text=True)
