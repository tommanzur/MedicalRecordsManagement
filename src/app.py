from flask import Flask
from flask_restx import Api
from routes.patients import api as patients_ns
from routes.entries import api as entries_ns
from routes.speech_to_text import api as speech_to_text_ns
from routes.text_suggestions import api as text_suggestions_ns

app = Flask(__name__)
api = Api(app, version='1.0', title='Patient Management API',
          description='A simple API for managing patients')

api.add_namespace(patients_ns, path='/patients')
api.add_namespace(entries_ns, path='/entries')
api.add_namespace(speech_to_text_ns, path='/speech_to_text')
api.add_namespace(text_suggestions_ns, path='/text-suggestions')

if __name__ == '__main__':
    app.run(debug=True)
