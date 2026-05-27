@'

# Travel Planner API

A management application that helps travellers plan trips and collect desired places to visit, built as an asynchronous RESTful API.

## Tech Stack

- **Framework:** FastAPI
- **Database:** SQLite + SQLAlchemy (Async) + aiosqlite
- **Package Manager:** `uv`
- **Containerization:** Docker & Docker Compose
- **Third-Party API:** Art Institute of Chicago API

## Setup and Run Instructions

### Option 1: Running via Docker (Recommended)

1. Make sure you have Docker and Docker Compose installed.
2. Open a terminal in the root of the project.
3. Run the following command:
   ```bash
   docker-compose up --build
   ```
4. The API will be available at `http://localhost:8000`.

### Option 2: Running Locally (with `uv`)

1. Install `uv` (Fast Python package manager) if you don't have it.
2. Run the following command to install dependencies:
   ```bash
   uv sync
   ```
3. Start the server:
   ```bash
   uv run run.py
   ```

## API Documentation & Endpoints

FastAPI provides an automatic, interactive API documentation.
Once the application is running, you can access the **Swagger UI (OpenAPI)** at:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

## Example Requests

### 1. Create a Travel Project with Places

**POST** `/projects/`

```json
{
  "name": "My trip to Chicago",
  "description": "Art exploration",
  "start_date": "2026-05-27",
  "places": [
    {
      "external_id": "65133",
      "notes": "Must see the panel"
    },
    {
      "external_id": "48299"
    }
  ]
}
```

### 2. Add a new place to an existing project

**POST** `/projects/{project_id}/places/`

```json
{
  "external_id": "87741",
  "notes": "Decided to visit this one too"
}
```

### 3. Update a Place (Mark as visited)

**PATCH** `/places/{place_id}`

```json
{
  "notes": "It was amazing! Highly recommended.",
  "is_visited": true
}
```

### 4. Delete a project

**DELETE** `/projects/{project_id}`
