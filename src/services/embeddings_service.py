import os
import numpy as np
import tiktoken
from langchain.text_splitter import TokenTextSplitter
from langchain_openai import OpenAIEmbeddings
from typing import List
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

# Configurar el splitter de texto
text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=103)
openai_api_key = "sk-proj-Fc7IcqjttoKngXxnO1hgT3BlbkFJZpMxWjdXhrvrmNXHMpy9"
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Función auxiliar: calcular el número de tokens
def num_tokens_from_string(string: str, encoding_name="cl100k_base") -> int:
    if not string:
        return 0
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# Función para dividir el texto en fragmentos y calcular embeddings
def generate_chunks_and_embeddings(text):
    token_len = num_tokens_from_string(text)
    if token_len <= 512:
        split_texts = [text]
    else:
        split_texts = text_splitter.split_text(text)
    
    embeddings_list = [embeddings.embed_query(chunk) for chunk in split_texts]
    return split_texts, embeddings_list

def find_similar_embeddings(query_embedding, embeddings_list, limit=5):
    """
    Encuentra embeddings similares comparando el embedding de la consulta con una lista de embeddings almacenados.
    """
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    similarities = []
    for embedding in embeddings_list:
        similarity = cosine_similarity(query_embedding, embedding)
        similarities.append((embedding, similarity))

    # Ordenar por similaridad en orden descendente
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Filtrar resultados por un umbral de similaridad si es necesario (opcional)
    similarity_threshold = 0.7
    most_similar_embeddings = [(emb, sim) for emb, sim in similarities if sim >= similarity_threshold]

    # Limitar el número de resultados
    return most_similar_embeddings[:limit]


def prepare_context(entries):
    """ Prepara el contexto combinando todas las entradas del paciente incluyendo fechas y detalles relevantes. """
    context_texts = []

    for entry in entries:
        entry_details = [
            f"Record: {entry.record}",
            f"Date of Visit: {entry.date_of_visit.strftime('%Y-%m-%d') if entry.date_of_visit else 'N/A'}",
            f"Time of Visit: {entry.time_of_visit.strftime('%H:%M:%S') if entry.time_of_visit else 'N/A'}",
            f"Visit Type: {entry.visit_type}",
            f"Symptoms: {entry.symptoms if entry.symptoms else 'N/A'}",
            f"Diagnosis: {entry.diagnosis if entry.diagnosis else 'N/A'}",
            f"Treatment: {entry.treatment if entry.treatment else 'N/A'}",
            f"Prescribed Medications: {entry.prescribed_medications if entry.prescribed_medications else 'N/A'}",
            f"Follow Up Needed: {'Yes' if entry.follow_up_needed else 'No'}",
            f"Follow Up Date: {entry.follow_up_date.strftime('%Y-%m-%d') if entry.follow_up_date else 'N/A'}"
        ]

        context_text = ". ".join(entry_details)
        context_texts.append(context_text)

    # Combine all entries into a single context string
    combined_context = " || ".join(context_texts)
    return combined_context