from flask import Flask, jsonify, request
from flask_cors import CORS
from routes.projects import projects_bp
from routes.users import users_bp
from flasgger import Swagger
from dotenv import load_dotenv
from prisma import Prisma
import os

load_dotenv()

app = Flask(__name__)
CORS(app, origins=os.getenv('CORS_ORIGIN', 'http://localhost:8080'), supports_credentials=True)

# Initialize Prisma
prisma = Prisma()

@app.before_first_request
def init_prisma():
    prisma.connect()

@app.teardown_appcontext
def shutdown_prisma(exception=None):
    prisma.disconnect()

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api-docs"
}

swagger = Swagger(app, config=swagger_config)

# Register blueprints
app.register_blueprint(projects_bp, url_prefix='/api/projects')
app.register_blueprint(users_bp, url_prefix='/api/users')

@app.route('/')
def health_check():
    """Health check endpoint
    ---
    responses:
      200:
        description: Service status
    """
    return jsonify({"status": "OK", "message": "Service is up and running!"})

@app.errorhandler(500)
def handle_error(error):
    return jsonify({"message": "Something went wrong!"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)