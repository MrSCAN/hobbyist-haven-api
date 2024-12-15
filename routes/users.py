from flask import Blueprint, jsonify, request, g, current_app
from middleware.auth import require_auth, require_admin, create_token
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from prisma.models import User
import json

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
async def register():
    """Register a new user
    ---
    responses:
      201:
        description: User created successfully
      400:
        description: Invalid request data
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"message": "No data provided"}), 400

        if not data.get('email') or not data.get('password') or not data.get('name'):
            return jsonify({"message": "Email, password and name are required"}), 400

        existing_user = await User.prisma().find_unique(
            where={"email": data['email']}
        )

        if existing_user:
            return jsonify({"message": "Email already registered"}), 400

        user = await User.prisma().create(
            data={
                "id": str(uuid.uuid4()),
                "email": data['email'],
                "password": generate_password_hash(data['password']),
                "name": data['name'],
                "role": "USER"
            }
        )

        token = create_token(user.id)
        return jsonify({
            "token": token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role
            }
        }), 201

    except Exception as e:
        current_app.logger.error(f"Error in register: {str(e)}")
        return jsonify({"message": "Error creating user", "error": str(e)}), 500

@users_bp.route('/login', methods=['POST'])
async def login():
    """Login user
    ---
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    try:
        data = request.get_json()

        if not data.get('email') or not data.get('password'):
            return jsonify({"message": "Email and password are required"}), 400

        user = await User.prisma().find_unique(
            where={"email": data['email']}
        )

        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({"message": "Invalid credentials"}), 401

        token = create_token(user.id)
        return jsonify({"token": token, "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role
        }})
    except Exception as e:
        return jsonify({"message": "Login failed"}), 500

@users_bp.route('/<user_id>', methods=['GET'])
@require_auth
async def get_user_role(user_id: str):
    """Get user role
    ---
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
    security:
      - BearerAuth: []
    responses:
      200:
        description: User role
      404:
        description: User not found
    """
    user = await User.prisma().find_unique(
        where={"id": user_id},
        select={"role": True}
    )

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(user)

@users_bp.route('/<user_id>/role', methods=['PUT'])
@require_admin
async def update_user_role(user_id: str):
    """Update user role
    ---
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
    security:
      - BearerAuth: []
    responses:
      200:
        description: User role updated
      403:
        description: Forbidden
    """
    data = request.get_json()
    user = await User.prisma().update(
        where={"id": user_id},
        data={"role": data['role']}
    )
    return jsonify(user)

@users_bp.route('/', methods=['GET'])
@require_admin
async def get_users():
    """Get all users
    ---
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of users
      403:
        description: Forbidden
    """
    users = User.prisma().find_many(
        select={
            "id": True,
            "email": True,
            "name": True,
            "role": True
        }
    )
    return jsonify(users)
