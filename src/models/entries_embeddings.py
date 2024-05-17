from models import db
from pgvector.sqlalchemy import Vector

class EntryEmbedding(db.Model):
    __tablename__ = 'entry_embeddings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    vector = db.Column(Vector(1536), nullable=False)

    def __init__(self, patient_id, text, vector):
        self.patient_id = patient_id
        self.text = text
        self.vector = vector
