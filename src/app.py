# app.py
from flask import Flask
from flask_restx import Api
from routes.patients import api as patients_ns
from routes.entries import api as entries_ns
from routes.speech_to_text import api as speech_to_text_ns
from routes.text_suggestions import api as text_suggestions_ns
from routes.conversations import api as conversations_ns
from routes.admin import api as admin_ns
from routes.auth import api as auth_ns

app = Flask(__name__)
api = Api(app, version='1.0', title='Patient Management API',
          description='A simple API for managing patients',
          security='Bearer Auth',
          authorizations={
              'Bearer Auth': {
                  'type': 'apiKey',
                  'in': 'header',
                  'name': 'Authorization',
                  'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
              }
          })

api.add_namespace(patients_ns, path='/patients')
api.add_namespace(entries_ns, path='/entries')
api.add_namespace(speech_to_text_ns, path='/speech_to_text')
api.add_namespace(text_suggestions_ns, path='/text-suggestions')
api.add_namespace(conversations_ns, path='/conversations')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(admin_ns, path='/admin')

if __name__ == '__main__':
    app.run(debug=True)
