import asyncio
from flask import Flask, jsonify, g, request, make_response
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
     resources={
         r"/*": {
             "origins": "*",
             "allow_headers": ["Content-Type", "Authorization"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "expose_headers": ["Content-Range", "X-Content-Range"],
             "supports_credentials": True,
             "max_age": 120  # Cache preflight response for 2 minutes
         }
     })

db = Prisma()
db.connect()
register(db)

swagger = Swagger(app)

# Register blueprints
app.register_blueprint(projects_bp, url_prefix='/api/projects')
app.register_blueprint(users_bp, url_prefix='/api/users')

@app.route('/')
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "OK", "message": "Service is up and running!"})

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
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