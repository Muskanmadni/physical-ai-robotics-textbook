# API Contracts: Physical AI & Humanoid Robotics Textbook

## Authentication Endpoints

### POST /api/auth/login
**Description**: Authenticate a user and return a session token
**Request**:
- Headers: Content-Type: application/json
- Body:
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```

**Response**:
- Status: 200 OK
- Body:
```json
{
  "token": "string",
  "user": {
    "id": "string",
    "email": "string",
    "name": "string"
  }
}
```

**Errors**:
- 400: Invalid credentials format
- 401: Invalid credentials
- 500: Server error

### POST /api/auth/register
**Description**: Register a new user
**Request**:
- Headers: Content-Type: application/json
- Body:
```json
{
  "email": "string (required)",
  "password": "string (required, min 8 chars)",
  "name": "string (required)"
}
```

**Response**:
- Status: 201 Created
- Body:
```json
{
  "message": "User created successfully"
}
```

**Errors**:
- 400: Invalid input format
- 409: User already exists
- 500: Server error

## User Management Endpoints

### GET /api/users/profile
**Description**: Get current user's profile information
**Headers**: Authorization: Bearer {token}
**Response**:
- Status: 200 OK
- Body:
```json
{
  "id": "string",
  "email": "string",
  "name": "string",
  "preferences": "JSON object"
}
```

### PUT /api/users/preferences
**Description**: Update user preferences
**Headers**: Authorization: Bearer {token}
**Request Body**:
```json
{
  "preferences": "JSON object"
}
```

**Response**:
- Status: 200 OK
- Body:
```json
{
  "message": "Preferences updated successfully"
}
```

## Textbook Content Endpoints

### GET /api/modules
**Description**: Get all textbook modules
**Response**:
- Status: 200 OK
- Body:
```json
[
  {
    "id": "string",
    "title": "string",
    "description": "string",
    "order": "integer"
  }
]
```

### GET /api/modules/{moduleId}/chapters
**Description**: Get chapters for a specific module
**Path Parameters**:
- moduleId: string (required)

**Response**:
- Status: 200 OK
- Body:
```json
[
  {
    "id": "string",
    "title": "string",
    "module": "string",
    "order": "integer",
    "language": "string"
  }
]
```

### GET /api/chapters/{chapterId}
**Description**: Get a specific chapter by ID
**Path Parameters**:
- chapterId: string (required)

**Query Parameters**:
- language: string (optional, default: "en")
- userId: string (optional, for personalization)

**Response**:
- Status: 200 OK
- Body:
```json
{
  "id": "string",
  "title": "string",
  "content": "string",
  "module": "string",
  "order": "integer",
  "language": "string",
  "metadata": "JSON object"
}
```

### GET /api/search
**Description**: Search textbook content
**Query Parameters**:
- q: string (required, search query)
- limit: integer (optional, default: 10)
- userId: string (optional, for personalized results)

**Response**:
- Status: 200 OK
- Body:
```json
{
  "results": [
    {
      "id": "string",
      "title": "string",
      "content": "string",
      "module": "string",
      "chapter": "string",
      "score": "number"
    }
  ]
}
```

## Quiz Endpoints

### GET /api/quizzes/{quizId}
**Description**: Get a specific quiz by ID
**Path Parameters**:
- quizId: string (required)

**Response**:
- Status: 200 OK
- Body:
```json
{
  "id": "string",
  "title": "string",
  "questions": [
    {
      "id": "string",
      "question": "string",
      "options": ["string"],
      "type": "string"  // "multiple-choice", "true-false", "short-answer"
    }
  ]
}
```

### POST /api/quizzes/{quizId}/submit
**Description**: Submit a quiz attempt
**Headers**: Authorization: Bearer {token}
**Path Parameters**:
- quizId: string (required)

**Request Body**:
```json
{
  "answers": [
    {
      "questionId": "string",
      "answer": "string"
    }
  ]
}
```

**Response**:
- Status: 201 Created
- Body:
```json
{
  "id": "string",
  "quizId": "string",
  "userId": "string",
  "score": "integer",
  "completedAt": "timestamp"
}
```

## Progress Tracking Endpoints

### GET /api/users/progress
**Description**: Get user's progress through the textbook
**Headers**: Authorization: Bearer {token}

**Response**:
- Status: 200 OK
- Body:
```json
{
  "progress": [
    {
      "chapterId": "string",
      "completed": "boolean",
      "progressPercentage": "integer"
    }
  ]
}
```

### PUT /api/users/progress/{chapterId}
**Description**: Update progress for a chapter
**Headers**: Authorization: Bearer {token}
**Path Parameters**:
- chapterId: string (required)

**Request Body**:
```json
{
  "completed": "boolean",
  "progressPercentage": "integer"
}
```

**Response**:
- Status: 200 OK
- Body:
```json
{
  "message": "Progress updated successfully"
}
```

## RAG (Retrieval-Augmented Generation) Endpoints

### POST /api/rag/query
**Description**: Query the RAG system for textbook-related information
**Request Body**:
```json
{
  "query": "string (required)",
  "userId": "string (optional)"
}
```

**Response**:
- Status: 200 OK
- Body:
```json
{
  "response": "string",
  "sources": [
    {
      "chapterId": "string",
      "title": "string",
      "relevance": "number"
    }
  ]
}
```

## Personalization Endpoints

### POST /api/personalization/generate
**Description**: Generate personalized content for a chapter
**Headers**: Authorization: Bearer {token}
**Request Body**:
```json
{
  "chapterId": "string (required)",
  "personalizationType": "string (required)",
  "userQuizScores": "array of objects (optional)"
}
```

**Response**:
- Status: 200 OK
- Body:
```json
{
  "id": "string",
  "originalChapterId": "string",
  "personalizedContent": "string",
  "personalizationType": "string"
}
```

## Translation Endpoints

### GET /api/translate/{contentId}
**Description**: Get translated content
**Path Parameters**:
- contentId: string (required)

**Query Parameters**:
- sourceType: string (required, e.g., "Chapter", "Quiz")
- targetLanguage: string (required, e.g., "ur", "en")

**Response**:
- Status: 200 OK
- Body:
```json
{
  "originalContentId": "string",
  "originalContentType": "string",
  "language": "string",
  "translatedContent": "JSON object"
}
```