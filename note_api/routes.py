from flask import current_app as app
from flask import jsonify, request

from . import db
from .models import Note


@app.route("/notes", methods=["POST"])
def create_note():
    """Create a new Note and store it in the database.

    Returns:
        Response: Flask reponse  with success message and 201 code.
        or failed message and 400 code in case it's failed.
    """
    data = request.get_json()
    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Invalid request"}), 400

    new_note = Note(title=data["title"], content=data["content"])
    db.session.add(new_note)
    db.session.commit()
    return jsonify({"message": "Note created successfully"}), 201


@app.route("/notes", methods=["GET"])
def get_notes():
    """Fetch all notes.

    Returns:
        Response: Flask reponse  with success message and 200 code.
    """
    notes = Note.query.all()
    return jsonify([note.to_dict() for note in notes]), 200

