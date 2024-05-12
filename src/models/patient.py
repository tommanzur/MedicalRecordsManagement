from flask_sqlalchemy import SQLAlchemy
from models import db

class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(20))
    medical_record_number = db.Column(db.String(50))
    insurance_provider = db.Column(db.String(100))
    insurance_policy_number = db.Column(db.String(50))
    conversations = db.relationship('Conversation', back_populates='patient', lazy=True)
    entries = db.relationship('Entry', backref='patient', lazy=True)