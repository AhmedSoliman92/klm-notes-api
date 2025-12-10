from note_api import db
from note_api.models import Note


def test_config(app):
    """Check if flask app is configured correctly for testing.

    Args:
        app (Flask): flask app instance for testing.
    """
    assert app.testing
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"


def test_get_notes_empty(client):
    """Test retrieving notes when the database is empty.

    Args:
        client (FlaskClient): To test http request.
    """

    response = client.get("/notes")
    assert response.status_code == 200
    assert response.get_json() == []


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


def test_get_notes_with_data(client, app):
    """Test retrieving notes after one has been created directly via the DB.

    Args:
        app (Flask): flask app instance for testing.
        client (FlaskClient): To test http request.
    """

    with app.app_context():
        db.session.add(Note(title="In-DB Test", content="Data Check"))
        db.session.commit()

    response = client.get("/notes")
    assert response.status_code == 200
    data = response.get_json()

    # Check the returned list size and content
    assert len(data) == 2
    assert data[1]["title"] == "In-DB Test"
    assert "id" in data[1]


def test_get_note_success(client, app):
    """
    Test retrieving an existing note by id.

    Args:
        client (FlaskClient): To test http request.
        app (Flask): flask app instance for testing.
    """
    with app.app_context():
        note = Note(title="Test Note", content="Test Content")
        db.session.add(note)
        db.session.commit()
        note_id = note.id

    response = client.get(f"/notes/{note_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == note_id
    assert data["title"] == "Test Note"
    assert data["content"] == "Test Content"


def test_get_note_not_found(client):
    """
    Test retrieving a note that does not exist.

    Args:
        client (FlaskClient): To test http request.
    """
    response = client.get("/notes/9999")
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Note not found"
