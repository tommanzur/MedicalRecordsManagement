from models.patient import db

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
    notes = db.Column(db.Text, nullable=True)

    patient = db.relationship('Patient', backref=db.backref('entries', lazy=True))
