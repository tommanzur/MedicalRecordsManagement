import json
import os
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.patient import Patient
from models.entry import Entry
from models.conversations import Conversation

class PostgresClient:
    def __init__(self):
        self.database_url = f"postgresql://{os.getenv('DB_USER', 'tu_usuario')}:" \
                            f"{os.getenv('DB_PASSWORD', 'tu_contraseña')}@" \
                            f"{os.getenv('DB_HOST', 'localhost')}/medical_reports_db"
        self.engine = create_engine(self.database_url)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

    def init_db(self):
        db.metadata.create_all(self.engine)
        db.metadata.create_all(self.engine)

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

    def get_all_patients(self):
        """Obtiene una lista de todos los pacientes."""
        session = self.Session()
        try:
            patients = session.query(Patient).all()
            return patients
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
            if 'notes' in kwargs and kwargs['notes'] is not None:
                if not isinstance(kwargs['notes'], list):
                    kwargs['notes'] = [kwargs['notes']]
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

    def get_all_entries(self):
        """Obtiene una lista de todas las entradas."""
        session = self.Session()
        try:
            entries = session.query(Entry).all()
            return entries
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

    def update_entry(self, entry_id, **kwargs):
        session = self.Session()
        try:
            entry = session.query(Entry).get(entry_id)
            if entry:
                for key, value in kwargs.items():
                    if key == 'notes':
                        current_notes = entry.notes
                        if isinstance(current_notes, str):
                            current_notes = json.loads(current_notes) if current_notes else []
                        if value:
                            current_notes.append(value)
                        setattr(entry, key, current_notes)
                    else:
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

    def add_conversation(self, patient_id, session_id):
        session = self.Session()
        try:
            new_conversation = Conversation(patient_id=patient_id, session_id=session_id)
            session.add(new_conversation)
            session.commit()
            return {'message': 'Conversation created'}
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

    def get_all_conversations(self):
        """Obtiene una lista de todas las conversaciones."""
        session = self.Session()
        try:
            conversation = session.query(Conversation)
            return conversation
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

    def get_conversation_by_id(self, conv_id):
        session = self.Session()
        try:
            conversation = session.query(Conversation).get(conv_id)
            return conversation
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

    def add_message_to_conversation(self, conv_id, message):
        """Añade un mensaje a una conversación existente."""
        session = self.Session()
        try:
            conversation = session.query(Conversation).get(conv_id)
            if conversation:
                current_messages = conversation.messages
                if isinstance(current_messages, str):
                    current_messages = json.loads(conversation.messages) if conversation.messages else []
                if message:
                    current_messages.append(message)
                    setattr(conversation, "messages", current_messages)
                    session.commit()
                    return conversation

        except SQLAlchemyError as e:
            print(f"SQLAlchemy Error: {e}")
            session.rollback()
            raise
        finally:
            session.close()


client = PostgresClient()
client.init_db()
