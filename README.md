# PenPal - Django DRF Project

A Django REST Framework project with JWT authentication and CORS support.

## Technology Stack

- **Django 5.2.7**
- **Django REST Framework**
- **Python 3.14**
- **uv** - Python package manager
- **WhiteNoise** - Static file serving
- **Docker & Docker Compose** - Containerization

## Prerequisites

- Docker
- Docker Compose

## Quick Start with Docker

### 1. Create Environment File

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your preferred settings (optional for development).

### 2. Build and run the application

```bash
# Build and start the containers
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

The application will be available at: http://localhost:8000

### Stop the application

```bash
docker-compose down
```

### View logs

```bash
docker-compose logs -f
```

## Development without Docker

### Prerequisites
- Python 3.14
- uv package manager

### Setup

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -e .

# Run migrations
cd penpal
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Project Structure

```
penpal/
├── manage.py
├── penpal/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── pyproject.toml
├── uv.lock
├── Dockerfile
└── docker-compose.yml
```

## Environment Variables

The application uses environment variables for configuration. Copy `.env.example` to `.env` and configure your settings:

```bash
cp .env.example .env
```

### Available Variables

- `DEBUG` - Set to `True` for development, `False` for production
- `SECRET_KEY` - Django secret key (generate a secure one for production)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hostnames
- `DATABASE_URL` - Database connection string (optional, defaults to SQLite)
- `CORS_ALLOWED_ORIGINS` - Comma-separated list of CORS origins

Example `.env` file:

```env
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Important**: Never commit the `.env` file to version control. It should be in `.gitignore` (already configured).

## API Endpoints

### Authentication
- `/api/token/` - Obtain JWT token
- `/api/token/refresh/` - Refresh JWT token

### Admin
- `/admin/` - Django admin panel

## Features

- ✅ Django REST Framework
- ✅ JWT Authentication (djangorestframework-simplejwt)
- ✅ CORS Support
- ✅ WhiteNoise for static files
- ✅ SQLite database (SQLite3)
- ✅ Dockerized for easy deployment
- ✅ Environment-based configuration

## Docker Commands

### Using Make (Recommended)

```bash
# Build and start containers in one command
make up-build

# Or build and start separately
make build
make up

# View logs
make logs

# Run migrations
make migrate

# Create superuser
make createsuperuser

# Django shell
make shell

# Stop containers
make down

# Clean everything (remove containers and volumes)
make clean

# Show all available commands
make help
```

### Manual Docker Commands

#### Build the image
```bash
docker build -t penpal .
```

#### Run a container
```bash
docker run -p 8000:8000 penpal
```

#### Run migrations
```bash
docker-compose exec web python manage.py migrate
```

#### Create superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

#### Django shell
```bash
docker-compose exec web python manage.py shell
```

#### View database
```bash
docker-compose exec web python manage.py dbshell
```

## Production Deployment

### Using docker-compose.prod.yml

1. Update your `.env` file with production settings:

```env
DEBUG=False
SECRET_KEY=generate-a-secure-secret-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

2. Build and run production containers:

```bash
# Build for production
docker-compose -f docker-compose.prod.yml build

# Start production containers
docker-compose -f docker-compose.prod.yml up -d
```

**Security Note**: In production:
- Set `DEBUG=False` in `.env`
- Use a strong, randomly generated `SECRET_KEY`
- Specify your actual domain in `ALLOWED_HOSTS`
- Consider using a production-ready database (PostgreSQL, MySQL) instead of SQLite

## Notes

- The application uses SQLite by default
- Static and media files are persisted using Docker volumes
- In production, set `DEBUG=False` and update `SECRET_KEY`
- Configure `ALLOWED_HOSTS` in production settings
- Consider using PostgreSQL or MySQL for production databases

## License

MIT

