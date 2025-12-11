# klm-notes-api

Simple Flask-based Notes API with PostgreSQL, designed to run locally using Docker Compose.

Prerequisites
- `git` is installed
- `python` is installed
- `docker` and `docker-compose` is installed and running

Local Setup Instructions

1. Clone the repository

	 ```bash
	 git clone https://github.com/AhmedSoliman92/klm-notes-api.git
	 cd klm-notes-api
	 ```

2. Start the application with Docker Compose

	 ```bash
	 docker-compose up --build -d
	 ```

	 - The Compose file starts two services: `flask-app` and `postgresql`.
	 - The Flask app is exposed on host port `5100` (mapped to container port `5000`).

3. Check logs (optional)

	 ```bash
	 docker-compose logs -f flask-app
     docker-compose logs -f postgresql
	 ```

4. Stop and remove containers

	 ```bash
	 docker-compose down
	 ```

API Usage

The API base URL when running locally via Docker Compose is: `http://localhost:5100`

Endpoints

- `POST /notes` — Create a new note
	- Example:

		```bash
		curl -s -X POST http://localhost:5100/notes \
			-H "Content-Type: application/json" \
			-d '{"title": "First note", "content": "This is a note."}'
		```

- `GET /notes` — List all notes
	- Example:

		```bash
		curl -s http://localhost:5100/notes
		```

- `GET /notes/<id>` — Get a single note
	- Example:

		```bash
		curl -s http://localhost:5100/notes/1
		```

- `PUT /notes/<id>` — Update a note's `title` and/or `content`
	- Example:

		```bash
		curl -s -X PUT http://localhost:5100/notes/1 \
			-H "Content-Type: application/json" \
			-d '{"title": "Updated title", "content": "Updated content."}'
		```

- `DELETE /notes/<id>` — Delete a note
	- Example:

		```bash
		curl -s -X DELETE http://localhost:5100/notes/1
		```

Notes

- The Compose file maps the container's port `5000` to host `5100`; use `http://localhost:5100`.
- Environment variables are set in `docker-compose.yml` (development values). Adjust for production.
- If Postgres takes time to become healthy, `flask-app` depends on `postgresql`'s health check; it will try every 6 seconds for 5 times, if not check logs with `docker-compose logs -f postgresql`.

Running tests

There are pytest-based tests under the `tests/` directory. You can run them locally (outside Docker). Use the commands for your platform below.

macOS / Linux (bash or zsh)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
```

Windows (Command Prompt)

```cmd
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q
```

Note

- If your system requires `python3` rather than `python`, replace `python` / `pip` accordingly (e.g., `python3`, `pip3`).

<br>
<br>

# Continuous Integration / Continuous Deployment (CI/CD)
```

Workflow name: "CI/CD Pipeline"
Task: automatically lint, test, and build the Docker image for klm-note-api.

The pipeline is triggered automatically under the following conditions:
* On every push to the main branch.
* On every pull_request targeting the main branch.
```

### Configuration: Setting Up GitHub Secrets

```
To add these secrets:

1. Navigate to Settings: In GitHub repository, click the "Settings" tab.
2. Go to Secrets: In the left sidebar, navigate to "Security" -> "Secrets and variables" -> "Actions".
3. Add New Repository Secret: Click the "New repository secret" button and enter the following names and corresponding values:

Secret Name: DOCKER_USERNAME
Purpose: Your Docker Hub username.

Secret Name: DOCKER_PAT
Purpose: Your Docker Hub Personal Access Token (PAT) used for logging in and pushing images.

Secret Name: DB_PASSWORD
Purpose: The password used to reset the PostgreSQL user's password during the tests job.

Secret Name: DB_URL
Purpose: The full connection string used to connect to the test PostgreSQL database.
```
### You can manually trigger the full pipeline.
```

1. Navigate to Actions: Go to the "Actions" tab in GitHub repository.
2. Select the Workflow: In the left sidebar, click on the "CI/CD Pipeline" workflow.
3. Run Workflow: On the main workflow page, click the "Run workflow" dropdown button located on the right side.
4. Click the green "Run workflow" button.

```

### Workflow Stages
```

The pipeline is broken down into sequential jobs to ensure code quality and stability before building:

Job: lint
Dependency: None
Purpose: Checks code against established standards.


Job Name: tests
Dependency: lint
Purpose: Executes unit/integration tests after setting up the PostgreSQL database instance.


Job Name: build
Dependency: lint, tests
Purpose: Builds a multi-platform Docker image, tags it with version metadata, and pushes it to Docker Hub.
```