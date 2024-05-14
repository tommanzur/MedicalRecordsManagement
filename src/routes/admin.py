# routes/admin.py
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from routes.auth import token_required
from services.postgres_client import client

api = Namespace('admin', description='Admin operations')

user_model = api.model('User', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

password_update_model = api.model('PasswordUpdate', {
    'username': fields.String(required=True, description='Username'),
    'new_password': fields.String(required=True, description='New Password')
})

@api.route('/user')
class UserManagement(Resource):
    @api.expect(user_model, validate=True)
    @api.doc('add_user', security='Bearer Auth')
    @token_required
    def post(self):
        """Add a new user"""
        data = request.json
        user_id = client.add_user(username=data['username'], password=data['password'])
        return jsonify({'message': f'User {data["username"]} added', 'user_id': user_id})

    @api.param('username', 'The username of the user to delete')
    @api.doc('delete_user', security='Bearer Auth')
    @token_required
    def delete(self):
        """Delete a user"""
        username = request.args.get('username')
        user = client.get_user_by_username(username)
        if user:
            client.delete_user(user.id)
            return jsonify({'message': f'User {username} deleted'})
        return jsonify({'message': f'User {username} not found'}), 404

@api.route('/user/password')
class PasswordUpdate(Resource):
    @api.expect(password_update_model, validate=True)
    @api.doc('update_password', security='Bearer Auth')
    @token_required
    def put(self):
        """Update user password"""
        data = request.json
        username = data['username']
        new_password = data['new_password']
        success = client.update_user_password(username, new_password)
        if success:
            return jsonify({'message': f'Password for user {username} updated'})
        return jsonify({'message': f'User {username} not found'}), 404
    