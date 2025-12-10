from . import db


class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def to_dict(self):
        """Convert Note model  to serialized dictionarty

        Returns:
            serialized_model (dict) : A dictionary containing the note's `id`,
                `title`, and `content`.
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
        }
