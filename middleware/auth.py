from functools import wraps
from flask import request, jsonify, g
from clerk import Clerk
from prisma import Prisma
import os

clerk = Clerk(secret_key=os.getenv('CLERK_SECRET_KEY'))
prisma = Prisma()

def require_auth(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not token:
                return jsonify({"message": "No token provided"}), 401
            
            session = clerk.sessions.verify_token(token)
            g.user = session
            return await f(*args, **kwargs)
        except Exception as e:
            return jsonify({"message": "Unauthorized"}), 401
    return decorated_function

def require_admin(f):
    @wraps(f)
    @require_auth
    async def decorated_function(*args, **kwargs):
        try:
            user = await prisma.user.find_unique(
                where={"id": g.user.id},
            )
            
            if user.role != 'ADMIN':
                return jsonify({"message": "Forbidden: Admin access required"}), 403
                
            return await f(*args, **kwargs)
        except Exception as e:
            return jsonify({"message": "Error checking admin status"}), 500
    return decorated_function