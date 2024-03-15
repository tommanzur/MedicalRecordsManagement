import os
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from src.models.patient import Patient, db as patient_db
from src.models.entry import Entry, db as entry_db

class PostgresClient:
    def __init__(self):
        self.database_url = f"postgresql://{os.getenv('DB_USER', 'tu_usuario')}:" \
                            f"{os.getenv('DB_PASSWORD', 'tu_contraseña')}@" \
                            f"{os.getenv('DB_HOST', 'localhost')}/medical_reports_db"
        self.engine = create_engine(self.database_url)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

    def init_db(self):
        patient_db.metadata.create_all(self.engine)
        entry_db.metadata.create_all(self.engine)

    def add_patient(self, **kwargs):
        session = self.Session()
        try:
            new_patient = Patient(**kwargs)
            session.add(new_patient)
            session.commit()
            return new_patient.id
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

    def get_patient(self, patient_id):
        session = self.Session()
        try:
            patient = session.query(Patient).get(patient_id)
            return patient
        finally:
            session.close()

    def update_patient(self, patient_id, **kwargs):
        session = self.Session()
        try:
            patient = session.query(Patient).get(patient_id)
            if patient:
                for key, value in kwargs.items():
                    setattr(patient, key, value)
                session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_patient(self, patient_id):
        session = self.Session()
        try:
            patient = session.query(Patient).get(patient_id)
            if patient:
                session.delete(patient)
                session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

    def add_entry(self, **kwargs):
        session = self.Session()
        try:
            new_entry = Entry(**kwargs)
            session.add(new_entry)
            session.commit()
            return new_entry.id
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

    def get_entry(self, entry_id):
        session = self.Session()
        try:
            entry = session.query(Entry).get(entry_id)
            return entry
        finally:
            session.close()

    def update_entry(self, entry_id, **kwargs):
        session = self.Session()
        try:
            entry = session.query(Entry).get(entry_id)
            if entry:
                for key, value in kwargs.items():
                    setattr(entry, key, value)
                session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_entry(self, entry_id):
        session = self.Session()
        try:
            entry = session.query(Entry).get(entry_id)
            if entry:
                session.delete(entry)
                session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

client = PostgresClient()
client.init_db()
