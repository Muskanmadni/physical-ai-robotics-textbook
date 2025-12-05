# Data Model: Physical AI & Humanoid Robotics Textbook

## Core Entities

### User
**Description**: Represents a registered user of the textbook platform
**Fields**:
- id (string, primary key)
- email (string, unique, required)
- name (string, required)
- preferences (JSON object, optional)
- createdAt (timestamp, required)
- updatedAt (timestamp, required)
- authProvider (string, optional)
- profilePicture (string, optional)

**Validation rules**:
- Email must follow standard email format
- Name must be 1-100 characters
- Preferences must conform to predefined schema

### Chapter
**Description**: Represents a chapter in the textbook
**Fields**:
- id (string, primary key)
- title (string, required)
- content (string, required)
- module (string, required)
- order (integer, required)
- language (string, required, default: "en")
- createdAt (timestamp, required)
- updatedAt (timestamp, required)
- metadata (JSON object, optional)

**Validation rules**:
- Title must be 1-200 characters
- Content length must be greater than 0
- Module must be one of the predefined modules (ROS 2, Gazebo/Unity Simulation, NVIDIA Isaac Robotics, Vision-Language-Action Systems)
- Order must be positive integer
- Language must be one of supported languages ("en", "ur")

### Module
**Description**: Represents a major section of the textbook
**Fields**:
- id (string, primary key)
- title (string, required)
- description (string, required)
- order (integer, required)
- createdAt (timestamp, required)
- updatedAt (timestamp, required)

**Validation rules**:
- Title must be 1-100 characters
- Description must be 1-500 characters
- Order must be positive integer

### UserProgress
**Description**: Tracks user progress through the textbook
**Fields**:
- id (string, primary key)
- userId (string, foreign key to User)
- chapterId (string, foreign key to Chapter)
- completed (boolean, required, default: false)
- progressPercentage (integer, required, default: 0)
- lastAccessed (timestamp, required)
- createdAt (timestamp, required)
- updatedAt (timestamp, required)

**Validation rules**:
- progressPercentage must be between 0-100
- userId must reference existing user
- chapterId must reference existing chapter

### Quiz
**Description**: Represents a quiz associated with a chapter or module
**Fields**:
- id (string, primary key)
- title (string, required)
- chapterId (string, foreign key to Chapter, optional)
- moduleId (string, foreign key to Module, optional)
- questions (JSON array, required)
- createdAt (timestamp, required)
- updatedAt (timestamp, required)

**Validation rules**:
- Title must be 1-200 characters
- Must have either chapterId or moduleId (but not both)
- Questions must be a non-empty array of properly formatted question objects

### QuizSubmission
**Description**: Represents a user's submission of a quiz
**Fields**:
- id (string, primary key)
- quizId (string, foreign key to Quiz)
- userId (string, foreign key to User)
- answers (JSON array, required)
- score (integer, required)
- completedAt (timestamp, required)
- createdAt (timestamp, required)

**Validation rules**:
- Score must be between 0-100
- Answers must match the format of associated quiz questions
- Only one submission per user per quiz

### RAGDocument
**Description**: Represents a document chunk for RAG system
**Fields**:
- id (string, primary key)
- chapterId (string, foreign key to Chapter)
- content (string, required)
- embedding (JSON array, required)
- vectorId (string, required, reference to Qdrant)
- createdAt (timestamp, required)
- updatedAt (timestamp, required)

**Validation rules**:
- Content length must be greater than 0
- Embedding must be a valid vector array
- VectorId must be unique across documents

### PersonalizedContent
**Description**: Stores personalized versions of textbook content
**Fields**:
- id (string, primary key)
- originalChapterId (string, foreign key to Chapter)
- userId (string, foreign key to User)
- personalizedContent (string, required)
- personalizationType (string, required)
- createdAt (timestamp, required)
- updatedAt (timestamp, required)

**Validation rules**:
- Content length must be greater than 0
- PersonalizationType must be one of predefined types (simplified, detailed, example-focused, etc.)

### Translation
**Description**: Contains translated versions of content
**Fields**:
- id (string, primary key)
- originalContentId (string, required) - can reference Chapter, Quiz, etc.
- originalContentType (string, required) - "Chapter", "Quiz", etc.
- language (string, required)
- translatedContent (JSON object, required)
- createdAt (timestamp, required)
- updatedAt (timestamp, required)

**Validation rules**:
- Language must be one of supported languages
- OriginalContentId and originalContentType must form a valid reference
- TranslatedContent must have matching structure to original content