from sqlalchemy import JSON
from models import db

class Entry(db.Model):

    __tablename__ = 'entry'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    record = db.Column(db.Text, nullable=False)
    date_of_visit = db.Column(db.Date, nullable=False)
    time_of_visit = db.Column(db.Time, nullable=True)
    visit_type = db.Column(db.String(100), nullable=False)
    symptoms = db.Column(db.Text, nullable=True)
    diagnosis = db.Column(db.Text, nullable=True)
    treatment = db.Column(db.Text, nullable=True)
    prescribed_medications = db.Column(db.Text, nullable=True)
    follow_up_needed = db.Column(db.Boolean, nullable=True)
    follow_up_date = db.Column(db.Date, nullable=True)
    attached = db.Column(JSON, nullable=True)

    notes = db.relationship('Note', back_populates='entry', cascade='all, delete-orphan')
