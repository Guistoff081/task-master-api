# Task Master API

A comprehensive task management API built with FastAPI, SQLModel, and PostgreSQL.

## 🚀 Features

- User authentication with JWT tokens
- Task management (CRUD operations)
- Role-based access control (Regular users and Superusers)
- Database migrations with Alembic
- Error tracking with Sentry
- Comprehensive test coverage
- Docker support for easy deployment

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLModel
- **Authentication**: JWT with PassLib and bcrypt
- **Testing**: pytest
- **Linting**: ruff, mypy
- **Container**: Docker
- **Error Tracking**: Sentry
- **Documentation**: OpenAPI (Swagger)

## 📋 Prerequisites

- Python 3.13+
- PostgreSQL
- Docker and Docker Compose (optional)

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Guistoff081/task-master-api.git
   cd task-master-api
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run with Docker**
   ```bash
   docker compose up -d
   ```

   Or **Run locally**:
   ```bash
   # Create virtual environment
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate  # Windows

   # Install dependencies
   uv sync

   # Run migrations
   alembic upgrade head

   # Start the server
   uvicorn app.main:app --reload
   ```

4. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Email interface (development): http://localhost:1080


## 💼 Development Setup

1. Install pre-commit hooks:
   ```bash
   # Install pre-commit if you haven't already
   pip install pre-commit

   # Install the git hooks
   pre-commit install -t pre-commit -t pre-push
   ```

2. The hooks will now run automatically:
   - `format.sh` and `lint.sh` run on every commit
   - `test.sh` runs before every push

3. Run hooks manually:
   ```bash
   # Run all hooks
   pre-commit run --all-files

   # Run individual hooks
   pre-commit run format --all-files
   pre-commit run lint --all-files
   pre-commit run test --all-files
   ```

## 🧪 Testing
Run the test suite:

```bash
./scripts/prepare-test.sh
./scripts/test.sh
```

## 📚 API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## ✈️ Deployment

Check out deployment docs: [Deployment](./deployment.md)

## 🔒 Authentication

The API uses JWT tokens for authentication. To access protected endpoints:

1. Register a new user at `/api/register`
2. Get your access token at `/api/login`
3. Include the token in your requests:
   ```bash
   curl -H "Authorization: Bearer your_token" http://localhost:8000/api/tasks/
   ```

## 🐳 Docker Support

The project includes a complete Docker setup with:
- PostgreSQL database
- API service
- Mail catcher (for development)
- Automatic database migrations
- Health checks

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
