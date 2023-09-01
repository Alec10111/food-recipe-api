# Food Recipes API

This project is a Food Recipes API built using FastAPI and MongoDB, with JWT authentication. It allows users to create, consult and manage food recipes. The API endpoints are protected using JWT tokens.
### Features
- Create, retrieve, list, update, and delete food recipes. 
- User registration and login with JWT authentication. 
- Secure endpoints using JWT tokens. 
- MongoDB used as the database backend. 
- Docker Compose setup for easy deployment.

### Tech stack
The API was built with Fastapi

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

- Docker and Docker Compose are installed on your machine. The easiest way to do this is to install Docker Desktop, which is available in Linux, Mac and Windos, and features docker compose.
- If you want to run the project locally, Python 3.8+ needs to be installed. For the database you can either spin up mongodb locally (you will need to install it) or using a docker container.

### Installation

Clone the repository (or unzip it if provided as a zip):

```bash
git clone https://github.com/your-username/food-recipes-api.git
cd food-recipes-api
```
```bash
unzip recipes-api.zip
```
#### Local Install
Set up a virtual environment:

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
Update the environment variables in the `.env` file according to your preferences.
- For the purposes of this project any secret keys will work, but in real scenarios it is recommended to use a strong key. You can generate a key using `openssl rand -hex 32`
- You have to set the variable `MONGO_CONNECTION_STRING` depending on how you spin up the database. If you run the whole project with docker compose, use 
```txt
MONGO_CONNECTION_STRING="mongodb://mongo:27017/"
```
matching the service name in the compose yaml. Otherwise you use `localhost` instead of `mongo`

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
Optionally, if you are using an IDE like PyCharm, you can run the `main.py` file directly from the editor, which will be equivalent to the command above

## API docs
FastAPI features swagger documentation to consult and try all available endpoints, as well as a feature to authenticate your user and access protected endpoints

Once the server is up, access the API documentation at http://localhost:8000/docs.

## Testing
Tests are written using `pytest`, and in order to run them you can use `docker compose run --rm -it app pytest` or if you installed the project locally, calling `pytest` in the terminal will be equivalent.
If you are using IDE like pycharm you can also run and debug the tests directly in the editor.

## Usage

### Recipes
Recipes consists of title, description, ingredients and steps. They also have information of the user that created them.
Using the available endpoints for `/recipes` you can 
- create a recipe
- retrieve a single recipe
- list all recipes
  - You can filter by ingredients adding an `ingredients` query param and a list of ingredients separated by comma, for example:
  - `http://localhost:8000/recipes?ingredients=eggs,avocado`
- update a recipe (only the ones created by yourself)
- delete a recipe (only the ones created by yourself)

This is an example of a json body to create a recipe:
```json
{
	"title": "Fried Eggs with Bacon",
	"description": "A simple breakfast recipe",
	"ingredients": [
		{
			"name": "Eggs",
			"quantity": "2 units"
		},
		{
			"name": "Bacon strips",
			"quantity": "3 units"
		}
	],
	"steps": [
		{
			"order": 1,
			"description": "Fry the eggs in the pan"
		},
		{
			"order": 2,
			"description": "Fry the bacon in the pan"
		}
	]
}
```
To update a recipe you have to provide the fields that you want to update in the body of the request. If you wanted to add a step to the previous recipe you would use this body:
```json
{
	"steps": [
		{
			"order": 1,
			"description": "Fry the eggs in the pan"
		},
		{
			"order": 2,
			"description": "Fry the bacon in the pan"
		},
      		{
			"order": 3,
			"description": "Serve quick, cold eggs and bacon are not nice"
		}
	]
}
```
### Users
Available operations for users are the following
- sign up by creating a user
A json example to create a user:
```json
{
	"username": "test_user",
	"fullname": "test user",
	"email": "test@gmail.com",
	"password": "12345"
}
```
- retrieving a user
- list all users (only displays id and username)
- retrieving current user

### Auth
In order to access all the endpoints in the project you will need to login. You can do it directly in the docs page clicking the 'Authorize' button and entering correct username and password for an existing user
- Get request for recipes (list and retrieve) can be accessed without login.
