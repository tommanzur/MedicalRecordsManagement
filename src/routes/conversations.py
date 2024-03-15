from flask import request
from flask_restx import Resource, Namespace, fields

api = Namespace('conversations', description='Conversations related operations')

# Model definitions for Swagger
conversation_model = api.model('Conversation', {
    'title': fields.String(required=True, description='Conversation title'),
    'description': fields.String(description='Conversation description'),
})

message_model = api.model('Message', {
    'conversation_id': fields.Integer(required=True, description='The ID of the conversation'),
    'content': fields.String(required=True, description='Message content'),
})

@api.route('/')
class ConversationList(Resource):
    @api.doc('list_conversations')
    def get(self):
        """List all conversations"""
        # Implementar lógica para retornar la lista de conversaciones
        return {'message': 'List of conversations'}

    @api.doc('create_conversation')
    @api.expect(conversation_model)
    def post(self):
        """Create a new conversation"""
        # Implementar lógica para crear una nueva conversación
        return {'message': 'Conversation created'}, 201

@api.route('/<int:conv_id>')
@api.param('conv_id', 'The unique identifier of the conversation')
@api.response(404, 'Conversation not found')
class Conversation(Resource):
    @api.doc('get_conversation')
    def get(self, conv_id):
        """Get a specific conversation"""
        # Implementar lógica para retornar una conversación específica
        return {'message': f'Conversation {conv_id}'}

    @api.doc('post_message')
    @api.expect(message_model)
    def post(self, conv_id):
        """Post a message to a conversation"""
        # Implementar lógica para postear un mensaje a una conversación específica
        return {'message': f'Message to conversation {conv_id} posted'}, 201
