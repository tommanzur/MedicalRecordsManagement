from flask import Flask
from flask_restx import Api
from routes.patients import api as patients_ns
from routes.entries import api as entries_ns

app = Flask(__name__)
api = Api(app, version='1.0', title='Patient Management API',
          description='A simple API for managing patients')

api.add_namespace(patients_ns, path='/patients')
api.add_namespace(entries_ns, path='/entries')

if __name__ == '__main__':
    app.run(debug=True)
