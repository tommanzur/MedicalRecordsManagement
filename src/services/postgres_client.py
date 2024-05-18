import os
import bcrypt
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from models import db
from typing import List
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from models.entries_embeddings import EntryEmbedding
from models.note import Note
from models.patient import Patient
from models.entry import Entry
from models.users import User 
from models.conversations import Conversation
from models.text_embedding import TextEmbedding
from services.audio_transcription import complete_missing_fields
from services.embeddings_service import prepare_context, generate_chunks_and_embeddings
from config import CHAT_MODEL
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

class PostgresClient:
    def __init__(self):
        self.database_url = f"postgresql+psycopg2://{os.getenv('DB_USER', 'tu_usuario')}:" \
                            f"{os.getenv('DB_PASSWORD', 'tu_contraseña')}@" \
                            f"{os.getenv('DB_HOST', 'localhost')}/medical_reports_db"
        self.engine = create_engine(self.database_url)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

    def init_db(self):
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
            new_entry = Entry(**kwargs)
            session.add(new_entry)
            session.commit()
            entries_context = prepare_context([new_entry])
            entries_texts, embeddings_list = generate_chunks_and_embeddings(entries_context)
            session.close()
            self.store_entry_embeddings(patient_id=new_entry.patient_id, embeddings=embeddings_list, texts=entries_texts)

            return new_entry.id
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

    def get_entries_of_one_patient(self, patient_id):
        session = self.Session()
        try:
            entries = session.query(Entry).filter(Entry.patient_id == patient_id).all()
            return entries
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
                    setattr(entry, key, value)
                session.commit()
                session.add(entry)    
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

    def add_note_to_entry(self, entry_id, text):
        session = self.Session()
        try:
            note = Note(entry_id=entry_id, text=text)
            session.add(note)
            session.commit()
            note_id = note.id
            split_texts, embeddings_list = generate_chunks_and_embeddings(text)
            entry = session.query(Entry).get(entry_id)

            for split_text, embedding_vector in zip(split_texts, embeddings_list):

                text_embedding = TextEmbedding(
                    note_id=note_id,
                    patient_id=entry.patient_id,
                    entry_id=entry_id,
                    text=split_text,
                    vector=embedding_vector
                )
                session.add(text_embedding)
            session.commit()

            completed_fields = complete_missing_fields(entry, text, date=entry.date_of_visit)
            if completed_fields:
                self.update_entry(entry_id, **completed_fields)

            return True
        
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Failed to add note: {e}")
            return False
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
            session = self.Session()
            conversation = Conversation(patient_id=patient_id, session_id=session_id)
            session.add(conversation)
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
            conversation = session.query(Conversation).all()
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

    def add_message_to_conversation(self, conv_id, message_content, patient_id):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            conversation = session.query(Conversation).get(conv_id)

            if not conversation:
                return None

            user_message = {"role": "user", "content": message_content}
            history = conversation.messages
            conversation.messages.append(user_message)

            chat_model = CHAT_MODEL
            prompt = ChatPromptTemplate.from_template(
                """
                Answer the following question based only on the provided context and the chat history:
                <context>
                {context}
                </context>
                <chat_history>
                {chat_history}
                </chat_history>
                Question: {input}
                """
            )

            document_chain = create_stuff_documents_chain(chat_model, prompt)
            retrieved_docs = self.retriever(
                query=message_content,
                patient_id=patient_id,
                run_manager=None
                )
            response = document_chain.invoke({
                "input": message_content,
                "context": retrieved_docs,
                "chat_history": history,
            })

            ai_message = {"role": "bot", "content": response}
            conversation.messages.append(ai_message)
            session.add(conversation)
            session.commit()
            return response

        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

    def get_embeddings_for_patient(self, patient_id):
        session = self.Session()
        try:
            embeddings = session.query(TextEmbedding).filter(TextEmbedding.patient_id == patient_id).all()
            return embeddings
        except SQLAlchemyError as e:
            print(f"Failed to retrieve embeddings: {e}")
            return None
        finally:
            session.close()

    def get_entry_embeddings(self, patient_id):
        """Recupera los embeddings de las entradas del paciente desde la base de datos."""
        session = self.Session()
        try:
            embeddings = session.query(EntryEmbedding).filter(EntryEmbedding.patient_id == patient_id).all()
            return [embedding.vector for embedding in embeddings]
        except SQLAlchemyError as e:
            print(f"Failed to retrieve entry embeddings: {e}")
            return None
        finally:
            session.close()

    def store_entry_embeddings(self, patient_id, embeddings, texts):
        """Almacena los embeddings de las entradas del paciente en la base de datos."""
        session = self.Session()
        try:
            for text, embedding in zip(texts, embeddings):
                entry_embedding = EntryEmbedding(patient_id=patient_id, text=text, vector=embedding)
                session.add(entry_embedding)
                session.commit()
        except SQLAlchemyError as e:
            print(f"Failed to store entry embeddings: {e}")
        finally:
            session.close()

    def search_similar_entries(self, query_embedding, patient_id=None, limit=5):
        session = self.Session()
        try:
            # Construir la consulta para la tabla text_embedding
            text_embedding_query = (
                session.query(TextEmbedding)
                .filter(TextEmbedding.patient_id == patient_id)
                .order_by(TextEmbedding.vector.l2_distance(query_embedding))
                .limit(limit)
            )

            # Ejecutar la consulta y obtener los resultados
            text_embedding_results = text_embedding_query.all()

            # Construir la consulta para la tabla entry_embeddings
            entry_embeddings_query = (
                session.query(EntryEmbedding)
                .filter(EntryEmbedding.patient_id == patient_id)
                .order_by(EntryEmbedding.vector.l2_distance(query_embedding))
                .limit(limit)
            )
            text_embedding_results.extend(entry_embeddings_query)
            return text_embedding_results
        
        except SQLAlchemyError as e:
            print(f"Failed to execute search query: {e}")
            return []
        finally:
            session.close()

    def retriever(self, query: str, patient_id, run_manager: CallbackManagerForRetrieverRun) -> List[Document]:
        split_texts, query_embeddings = generate_chunks_and_embeddings(query)
        query_embedding = query_embeddings[0]  # Usar el primer embedding generado

        similar_notes = self.search_similar_entries(query_embedding, patient_id=patient_id, limit=5)
        documents = [
            Document(
                page_content=note.text)
            for note in similar_notes
        ]
        return documents
    
    def add_user(self, username, password):
        session = self.Session()
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_user = User(username=username, password=hashed_password.decode('utf-8'))
            session.add(new_user)
            session.commit()
            return new_user.id
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()
            
    def get_user_by_username(self, username):
        session = self.Session()
        try:
            user = session.query(User).filter(User.username == username).first()
            return user
        finally:
            session.close()

    def delete_user(self, user_id):
        session = self.Session()
        try:
            user = session.query(User).get(user_id)
            if user:
                session.delete(user)
                session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

    def update_user_password(self, username, new_password):
        session = self.Session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                user.password = hashed_password
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

client = PostgresClient()
client.init_db()
