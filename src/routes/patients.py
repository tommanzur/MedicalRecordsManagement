from flask import request
from flask_restx import Resource, Namespace, fields
from models.patient import Patient
from services.postgres_client import client

api = Namespace('patients', description='Patient related operations')

# Model definition for Swagger
patient_model = api.model('Patient', {
    'name': fields.String(required=True, description='Patient name'),
    'date_of_birth': fields.Date(required=True, description='Patient birth date'),
    'gender': fields.String(required=True, description='Patient gender'),
    'address': fields.String(description='Patient address'),
    'phone_number': fields.String(description='Patient phone number'),
    'email': fields.String(description='Patient email'),
    'emergency_contact_name': fields.String(description='Emergency contact name'),
    'emergency_contact_phone': fields.String(description='Emergency contact phone'),
    'medical_record_number': fields.String(description='Medical record number'),
    'insurance_provider': fields.String(description='Insurance provider'),
    'insurance_policy_number': fields.String(description='Insurance policy number'),
})

@api.route('/')
class PatientList(Resource):
    @api.doc('list_patients')
    @api.marshal_list_with(patient_model)
    def get(self):
        """List all patients"""
        # Here you would implement the logic to retrieve all patients from the database
        return client.session.query(Patient).all()

    @api.doc('create_patient')
    @api.expect(patient_model)
    @api.marshal_with(patient_model, code=201)
    def post(self):
        """Create a new patient"""
        data = request.json
        patient_id = client.add_patient(**data)
        return client.get_patient(patient_id), 201

@api.route('/<int:patient_id>')
@api.param('patient_id', 'The unique identifier of the patient')
@api.response(404, 'Patient not found')
class Patient(Resource):
    @api.doc('get_patient')
    @api.marshal_with(patient_model)
    def get(self, patient_id):
        """Get data of a specific patient"""
        patient = client.get_patient(patient_id)
        if patient is not None:
            return patient
        api.abort(404)

    @api.doc('update_patient')
    @api.expect(patient_model)
    def put(self, patient_id):
        """Modify patient data"""
        data = request.json
        client.update_patient(patient_id, **data)
        return {'success': True, 'message': 'Patient data updated'}, 200

    @api.doc('delete_patient')
    def delete(self, patient_id):
        """Delete a patient"""
        client.delete_patient(patient_id)
        return {'success': True, 'message': 'Patient deleted'}, 200
