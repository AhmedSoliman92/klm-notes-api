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
