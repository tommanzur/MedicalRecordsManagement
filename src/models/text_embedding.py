from pgvector.sqlalchemy import Vector
from models import db

class TextEmbedding(db.Model):
    __tablename__ = 'text_embedding'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    vector = db.Column(Vector(1536))

    notes = db.relationship('Note', back_populates='embeddings')

    def __init__(self, note_id, entry_id, patient_id, text, vector):
        self.note_id = note_id
        self.entry_id = entry_id
        self.patient_id = patient_id
        self.text = text
        self.vector = vector
