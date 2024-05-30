from services.openai_client import openai_client
import json

def transcribe_audio(audio_bytes, filename):
    response = openai_client.audio.transcriptions.create(
        file=(filename, audio_bytes),
        model="whisper-1"
    )
    return response.text

def complete_missing_fields(entry, note_transcription, date):
    # Obtener la lista de campos vacíos
    empty_fields = []
    if not entry.visit_type:
        empty_fields.append({'field': 'visit_type', 'type': 'String'})
    if not entry.symptoms:
        empty_fields.append({'field': 'symptoms', 'type': 'Text'})
    if not entry.diagnosis:
        empty_fields.append({'field': 'diagnosis', 'type': 'Text'})
    if not entry.treatment:
        empty_fields.append({'field': 'treatment', 'type': 'Text'})
    if not entry.prescribed_medications:
        empty_fields.append({'field': 'prescribed_medications', 'type': 'Text'})
    if not entry.follow_up_needed or entry.follow_up_needed is False:
        empty_fields.append({'field': 'follow_up_needed', 'type': 'Boolean'})
    if not entry.follow_up_date:
        empty_fields.append({'field': 'follow_up_date', 'type': 'Date'})

    # Generar el prompt para el cliente de OpenAI
    prompt = (
        f"The following is the transcription of a medical note:\n\n"
        f"{note_transcription}\n\n"
        f"The following fields are empty in the patient's entry:\n"
    )
    
    for field in empty_fields:
        prompt += f"- {field['field']} ({field['type']})\n"

    prompt += (
        f"If the necessary information to fill these fields is present in the transcription, "
        f"please extract it and provide up to four words for each field. Do not add new information. "
        f"For the 'visit_type' field, use only one of these options: routine visit, emergency visit, follow-up visit, initial consultation. "
        f"For the 'prescribed_medications' field, use only drug names and commercial drug names. Do not include unknown medication names. "
        f"If there is not enough information for a field, do not include it in the response dictionary. "
        f"Return the response as a dictionary in the following format:\n"
        f"{{\n"
        f"\"field_name\": \"value\",\n"
        f"\"field_name2\": \"value2\"\n"
        f"}}\n\n"
        f"Today's date is {date}. Ensure that the 'follow_up_date' field in the response dictionary always follows the format 'YYYY-MM-DD'."
    )

    # Llamada al cliente de OpenAI para completar los campos faltantes
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a proficient AI with a specialty in extracting specific information from text. Based on the provided transcription, identify and extract the necessary information to fill in the missing fields in the patient's record. Each field should be filled with a short sentence if the information is available in the transcription."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    completion = response.choices[0].message.content
    completed_fields = json.loads(completion)

    return completed_fields
