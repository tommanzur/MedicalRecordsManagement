# Patient Management API Documentation

## Overview

This API provides services for a medical records application where doctors can register medical histories as text or voice notes, which are stored as text using Whisper. Doctors can navigate through different patients, add, modify, and delete records. The API also supports managing clinical entries for each patient and offers a RAG chatbot service. Doctors can chat with a language model contextualized with the patient's clinical history and conversation history using LangChain, pgvector, and SQLAlchemy. The API includes Swagger documentation and an admin section for user management, including login functionality with JWT authentication for secure access.

## Features

- **Patient Management**: Add, modify, delete, and list patients.
- **Clinical Entries Management**: Add, modify, delete, and list clinical entries for patients.
- **Speech to Text Conversion**: Convert audio files to text and summarize speech into notes.
- **Text Suggestions**: Process input text to provide suggestions.
- **Conversational AI**: Chat with a model contextualized with the patient's clinical history.
- **Authentication**: User login with JWT token generation.
- **Admin Panel**: Manage users and update passwords.

## API Endpoints

### Patient Related Operations

**Create a New Patient**

- **Endpoint**: POST `/patients/`
- **Description**: Creates a new patient.

**List All Patients**

- **Endpoint**: GET `/patients/`
- **Description**: Retrieves a list of all patients.

**Delete a Patient**

- **Endpoint**: DELETE `/patients/{patient_id}`
- **Description**: Deletes a specific patient.

**Modify Patient Data**

- **Endpoint**: PUT `/patients/{patient_id}`
- **Description**: Updates data of a specific patient.

**Get Patient Data**

- **Endpoint**: GET `/patients/{patient_id}`
- **Description**: Retrieves data of a specific patient.

### Entries Related Operations

**Create a New Clinical Entry**

- **Endpoint**: POST `/entries/`
- **Description**: Creates a new clinical entry.

**List All Entries**

- **Endpoint**: GET `/entries/`
- **Description**: Retrieves a list of all entries.

**List Entries by Patient**

- **Endpoint**: GET `/entries/patient/{patient_id}`
- **Description**: Retrieves all entries for a specific patient.

**Delete an Entry**

- **Endpoint**: DELETE `/entries/{entry_id}`
- **Description**: Deletes a specific entry.

**Modify Entry Data**

- **Endpoint**: PUT `/entries/{entry_id}`
- **Description**: Updates data of a specific entry.

**Get Entry Data**

- **Endpoint**: GET `/entries/{entry_id}`
- **Description**: Retrieves data of a specific entry.

### Speech to Text Operations

**Convert Speech to Text**

- **Endpoint**: POST `/speech_to_text/{entry_id}`
- **Description**: Converts speech from an audio file to text and adds the summarized speech to notes.

### Text Suggestions Operations

**Process Text for Suggestions**

- **Endpoint**: POST `/text-suggestions/`
- **Description**: Processes input text and provides suggestions.

### Conversations Operations

**Chatbot RAG Service**

**Create a New Conversation**

- **Endpoint**: POST `/conversations/`
- **Description**: Creates a new conversation.

**List All Conversations**

- **Endpoint**: GET `/conversations/`
- **Description**: Retrieves a list of all conversations.

**Post a Message to a Conversation**

- **Endpoint**: POST `/conversations/{conv_id}`
- **Description**: Posts a message to a specific conversation.

**Get a Specific Conversation**

- **Endpoint**: GET `/conversations/{conv_id}`
- **Description**: Retrieves a specific conversation.

### Authentication Operations

**User Login**

- **Endpoint**: POST `/auth/login`
- **Description**: Authenticates a user and returns a JWT token.

### Admin Operations

**Add a New User**

- **Endpoint**: POST `/admin/user`
- **Description**: Adds a new user.

**Delete a User**

- **Endpoint**: DELETE `/admin/user`
- **Description**: Deletes a specific user.

**Update User Password**

- **Endpoint**: PUT `/admin/user/password`
- **Description**: Updates the password of a specific user.

## Usage

### Local Setup

**Build and Start Docker Containers:**

```bash
docker compose up --build flask_db
```

```bash
python src/app.py runserver ai
```
**Configure Credentials:**
Set the database credentials and OpenAI key in the config.py file before running the application.

## Swagger Documentation
Access detailed API documentation at /swagger.json.

- Admin Panel
Manage users and access admin functionalities through the admin panel.

- Authentication
Secure access with JWT tokens for API requests.