# routes/auth.py
import bcrypt
from flask import request, jsonify, make_response
from flask_restx import Namespace, Resource, fields
import jwt
from functools import wraps
from datetime import datetime, timedelta
from services.postgres_client import client
from config import SECRET_KEY

api = Namespace('auth', description='Authentication related operations')

# Modelo de credenciales para Swagger
login_model = api.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.doc('login')
    def post(self):
        auth = request.json
        if not auth or not auth.get('username') or not auth.get('password'):
            return make_response('Could not verify!', 401)
        
        user = client.get_user_by_username(auth['username'])
        
        if user and bcrypt.checkpw(auth['password'].encode('utf-8'), user.password.encode('utf-8')):
            token = jwt.encode({
                'user': user.username,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, SECRET_KEY, algorithm="HS256")
            return jsonify({'token': token})
        
        return make_response('Could not verify!', 401)