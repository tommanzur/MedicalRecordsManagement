import json
from flask import request
from flask_restx import Resource, Namespace, fields
from models.entry import Entry
from services.postgres_client import client

api = Namespace('entries', description='Entry related operations')

entry_model = api.model('Entry', {
    'id': fields.Integer(required=True, description='The entry ID'),
    'patient_id': fields.Integer(required=True, description='The patient ID associated with this entry'),
    'record': fields.String(required=False, description='Details of the medical record'),
    'date_of_visit': fields.Date(required=False, description='Date of the visit'),
    'time_of_visit': fields.String(required=False, description='Time of the visit', example="14:30"),
    'visit_type': fields.String(required=True, description='Type of visit', example="Routine Check-up"),
    'symptoms': fields.String(required=False, description='Symptoms presented by the patient', example="Headache, fever"),
    'diagnosis': fields.String(required=False, description='Diagnosis', example="Common cold"),
    'treatment': fields.String(required=False, description='Treatment prescribed', example="Rest and hydration"),
    'prescribed_medications': fields.String(required=False, description='Medications prescribed', example="Paracetamol"),
    'follow_up_needed': fields.Boolean(required=False, description='Is follow-up needed?', example=False),
    'follow_up_date': fields.Date(required=False, description='Date for the follow-up', example="2024-06-15"),
    'notes': fields.String (required=False, description='Any additional notes', example=["summary", "Visit summary", "detail", "More detailed note"]),
    'attached': fields.List(fields.String, required=False, description='Attached files metadata', example={"filename": "report.pdf", "url": "http://example.com/report.pdf"})
})

@api.route('/')
class EntryList(Resource):
    @api.doc('list_entries')
    @api.marshal_list_with(entry_model)
    def get(self):
        """List all entries"""
        entries = client.get_all_entries()
        return entries

    @api.doc('create_entry')
    @api.expect(entry_model)
    @api.marshal_with(entry_model, code=201)
    def post(self):
        """Create a new entry"""
        data = request.json
        entry_id = client.add_entry(**data)
        return client.get_entry(entry_id), 201

@api.route('/<int:entry_id>')
@api.param('entry_id', 'The unique identifier of the entry')
@api.response(404, 'Entry not found')
class EntryResource(Resource):
    @api.doc('get_entry')
    @api.marshal_with(entry_model)
    def get(self, entry_id):
        """Get data of a specific entry"""
        entry = client.get_entry(entry_id)
        if entry is not None:
            return entry
        api.abort(404)

    @api.doc('update_entry')
    @api.expect(entry_model)
    def put(self, entry_id):
        """Modify entry data"""
        data = request.json
        client.update_entry(entry_id, **data)
        return {'success': True, 'message': 'Entry data updated'}, 200

    @api.doc('delete_entry')
    def delete(self, entry_id):
        """Delete an entry"""
        client.delete_entry(entry_id)
        return {'success': True, 'message': 'Entry deleted'}, 200
