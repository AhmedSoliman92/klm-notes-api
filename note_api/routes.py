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


@app.route("/notes/<int:id>", methods=["GET"])
def get_note(id):
    """Retrieve single note by note id

    Args:
        id (int): id of note

    Returns:
        Response: Flask reponse  with note details and 200 code.
        error message and 404 code in case is not exist.
    """
    note = db.session.get(Note, id)
    print(note)
    if not note:
        return jsonify({"error": "Note not found"}), 404
    return jsonify(note.to_dict()), 200


@app.route("/notes/<int:id>", methods=["PUT"])
def update_note(id):
    """Update the title and/or content of an existing note.
    Args:
        id (int): _description_

    Returns:
        Response: Flask reponse  with note details and 200 code.
        error message and 404 code in case is not exist or 400 code
        if it's invalid.
    """
    note = db.session.get(Note, id)
    if not note:
        return jsonify({"error": "Note not found"}), 404
    data = request.get_json()
    if not data or ("title" not in data and "content" not in data):
        return jsonify({"error": "Invalid request"}), 400
    if data.get("title"):
        note.title = data["title"]
    if data.get("content"):
        note.content = data["content"]
    db.session.commit()
    return jsonify({"message": "Note updated successfully"}), 200
