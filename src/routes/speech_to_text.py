from flask import request
from flask_restx import Resource, Namespace, fields

api = Namespace('speech_to_text', description='Speech to text operations')

# Model definition for Swagger
speech_to_text_model = api.model('SpeechToText', {
    'audio': fields.String(required=True, description='Base64 encoded audio file')
})

@api.route('/')
class SpeechToText(Resource):
    @api.doc('convert_speech_to_text')
    @api.expect(speech_to_text_model)
    @api.response(200, 'Success')
    @api.response(400, 'Bad Request')
    def post(self):
        """Convert speech from audio file to text"""
        data = request.json
        audio_base64 = data.get('audio')
        # Here we gonna implement the logic to decode the base64 audio, process it, 
        # and convert it to text using your chosen library or API
