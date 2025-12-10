import pytest

from note_api import create_app, db


@pytest.fixture(scope="session")
def app():
    """Create a fresh app instance for the test

    Yields:
        app (Flask): Flask app instance for testing.
    """
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    """HTTP requests simulation

    Args:
        app (Flask): flask app instance for test

    Returns:
        FlaskClient: client instance for simulate http request.
    """
    return app.test_client()


@pytest.fixture()
def runner(app):
    """Testing command-line commands.

    Args:
        app (Flask): flask app instance for test

    Returns:
        FlaskCliRunner: A test runner instance to invoke CLI commands
    """
    return app.test_cli_runner()
