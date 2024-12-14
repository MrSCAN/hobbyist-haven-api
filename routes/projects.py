from flask import Blueprint, jsonify, request, g
from middleware.auth import require_auth
from prisma import Prisma
from typing import Dict, Any

projects_bp = Blueprint('projects', __name__)
prisma = Prisma()

@projects_bp.route('/', methods=['GET'])
async def get_projects():
    """Get all projects
    ---
    responses:
      200:
        description: List of all projects
    """
    projects = await prisma.project.find_many(
        include={
            "author": True,
            "stages": True
        }
    )
    return jsonify(projects)

@projects_bp.route('/<project_id>', methods=['GET'])
async def get_project(project_id: str):
    """Get a single project
    ---
    parameters:
      - name: project_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Project details
      404:
        description: Project not found
    """
    project = await prisma.project.find_unique(
        where={"id": project_id},
        include={
            "author": True,
            "stages": True
        }
    )
    
    if not project:
        return jsonify({"message": "Project not found"}), 404
        
    return jsonify(project)

@projects_bp.route('/', methods=['POST'])
@require_auth
async def create_project():
    """Create a new project
    ---
    security:
      - BearerAuth: []
    responses:
      201:
        description: Project created successfully
      400:
        description: Invalid request data
    """
    data: Dict[str, Any] = request.get_json()
    
    if not data.get('title') or not data.get('description'):
        return jsonify({"message": "Title and description are required"}), 400
        
    project = await prisma.project.create(
        data={
            "title": data['title'],
            "description": data['description'],
            "techStack": data.get('techStack', []),
            "repoUrls": data.get('repoUrls', []),
            "imageUrl": data.get('imageUrl', ''),
            "documentation": data.get('documentation', ''),
            "youtubeUrl": data.get('youtubeUrl'),
            "stages": {
                "create": data.get('stages', [])
            },
            "authorId": g.user.id
        },
        include={
            "author": True,
            "stages": True
        }
    )
    
    return jsonify(project), 201

@projects_bp.route('/<project_id>', methods=['PUT'])
@require_auth
async def update_project(project_id: str):
    """Update a project
    ---
    parameters:
      - name: project_id
        in: path
        type: string
        required: true
    security:
      - BearerAuth: []
    responses:
      200:
        description: Project updated successfully
      404:
        description: Project not found
    """
    data: Dict[str, Any] = request.get_json()
    
    project = await prisma.project.update(
        where={"id": project_id},
        data={
            "title": data.get('title'),
            "description": data.get('description'),
            "techStack": data.get('techStack'),
            "repoUrls": data.get('repoUrls'),
            "imageUrl": data.get('imageUrl'),
            "documentation": data.get('documentation'),
            "youtubeUrl": data.get('youtubeUrl'),
            "stages": {
                "deleteMany": {},
                "create": data.get('stages', [])
            }
        },
        include={
            "author": True,
            "stages": True
        }
    )
    
    return jsonify(project)

@projects_bp.route('/<project_id>', methods=['DELETE'])
@require_auth
async def delete_project(project_id: str):
    """Delete a project
    ---
    parameters:
      - name: project_id
        in: path
        type: string
        required: true
    security:
      - BearerAuth: []
    responses:
      204:
        description: Project deleted successfully
    """
    await prisma.project.delete(
        where={"id": project_id}
    )
    
    return '', 204