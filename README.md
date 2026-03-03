# Jina AI Reranker API Compatible Service

A FastAPI implementation that provides a compatible API interface for Jina AI's reranker service, connecting to a LiteLLM reranking backend.

## Features

- ✅ Jina AI Reranker API compatibility
- 🚀 Built with FastAPI for high performance
- 🔌 Connects to LiteLLM reranking service
- 🐳 Docker support for easy deployment
- 🔐 Secure by default with non-root user in Docker
- 🛠️ Configurable through environment variables

## Prerequisites

- Python 3.12+
- Docker (optional, for containerized deployment)
- Access to a LiteLLM service with reranking capabilities

## Installation

### Using Python directly

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Navigate to the source directory:
   ```bash
   cd src
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on the environment variables described below.

5. Run the application:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### Using Docker

1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. The API will be available at `http://localhost:8000`

## Configuration

The application can be configured using the following environment variables:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `RERANKER_MODEL` | The model name to use for reranking | `rerank-english-v3.0` |
| `LITELLM_BASE_URL` | Base URL of the LiteLLM service | `http://0.0.0.0:4000` |

Create a `.env` file in the project root with your configuration:
```env
RERANKER_MODEL=rerank-english-v3.0
LITELLM_BASE_URL=http://your-litellm-service:4000
```

## API Endpoints

### POST `/rerank`

Rerank documents based on their relevance to a query.

**Request Body:**
```json
{
  "model": "rerank-english-v3.0",
  "query": "What is the capital of France?",
  "documents": [
    "Berlin is the capital of Germany.",
    "Paris is the capital of France.",
    "Madrid is the capital of Spain."
  ],
  "top_n": 3,
  "return_documents": true
}
```

**Response:**
```json
{
  "results": [
    {
      "index": 1,
      "relevance_score": 0.95,
      "document": {
        "text": "Paris is the capital of France."
      }
    },
    {
      "index": 0,
      "relevance_score": 0.12,
      "document": {
        "text": "Berlin is the capital of Germany."
      }
    },
    {
      "index": 2,
      "relevance_score": 0.08,
      "document": {
        "text": "Madrid is the capital of Spain."
      }
    }
  ]
}
```

### GET `/health`

Health check endpoint to verify the service is running.

**Response:**
```json
{
  "status": "ok"
}
```

## Development

### Setting up the development environment

1. Ensure you have Python 3.12+ installed
2. Install dependencies:
   ```bash
   pip install -r src/requirements.txt
   ```

### Running tests

Currently, no test suite is implemented. Consider adding tests for your specific use case.

### Code structure

```
├── src/
│   ├── main.py          # Main FastAPI application
│   ├── requirements.txt # Python dependencies
│   └── pyproject.toml   # Project metadata
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
└── README.md            # This file
```

## Deployment

### Deploying with Docker

1. Build the Docker image:
   ```bash
   docker build -t jina-reranker-api .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file .env jina-reranker-api
   ```

### Deploying with Docker Compose

1. Update the `.env` file with your configuration
2. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

