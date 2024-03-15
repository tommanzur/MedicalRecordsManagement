from flask import request
from flask_restx import Resource, Namespace, fields
from models.entry import Entry
from services.postgres_client import client

api = Namespace('entries', description='Entry related operations')

# Model definition for Swagger
entry_model = api.model('Entry', {
    'patient_id': fields.Integer(required=True, description='The patient ID associated with this entry'),
    'record': fields.String(required=True, description='Details of the medical record'),
    'date_of_visit': fields.Date(required=True, description='Date of the visit'),
    'time_of_visit': fields.String(description='Time of the visit'),
    'visit_type': fields.String(required=True, description='Type of visit'),
    'symptoms': fields.String(description='Symptoms presented by the patient'),
    'diagnosis': fields.String(description='Diagnosis'),
    'treatment': fields.String(description='Treatment prescribed'),
    'prescribed_medications': fields.String(description='Medications prescribed'),
    'follow_up_needed': fields.Boolean(description='Is follow-up needed?'),
    'follow_up_date': fields.Date(description='Date for the follow-up'),
    'notes': fields.String(description='Any additional notes'),
})

@api.route('/')
class EntryList(Resource):
    @api.doc('list_entries')
    @api.marshal_list_with(entry_model)
    def get(self):
        """List all entries"""
        return client.session.query(Entry).all()

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
class Entry(Resource):
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
