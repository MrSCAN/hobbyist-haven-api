# Hobbyist Haven API

A Flask-based REST API for managing hobby projects and user accounts.

## Prerequisites

- Python 3.8+
- pip
- SQLite

## Setup & Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hobbyist-haven-api
```

2. Create and activate a virtual environment:
```bash
python -m venv .ev
source .ev/bin/activate  # On Windows use: .ev\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
prisma db push
```

5. Set up environment variables by creating a `.env` file:
```
PORT=3000
CORS_ORIGIN=http://localhost:8080
JWT_SECRET=your_jwt_secret_key_here
```

6. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:3000`

## API Endpoints

### Authentication

- **POST /api/users/register**
  - Register a new user
  - Body: `{ "email": "user@example.com", "password": "password", "name": "User Name" }`

- **POST /api/users/login**
  - Login user
  - Body: `{ "email": "user@example.com", "password": "password" }`

### Projects

- **GET /api/projects**
  - Get all projects
  - No authentication required

- **GET /api/projects/<project_id>**
  - Get a specific project
  - No authentication required

- **POST /api/projects**
  - Create a new project
  - Requires authentication
  - Body: 
    ```json
    {
      "title": "Project Title",
      "description": "Project Description",
      "techStack": ["Tech1", "Tech2"],
      "repoUrls": ["url1", "url2"],
      "imageUrl": "optional-image-url",
      "documentation": "optional-documentation",
      "youtubeUrl": "optional-youtube-url",
      "stages": [
        {
          "title": "Stage 1",
          "description": "Stage Description"
        }
      ]
    }
    ```

- **PUT /api/projects/<project_id>**
  - Update a project
  - Requires authentication
  - Body: Same as POST

- **DELETE /api/projects/<project_id>**
  - Delete a project
  - Requires authentication

### Users

- **GET /api/users**
  - Get all users
  - Requires admin authentication

- **GET /api/users/<user_id>**
  - Get user role
  - Requires authentication

- **PUT /api/users/<user_id>/role**
  - Update user role
  - Requires admin authentication
  - Body: `{ "role": "ADMIN" }`

## Authentication

The API uses JWT tokens for authentication. After logging in or registering, you'll receive a token that should be included in the Authorization header of subsequent requests:

```
Authorization: Bearer <your-token>
```

## Development

The API uses:
- Flask for the web framework
- Prisma for database ORM
- JWT for authentication
- SQLite for database

## API Documentation

API documentation is available at `/api-docs` when running the server.