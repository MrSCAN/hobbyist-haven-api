from flask import Blueprint, jsonify, request
from middleware.auth import require_auth, require_admin
from prisma import Prisma
from clerk import Clerk
import os

users_bp = Blueprint('users', __name__)
prisma = Prisma()
clerk = Clerk(secret_key=os.getenv('CLERK_SECRET_KEY'))

@users_bp.route('/webhook', methods=['POST'])
async def clerk_webhook():
    """Handle Clerk webhooks
    ---
    responses:
      200:
        description: Webhook processed successfully
      400:
        description: Webhook processing error
    """
    try:
        event = request.get_json()
        
        if event['type'] == 'user.created':
            data = event['data']
            await prisma.user.create(
                data={
                    "id": data['id'],
                    "email": data['email_addresses'][0]['email_address'],
                    "name": f"{data['first_name']} {data['last_name']}".strip(),
                    "role": "USER"
                }
            )
            
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": "Webhook error"}), 400

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
    user = await prisma.user.find_unique(
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
    user = await prisma.user.update(
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
    users = await prisma.user.find_many(
        select={
            "id": True,
            "email": True,
            "name": True,
            "role": True
        }
    )
    return jsonify(users)