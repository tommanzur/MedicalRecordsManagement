from flask_restx import Namespace, Resource, reqparse
from werkzeug.datastructures import FileStorage
from services.postgres_client import client
from services.audio_transcription import transcribe_audio
from flask_restx import reqparse
from werkzeug.datastructures import FileStorage
from routes.auth import token_required

api = Namespace("speech_to_text", description="Speech to text operations")

def audio_file_type(value):
    if not isinstance(value, FileStorage):
        raise ValueError("The file must be a FileStorage type")
    
    allowed_extensions = (
        ".flac", ".m4a", ".mp3", ".mp4", ".mpeg",
        ".mpga", ".oga", ".ogg", ".wav", ".webm"
    )
    if not any(value.filename.endswith(ext) for ext in allowed_extensions):
        raise ValueError(
            f"Invalid file format. Allowed formats are: {', '.join(allowed_extensions)}"
        )

    return value

file_upload = reqparse.RequestParser()
file_upload.add_argument(
    "audio",
    type=audio_file_type,
    location="files",
    required=True,
    help="Audio file must be in one of the permitted formats: FLAC, M4A, MP3, MP4, MPEG, MPGA, OGA, OGG, WAV, WEBM"
)

@api.route("/<int:entry_id>")
class SpeechToText(Resource):
    @api.doc("speech_to_text", security="Bearer Auth")
    @api.expect(file_upload)
    @api.response(200, "Success")
    @api.response(400, "Bad Request")
    @api.response(404, "Entry not found")
    @token_required
    def post(self, entry_id):
        """Convert speech from audio file to text and add the summarized speech to notes"""
        args = file_upload.parse_args(strict=True)
        audio_file = args["audio"]
        audio_bytes = audio_file.read()

        transcription = transcribe_audio(audio_bytes, audio_file.filename)

        entry = client.get_entry(entry_id)
        if entry:
            success = client.add_note_to_entry(entry_id, transcription)
            if success:
                return {"success": True, "message": "Note added successfully"}, 200
            else:
                return {"success": False, "message": "Failed to add note"}, 400
        else:
            api.abort(404, "Entry not found")
