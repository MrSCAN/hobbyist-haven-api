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
     resources={r"/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

db = Prisma()
db.connect()
register(db)

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
    """Health check endpoint."""
    return jsonify({"status": "OK", "message": "Service is up and running!"})

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