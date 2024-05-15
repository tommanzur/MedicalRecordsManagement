from flask_sqlalchemy import SQLAlchemy
from models import db

class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    entry = db.relationship('Entry', back_populates='notes')