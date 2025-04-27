# **S4E Internship Task AI Code App**

A web-based Ollama integrated code generator for Python security automation tasks.

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0.1-green.svg)
![Docker](https://img.shields.io/badge/docker-latest-blue.svg)
![Kubernetes](https://img.shields.io/badge/kubernetes-latest-blue.svg)

## Features

* AI-powered Python code generation for especially security tasks
* Integrated with Ollama API for code generation
* Real-time code preview and syntax highlighting
* Docker and Kubernetes ready deployment
* Model selection capability (using tinyllama for resource efficiency)
* Copy-to-clipboard functionality
* Responsive web interface with modern UI

## Project Structure
```
.
├── app.py                 # Flask application with endpoints
├── model.py              # Ollama integration and model handling
├── templates/
│   └── page.html        # Web interface
├── ai-code-app/         # Helm chart directory
│   ├── Chart.yaml      # Chart metadata
│   ├── values.yaml     # Default chart values
│   └── templates/      # Kubernetes manifests
│       ├── deployment.yaml
│       ├── service.yaml
│       └── ollama-deployment.yaml
└── Dockerfile           # Container build instructions
```

## Prerequisites

* Docker Desktop
* Kubernetes cluster (Minikube)
* Helm 3
* Python 3.13+
* Flask
* 8GB+ RAM recommended
* 6+ CPU cores recommended

## Local Development

### 1. Set Up Python Environment

First, create and activate a virtual environment:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate it on macOS
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install and Start Ollama

```bash
# Install Ollama on macOS
curl https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# In a new terminal, pull the required model
ollama pull tinyllama
```

### 4. Run the Application

```bash
python app.py
```
Visit http://localhost:5000

## Docker Deployment

### Getting Image from DockerHub

1. Pull the pre-built image:
```bash
docker pull uygaregemen/ai-code-app:latest
```

2. Run the container:
```bash
docker run -d \
  -p 5000:5000 \
  --name ai-code-app \
  uygaregemen/ai-code-app:latest
```

### Environment Variables (Optional)
```bash
docker run -d \
  -p 5000:5000 \
  -e OLLAMA_HOST="http://localhost:11434" \
  --name ai-code-app \
  uygaregemen/ai-code-app:latest
```

## Local Kubernetes Setup with Minikube

### Prerequisites
- Docker Desktop
- Homebrew package manager

### Installation Steps

1. Install Minikube:
```bash
brew install minikube
```

2. Start Minikube with required resources:
```bash
minikube start --cpus=6 --memory=8g --driver=docker
```

3. Enable addons:
```bash
minikube addons enable metrics-server
minikube addons enable ingress
```

4. Install Helm:
```bash
brew install helm
```

5. Deploy the application:
```bash
helm install ai-code-app ./ai-code-app
```

6. Access the application:
```bash
minikube service ai-code-app
```

## API Endpoints

### GET /
- Returns the main web interface
- Response: HTML page

### POST /
- Generates code based on user input
- Request Body:
  ```json
  {
    "user_input": "string",
    "model": "string"
  }
  ```
- Response:
  ```json
  {
    "title": "string",
    "code_output": "string"
  }
  ```

### GET /models
- Returns available Ollama models
- Response:
  ```json
  {
    "models": ["tinyllama", "llama3.2", ...]
  }
  ```

## Deployment Updates

When you make changes to the application, follow these steps:

1. Build new Docker image:
```bash
docker build -t uygaregemen/ai-code-app:latest .
```

2. Push to Docker Hub:
```bash
docker push uygaregemen/ai-code-app:latest
```

3. Update Kubernetes deployment:
```bash
helm upgrade ai-code-app ./ai-code-app
kubectl rollout restart deployment ai-code-app
```

## Known Issues and Limitations

### Model Performance
1. **TinyLlama Limitations**
   - Slower response times compared to larger models
   - May produce inconsistent code quality
   - Resource-optimized for development environments

2. **Warm-up Issues**
   - Initial "Load failed" errors during model initialization
   - Workaround: Wait 30-60 seconds after deployment
   - Subsequent requests work normally

### Resource Requirements
- Minimum: 4 CPU, 6GB RAM
- Recommended: 8+ CPU, 10GB+ RAM
- Storage: 5GB free space

## Troubleshooting

### Common Issues
1. Pod in `Pending` state:
```bash
kubectl describe pod <pod-name>
```

2. Check Ollama logs:
```bash
kubectl logs -l app.kubernetes.io/component=ollama -f
```

3. Service connectivity:
```bash
kubectl get svc
minikube service list
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- [@uygaregemenocak](https://github.com/uygaregemenocak)


