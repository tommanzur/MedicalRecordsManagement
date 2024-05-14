from flask import request
from flask_restx import Resource, Namespace, fields
from services.postgres_client import client as postgres_client
from routes.auth import token_required

api = Namespace('conversations', description='Conversations related operations')

# Model definitions for Swagger
conversation_model = api.model('Conversation', {
    'id': fields.Integer(readOnly=True, description='Unique identifier of the conversation'),
    'patient_id': fields.Integer(required=True, description='Patient ID'),
    'start_time': fields.DateTime(required=True, description='Start time of the conversation', example='2024-05-11T12:00:00Z'),
    'end_time': fields.DateTime(required=False, description='End time of the conversation', example='2024-05-11T13:00:00Z'),
    'session_id': fields.String(required=True, description='Session UUID', example='123e4567-e89b-12d3-a456-426614174000'),
    'messages': fields.Raw(required=False, description='JSONB field storing messages in JSON format')
})

message_model = api.model('Message', {
    'role': fields.String(required=True, description='Sender of the message', example='doctor'),
    'content': fields.String(required=True, description='Content of the message', example='How are you feeling today?')
})


@api.route('/')
class ConversationList(Resource):
    @api.doc('list_conversations')
    @api.marshal_list_with(conversation_model)
    @token_required
    def get(self):
        """List all conversations"""
        conversations = postgres_client.get_all_conversations()
        return conversations

    @api.doc('create_conversation')
    @api.expect(conversation_model)
    @api.marshal_with(conversation_model, code=201)
    @token_required
    def post(self):
        """Create a new conversation"""
        data = request.json
        new_conversation = postgres_client.add_conversation(patient_id=data['patient_id'], session_id=data['session_id'])
        return new_conversation, 201

@api.route('/<int:conv_id>')
@api.param('conv_id', 'The unique identifier of the conversation')
@api.response(404, 'Conversation not found')
class ConversationResource(Resource):
    @api.doc('get_conversation')
    @api.marshal_with(conversation_model)
    @token_required
    def get(self, conv_id):
        """Get a specific conversation"""
        conversation = postgres_client.get_conversation_by_id(conv_id)
        if conversation is None:
            api.abort(404, 'Conversation not found')
        return conversation, 200

    @api.doc('post_message')
    @api.expect(message_model)
    @token_required
    def post(self, conv_id):
        """Post a message to a conversation"""
        content = request.json['content']
        try:
            response = postgres_client.add_message_to_conversation(conv_id, content)
            return {'message': 'Message and response added to conversation', 'response': response}, 201
        except Exception as e:
            api.abort(404, 'Conversation not found or error in processing: ' + str(e))
