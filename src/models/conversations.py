from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from models import db
from sqlalchemy.ext.mutable import MutableList


class Conversation(db.Model):
    __tablename__ = 'conversation'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    session_id = db.Column(db.String(36), nullable=False)
    messages = db.Column(MutableList.as_mutable(JSON) , nullable=True, default=[])
    
    patient = db.relationship('Patient', back_populates='conversations')

    def __init__(self, patient_id, session_id, messages=None, *args, **kwargs):
        super(Conversation, self).__init__(*args, **kwargs)
        self.patient_id = patient_id
        self.session_id = session_id
        if messages is None:
            self.messages = []

