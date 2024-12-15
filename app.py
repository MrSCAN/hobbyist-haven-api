import asyncio
from flask import Flask, jsonify, g
from flask_cors import CORS
from routes.projects import projects_bp
from routes.users import users_bp
from flasgger import Swagger
from dotenv import load_dotenv
from prisma import Prisma, register
import os

load_dotenv()

app = Flask(__name__)
CORS(app, 
     origins=["http://localhost:8080"],
     allow_credentials=True,
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     expose_headers=["Content-Range", "X-Content-Range"])

db = Prisma()
db.connect()
register(db)

# ... keep existing code (Swagger configuration)

# Register blueprints
app.register_blueprint(projects_bp, url_prefix='/api/projects')
app.register_blueprint(users_bp, url_prefix='/api/users')

@app.route('/')
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "OK", "message": "Service is up and running!"})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.errorhandler(500)
def handle_error(error):
    app.logger.error(f"Internal Server Error: {str(error)}")
    return jsonify({"message": "Internal Server Error", "error": str(error)}), 500

@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.error(f"Unhandled Exception: {str(error)}")
    return jsonify({"message": "Internal Server Error", "error": str(error)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)