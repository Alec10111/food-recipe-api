# Food Recipes API

This project is a Food Recipes API built using FastAPI and MongoDB, with JWT authentication. It allows users to create, update, and manage food recipes. The API endpoints are protected using JWT tokens.
Features

- Create, retrieve, update, and delete food recipes. 
- User registration and login with JWT authentication. 
- Secure endpoints using JWT tokens. 
- MongoDB used as the database backend. 
- Docker Compose setup for easy deployment.

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

    Docker and Docker Compose are installed on your machine.
    Python 3.8+ is installed.

### Installation

Clone the repository:

```bash
git clone https://github.com/your-username/food-recipes-api.git
cd food-recipes-api
```

Set up a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
Install project dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

Rename .env.example to .env and configure the environment variables:

```bash
mv .env.example .env
```

Update the environment variables in the .env file according to your preferences.

### Running with Docker Compose

Build and start the containers:

```bash
docker-compose up --build
```

### Running without Docker

Start the FastAPI server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Access the API documentation at http://localhost:8000/docs.

### Usage
- Register a new user and obtain JWT tokens. 
- Use the tokens to access protected endpoints for managing recipes.