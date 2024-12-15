from functools import wraps
from flask import request, jsonify, g
from prisma.models import User
import jwt
import os
from datetime import datetime, timedelta


JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-here')

def create_token(user_id: str) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not token:
                return jsonify({"message": "No token provided"}), 401

            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            user = User.prisma().find_unique(
                where={"id": payload['user_id']}
            )

            if not user:
                return jsonify({"message": "User not found"}), 401

            g.user = user
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"message": "Unauthorized"}), 401
    return decorated_function

def require_admin(f):
    @wraps(f)
    @require_auth
    def decorated_function(*args, **kwargs):
        try:
            if g.user.role != 'ADMIN':
                return jsonify({"message": "Forbidden: Admin access required"}), 403
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"message": "Error checking admin status"}), 500
    return decorated_function