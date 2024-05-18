from datetime import datetime
from sqlalchemy import JSON
from models import db

class Entry(db.Model):

    __tablename__ = 'entry'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date_of_visit = db.Column(db.Date, nullable=False, default=datetime.today())
    time_of_visit = db.Column(db.Time, nullable=True)
    visit_type = db.Column(db.String(100), nullable=True)
    symptoms = db.Column(db.Text, nullable=True)
    diagnosis = db.Column(db.Text, nullable=True)
    treatment = db.Column(db.Text, nullable=True)
    prescribed_medications = db.Column(db.Text, nullable=True)
    follow_up_needed = db.Column(db.Boolean, nullable=True)
    follow_up_date = db.Column(db.Date, nullable=True)
    attached = db.Column(JSON, nullable=True)

    notes = db.relationship('Note', back_populates='entry', cascade='all, delete-orphan')

    def __init__(self, patient_id, date_of_visit=None, time_of_visit=None):
        self.patient_id = patient_id
        if not date_of_visit:
            self.date_of_visit = datetime.today()
        else:
            self.date_of_visit = date_of_visit
        if not time_of_visit:
            now = datetime.now()
            self.time_of_visit = now.replace(second=0, microsecond=0)
        else:
            self.time_of_visit = time_of_visit
