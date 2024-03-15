from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    emergency_contact_name = db.Column(db.String(100), nullable=True)
    emergency_contact_phone = db.Column(db.String(20), nullable=True)
    medical_record_number = db.Column(db.String(50), nullable=True)
    insurance_provider = db.Column(db.String(100), nullable=True)
    insurance_policy_number = db.Column(db.String(50), nullable=True)
    
    entries = db.relationship('Entry', backref='patient', lazy=True)

