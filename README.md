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

4. Generate Prisma client:
```bash
prisma generate
```

5. Initialize the database:
```bash
prisma db push
```

6. Set up environment variables by creating a `.env` file:
```
PORT=3000
CORS_ORIGIN=http://localhost:8080
JWT_SECRET=your_jwt_secret_key_here
```

7. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:3000`

## API Documentation

### Authentication Endpoints

#### Register User
- **POST** `/api/users/register`
- **Body:**
```json
{
  "email": "user@example.com",
  "password": "password",
  "name": "User Name"
}
```

#### Login User
- **POST** `/api/users/login`
- **Body:**
```json
{
  "email": "user@example.com",
  "password": "password"
}
```

### Project Endpoints

#### Get All Projects
- **GET** `/api/projects`
- No authentication required

#### Get Single Project
- **GET** `/api/projects/<project_id>`
- No authentication required

#### Create Project
- **POST** `/api/projects`
- Requires authentication
- **Body:**
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

#### Update Project
- **PUT** `/api/projects/<project_id>`
- Requires authentication
- Body: Same as Create Project

#### Delete Project
- **DELETE** `/api/projects/<project_id>`
- Requires authentication

### User Management Endpoints

#### Get All Users
- **GET** `/api/users`
- Requires admin authentication

#### Get User Role
- **GET** `/api/users/<user_id>`
- Requires authentication

#### Update User Role
- **PUT** `/api/users/<user_id>/role`
- Requires admin authentication
- **Body:**
```json
{
  "role": "ADMIN"
}
```

## Authentication

The API uses JWT tokens for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-token>
```

## Development Notes

- The API uses SQLite as the database
- Arrays (like techStack and repoUrls) are stored as JSON strings in the database
- Prisma is used as the ORM
- JWT is used for authentication
- API documentation is available at `/api-docs` when running the server

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error