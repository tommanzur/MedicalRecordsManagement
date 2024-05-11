import json
from flask import jsonify, request
from flask_restx import Resource, Namespace, reqparse
from werkzeug.datastructures import FileStorage
from models.entry import Entry
from services.postgres_client import client
from services.audio_transcription import transcribe_audio, resume_speech

api = Namespace("speech_to_text", description="Speech to text operations")

# Parser for file upload
file_upload = reqparse.RequestParser()
file_upload.add_argument(
    "audio", type=FileStorage, location="files", required=True, help="Audio file"
)


@api.route("/<int:entry_id>")
class SpeechToText(Resource):
    @api.expect(file_upload)
    @api.response(200, "Success")
    @api.response(400, "Bad Request")
    @api.response(404, "Entry not found")
    def post(self, entry_id):
        """Convert speech from audio file to text and add the summarized speech to notes"""
        args = file_upload.parse_args(strict=True)
        audio_file = args["audio"]

        #transcription = transcribe_audio(audio_file)
        transcription = "Nota de texto que ahora es una cadena"

        entry = client.get_entry(entry_id)
        if entry:
            client.update_entry(entry_id, notes=transcription)
            return {'success': True, 'message': 'Note added successfully'}, 200
        else:
            api.abort(404, "Entry not found")
