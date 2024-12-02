# Simple REST API

A simple RESTful API project built with Node.js and Express.

## Project Structure

```
project/
├── src/
│   ├── controllers/    # Request handlers
│   │   └── user.controller.js
│   ├── services/      # Business logic
│   │   └── user.service.js
│   ├── routes/        # Route definitions
│   │   ├── index.js
│   │   └── user.routes.js
│   └── index.js       # App entry point
├── .env              # Environment variables
└── package.json
```

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

## API Endpoints

### Users
- GET `/api/users` - Get all users
- POST `/api/users` - Create a new user
- GET `/api/users/:id` - Get user by ID
- PUT `/api/users/:id` - Update user
- DELETE `/api/users/:id` - Delete user

## Example Request

Create a new user:
```bash
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```
