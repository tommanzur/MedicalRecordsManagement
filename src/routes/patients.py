from flask import request
from flask_restx import Resource, Namespace, fields
from services.postgres_client import client
from flask_restx import Namespace, Resource
from routes.auth import token_required


api = Namespace('patients', description='Patient related operations')

patient_model = api.model('Patient', {
    'id': fields.Integer(readonly=True),
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
    @api.doc('list_patients', security='Bearer Auth')
    @api.marshal_list_with(patient_model)
    @token_required
    def get(self):
        """List all patients"""
        return client.get_all_patients()

    @api.doc('create_patient', security='Bearer Auth')
    @api.expect(patient_model)
    @api.marshal_with(patient_model, code=201)
    @token_required
    def post(self):
        """Create a new patient"""
        data = request.json
        patient_id = client.add_patient(**data)
        return client.get_patient(patient_id), 201

@api.route('/<int:patient_id>')
@api.param('patient_id', 'The unique identifier of the patient')
@api.response(404, 'Patient not found')
class PatientResource(Resource):
    @api.doc('get_patient', security='Bearer Auth')
    @api.marshal_with(patient_model)
    @token_required
    def get(self, patient_id):
        """Get data of a specific patient"""
        patient = client.get_patient(patient_id)
        if patient is not None:
            return patient
        api.abort(404)

    @api.doc('update_patient', security='Bearer Auth')
    @api.expect(patient_model)
    @token_required
    def put(self, patient_id):
        """Modify patient data"""
        data = request.json
        client.update_patient(patient_id, **data)
        return {'success': True, 'message': 'Patient data updated'}, 200

    @api.doc('delete_patient', security='Bearer Auth')
    @token_required
    def delete(self, patient_id):
        """Delete a patient"""
        client.delete_patient(patient_id)
        return {'success': True, 'message': 'Patient deleted'}, 200
