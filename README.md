# S4E_Internship_Task
This is a mini task for s4e internship.
The program is designed for generating python code for the user request delivering just the code and the title.
It uses the ollama for generating code llama3 to be exact and flask for the backend with basic html structure.

## Running with Docker
This project includes a Docker setup for easy deployment and isolation of dependencies.

- **Python version:** 3.13-slim (as specified in the Dockerfile)
- **Dependencies:** Installed from `requirements.txt` inside a Python virtual environment
- **No required environment variables** (unless you add a `.env` file and uncomment the relevant line in `docker-compose.yaml`)
- **Exposed port:** 5000 (Flask default)
- **Runs as a non-root user** for improved security

### Build and Run
To build and start the application using Docker Compose:

```sh
docker compose up --build
```

The Flask app will be available at [http://localhost:5000](http://localhost:5000).

No additional configuration or persistent volumes are required for this project.
