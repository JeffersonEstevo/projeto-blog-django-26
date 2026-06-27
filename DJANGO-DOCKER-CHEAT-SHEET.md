# Docker & Django: The Ultimate Cheat Sheet

## Introduction to Docker and Django

Docker revolutionizes Django development by providing:
- **Consistent environments** across development, testing, and production
- **Isolation** of dependencies and services
- **Simplified collaboration** - no more "it works on my machine"
- **Easy scaling** and deployment
- **Microservices-ready** architecture

This guide covers everything from basic setup to advanced production configurations.

---

## 1. Setting Up a Django Project

### Basic Project Structure

```text
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── apps/
    ├── app1/
    └── app2/
```

### Creating a `requirements.txt`

**Manual:**
```bash
pip freeze > requirements.txt
```

**Example `requirements.txt`:**
```text
Django==4.2.1
psycopg2-binary==2.9.6
gunicorn==20.1.0
django-environ==0.9.0
django-cors-headers==3.14.0
djangorestframework==3.14.0
```

---

## 2. Dockerizing a Django Application

### Creating a `Dockerfile`

**Basic Development `Dockerfile`:**
```dockerfile
# Stage 1: Build stage
FROM python:3.11-slim-buster AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create a user to run the application
RUN addgroup --system --gid 1001 django \
    && adduser --system --uid 1001 --gid 1001 django

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

**Production `Dockerfile`:**
```dockerfile
# Stage 1: Builder
FROM python:3.11-slim-buster AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final
FROM python:3.11-slim-buster

WORKDIR /app

# Copy from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
```

### Creating a `docker-compose.yml`

**Development `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: myproject_db
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=myproject_db
      - POSTGRES_USER=myproject_user
      - POSTGRES_PASSWORD=myproject_password
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U myproject_user -d myproject_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: myproject_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  web:
    build: .
    container_name: myproject_web
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/static
      - media_volume:/app/media
    ports:
      - "8000:8000"
    environment:
      - DJANGO_SETTINGS_MODULE=myproject.settings.dev
      - DB_NAME=myproject_db
      - DB_USER=myproject_user
      - DB_PASSWORD=myproject_password
      - DB_HOST=db
      - DB_PORT=5432
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  celery:
    build: .
    container_name: myproject_celery
    command: celery -A myproject worker -l info
    volumes:
      - .:/app
    environment:
      - DJANGO_SETTINGS_MODULE=myproject.settings.dev
      - DB_NAME=myproject_db
      - DB_USER=myproject_user
      - DB_PASSWORD=myproject_password
      - DB_HOST=db
      - DB_PORT=5432
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - db
      - redis
      - web

  celery-beat:
    build: .
    container_name: myproject_celery_beat
    command: celery -A myproject beat -l info
    volumes:
      - .:/app
    environment:
      - DJANGO_SETTINGS_MODULE=myproject.settings.dev
    depends_on:
      - celery

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:
```

**Production `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    networks:
      - backend

  web:
    build: .
    restart: always
    command: gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application
    volumes:
      - static_volume:/app/static
      - media_volume:/app/media
    expose:
      - "8000"
    environment:
      - DJANGO_SETTINGS_MODULE=myproject.settings.prod
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=db
      - DB_PORT=5432
    depends_on:
      - db
    networks:
      - backend

  nginx:
    image: nginx:alpine
    restart: always
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/static
      - media_volume:/media
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web
    networks:
      - backend

networks:
  backend:

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### Creating a `.dockerignore`

```text
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
*.pot
*.pyc
local_settings.py
db.sqlite3
media/
static/

# Docker
Dockerfile
.dockerignore
docker-compose*.yml

# Version Control
.git/
.gitignore
.svn/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local
.env.*.local
```

---

## 3. Django Settings Configuration

### `settings/base.py` (Common Settings)

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-key-for-dev')

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'apps.app1',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# Database - Will be overridden in dev/prod settings
DATABASES = {}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

### `settings/dev.py` (Development Settings)

```python
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'myproject_db'),
        'USER': os.environ.get('DB_USER', 'myproject_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'myproject_password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### `settings/prod.py` (Production Settings)

```python
from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'CONN_MAX_AGE': 60,
    }
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# CORS settings
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')

# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

---

## 4. Essential Docker Commands

### Image Management

| Command | Description |
|---------|-------------|
| `docker build -t myproject:latest .` | Build image from Dockerfile |
| `docker build -t myproject:latest -f Dockerfile.prod .` | Build with custom Dockerfile |
| `docker images` | List all images |
| `docker rmi <image_id>` | Remove image |
| `docker rmi $(docker images -q)` | Remove all images |
| `docker tag myproject:latest myrepo/myproject:v1` | Tag image for registry |
| `docker push myrepo/myproject:v1` | Push image to registry |
| `docker pull myrepo/myproject:v1` | Pull image from registry |
| `docker image prune -a` | Remove unused images |

### Container Management

| Command | Description |
|---------|-------------|
| `docker run -d -p 8000:8000 --name myapp myproject:latest` | Run container in background |
| `docker run -it --rm myproject:latest /bin/bash` | Run container interactively |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers |
| `docker stop <container_id>` | Stop container |
| `docker start <container_id>` | Start stopped container |
| `docker restart <container_id>` | Restart container |
| `docker rm <container_id>` | Remove container |
| `docker rm -f <container_id>` | Force remove running container |
| `docker rm $(docker ps -a -q)` | Remove all containers |
| `docker logs <container_id>` | View container logs |
| `docker logs -f <container_id>` | Follow logs |
| `docker exec -it <container_id> /bin/bash` | Execute bash inside container |
| `docker exec <container_id> python manage.py migrate` | Run migration in container |
| `docker cp <container_id>:/app/file.txt .` | Copy from container |

### Docker Compose Commands

| Command | Description |
|---------|-------------|
| `docker-compose up` | Start all services |
| `docker-compose up -d` | Start in detached mode |
| `docker-compose up --build` | Rebuild and start |
| `docker-compose down` | Stop and remove containers |
| `docker-compose down -v` | Stop and remove containers + volumes |
| `docker-compose ps` | List services |
| `docker-compose logs` | View logs from all services |
| `docker-compose logs -f web` | Follow logs for web service |
| `docker-compose exec web bash` | Execute command in service |
| `docker-compose exec web python manage.py migrate` | Run Django migration |
| `docker-compose restart web` | Restart specific service |
| `docker-compose build --no-cache` | Rebuild without cache |
| `docker-compose config` | Validate compose file |
| `docker-compose run --rm web python manage.py test` | Run command in new container |

---

## 5. Database Integration

### PostgreSQL Configuration

**Django Settings:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}
```

**PostgreSQL Docker Service:**
```yaml
db:
  image: postgres:15
  environment:
    POSTGRES_DB: myproject_db
    POSTGRES_USER: myproject_user
    POSTGRES_PASSWORD: myproject_password
  volumes:
    - postgres_data:/var/lib/postgresql/data
  ports:
    - "5432:5432"
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U myproject_user"]
    interval: 10s
    timeout: 5s
    retries: 5
```

### MySQL Configuration

**Django Settings:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}
```

**MySQL Docker Service:**
```yaml
db:
  image: mysql:8.0
  environment:
    MYSQL_DATABASE: myproject_db
    MYSQL_USER: myproject_user
    MYSQL_PASSWORD: myproject_password
    MYSQL_ROOT_PASSWORD: root_password
  volumes:
    - mysql_data:/var/lib/mysql
  ports:
    - "3306:3306"
  command: --default-authentication-plugin=mysql_native_password
```

### Running Migrations

**Manual Migration:**
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

**Migration Script (migrate.sh):**
```bash
#!/bin/bash
echo "Running migrations..."
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
echo "Migrations complete!"
```

---

## 6. Static and Media Files

### Development Configuration

**Django Settings:**
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**Docker Compose Volumes:**
```yaml
volumes:
  - static_volume:/app/static
  - media_volume:/app/media
```

### Production Configuration with Nginx

**Nginx Configuration (nginx/nginx.conf):**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream django {
        server web:8000;
    }

    server {
        listen 80;
        server_name example.com;

        location /static/ {
            alias /static/;
        }

        location /media/ {
            alias /media/;
        }

        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

**Collect Static Files:**
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

---

## 7. Advanced Docker Concepts

### Custom Entrypoints

**entrypoint.sh:**
```bash
#!/bin/bash
set -e

# Wait for database
if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for PostgreSQL..."
    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.1
    done
    echo "PostgreSQL started"
fi

# Run migrations
python manage.py migrate

# Create superuser if needed
if [ "$CREATE_SUPERUSER" = "true" ]; then
    python manage.py createsuperuser --noinput || true
fi

# Execute the command
exec "$@"
```

**Dockerfile with Entrypoint:**
```dockerfile
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
```

### Environment Variables

**.env file:**
```env
# Database
DB_NAME=myproject_db
DB_USER=myproject_user
DB_PASSWORD=myproject_password
DB_HOST=db
DB_PORT=5432

# Django
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=myproject.settings.prod
ALLOWED_HOSTS=example.com,www.example.com

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=user@gmail.com
EMAIL_HOST_PASSWORD=app-password

# CORS
CORS_ALLOWED_ORIGINS=https://example.com,https://www.example.com
```

**Using .env in docker-compose:**
```yaml
services:
  web:
    env_file:
      - .env
    environment:
      - CREATE_SUPERUSER=true
```

### Image Optimization

**Multi-stage Build:**
```dockerfile
# Builder stage
FROM python:3.11-slim-buster AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim-buster
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "myproject.wsgi"]
```

**Optimization Tips:**
1. Use specific base images (`python:3.11-slim-buster`)
2. Combine RUN commands to reduce layers
3. Use `.dockerignore` to exclude unnecessary files
4. Leverage build cache with proper COPY order
5. Remove package managers and temp files
6. Use multi-stage builds to reduce size
7. Set appropriate environment variables

**Example Optimized Dockerfile:**
```dockerfile
FROM python:3.11-slim-buster AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim-buster
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

USER 1000:1000
EXPOSE 8000
CMD ["gunicorn", "myproject.wsgi"]
```

---

## 8. Troubleshooting Common Issues

### Connection Refused Errors

**Problem:** Django can't connect to database
**Solution:**
- Check database service is running: `docker-compose ps`
- Verify connection settings in settings.py
- Ensure database container is healthy
- Wait for database to be ready before starting web

**Fix with healthcheck:**
```yaml
services:
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d db"]
      interval: 10s
      timeout: 5s
      retries: 5
  
  web:
    depends_on:
      db:
        condition: service_healthy
```

### Permission Issues

**Problem:** Permission denied errors with volumes
**Solution:**
- Use non-root user in Dockerfile
- Set proper user IDs
- Use `chown` in entrypoint

**Fix:**
```dockerfile
RUN useradd -m -u 1000 django
USER django
```

### Port Conflicts

**Problem:** `Error starting userland proxy: listen tcp4 0.0.0.0:8000: bind: address already in use`
**Solution:**
- Stop other containers using the port: `docker stop $(docker ps -q)`
- Change port mapping: `"8001:8000"`
- Check for other processes: `lsof -i :8000`

### Dependency Conflicts

**Problem:** Package installation fails
**Solution:**
- Pin exact versions in requirements.txt
- Use specific base image versions
- Check for system dependencies
- Use Python virtual environment

**Fix:**
```dockerfile
# Install system dependencies first
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Then install Python packages
COPY requirements.txt .
RUN pip install -r requirements.txt
```

### Static Files Not Loading

**Problem:** 404 errors for static files
**Solution:**
- Verify STATIC_URL and STATIC_ROOT settings
- Check volume mounts
- Run collectstatic
- Check Nginx configuration

**Fix:**
```bash
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart
```

### Memory/Performance Issues

**Problem:** Containers consuming too much memory
**Solution:**
- Set memory limits in docker-compose
```yaml
services:
  web:
    mem_limit: 512m
    mem_reservation: 256m
    cpus: '0.5'
```

### Database Connection Limits

**Problem:** "FATAL: remaining connection slots are reserved"
**Solution:**
- Reduce Django connection pool
- Increase PostgreSQL max_connections
- Use connection pooling middleware

**Django Settings:**
```python
DATABASES = {
    'default': {
        'CONN_MAX_AGE': 60,
        'CONN_HEALTH_CHECKS': True,
    }
}
```

---

## 9. Useful Docker Compose Extensions

### Health Checks

```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Resource Limits

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### Logging Configuration

```yaml
services:
  web:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Multiple Networks

```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true

services:
  nginx:
    networks:
      - frontend
      - backend
  web:
    networks:
      - backend
  db:
    networks:
      - backend
```

---

## 10. Quick Reference Card

### Common Development Workflow

| Step | Command |
|------|---------|
| Build | `docker-compose up --build` |
| Start | `docker-compose up -d` |
| Logs | `docker-compose logs -f` |
| Stop | `docker-compose down` |
| Migrations | `docker-compose exec web python manage.py migrate` |
| Shell | `docker-compose exec web python manage.py shell` |
| Tests | `docker-compose exec web python manage.py test` |
| Static | `docker-compose exec web python manage.py collectstatic` |
| Superuser | `docker-compose exec web python manage.py createsuperuser` |
| Bash | `docker-compose exec web /bin/bash` |

### Database Commands

| Task | Command |
|------|---------|
| Backup | `docker exec -t myproject_db pg_dump -U user myproject_db > backup.sql` |
| Restore | `cat backup.sql \| docker exec -i myproject_db psql -U user myproject_db` |
| Shell | `docker exec -it myproject_db psql -U user myproject_db` |
| Reset | `docker-compose down -v && docker-compose up -d` |

### Container Cleanup

```bash
# Stop all containers
docker stop $(docker ps -a -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Remove all images
docker rmi $(docker images -q)

# Remove all volumes
docker volume rm $(docker volume ls -q)

# Full cleanup
docker system prune -a --volumes
```

### Quick Debugging

```bash
# Check running containers
docker ps

# Check all containers
docker ps -a

# View logs for web
docker-compose logs web

# View last 50 lines
docker-compose logs --tail=50 web

# Follow logs with timestamp
docker-compose logs -f --timestamps

# Check container details
docker inspect myproject_web

# Check container resource usage
docker stats

# Execute Python inside container
docker-compose exec web python

# Test Django settings
docker-compose exec web python -c "import django; django.setup(); print(django.conf.settings.DATABASES)"
```

---

## 11. Security Best Practices

### Dockerfile Security

```dockerfile
# Use specific image version
FROM python:3.11-slim-buster

# Avoid running as root
RUN useradd -m -u 1000 django
USER django

# Don't expose sensitive data
ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY

# Use multi-stage builds
# Use .dockerignore

# Scan for vulnerabilities
# docker scan myproject:latest
```

### Production Settings

```python
# Always use environment variables for secrets
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Disable debug mode
DEBUG = False

# Restrict hosts
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Use HTTPS
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Use secure headers
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Container Security

```yaml
services:
  web:
    security_opt:
      - no-new-privileges:true
    read_only: true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    tmpfs:
      - /tmp
    mem_limit: 512m
```

---

## 12. Monitoring and Logging

### Health Check Endpoint

```python
# urls.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'healthy'})

urlpatterns = [
    path('health/', health_check),
]
```

### Logging Configuration

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

---

## 13. Deploying to Production

### Pre-deployment Checklist

- [ ] Environment variables configured
- [ ] Secret key set
- [ ] Debug mode disabled
- [ ] Allowed hosts configured
- [ ] HTTPS configured
- [ ] Static files collected
- [ ] Database migrations run
- [ ] Database backed up
- [ ] Health checks implemented
- [ ] Monitoring configured
- [ ] Logging configured
- [ ] Resource limits set

### Deployment Commands

```bash
# Pull latest code
git pull

# Rebuild and start
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Clear cache
docker-compose -f docker-compose.prod.yml exec redis redis-cli FLUSHALL

# Restart services
docker-compose -f docker-compose.prod.yml restart
```

---

## 14. Additional Resources

### Useful Images

| Image | Purpose |
|-------|---------|
| `python:3.11-slim-buster` | Django application |
| `postgres:15` | PostgreSQL database |
| `redis:7-alpine` | Redis cache |
| `nginx:alpine` | Reverse proxy |
| `celery/celery:latest` | Celery worker |
| `rabbitmq:3-management` | Message broker |

### Essential Packages

```text
django==4.2.1
django-environ==0.9.0
django-cors-headers==3.14.0
djangorestframework==3.14.0
psycopg2-binary==2.9.6
gunicorn==20.1.0
redis==4.5.5
celery==5.3.1
django-celery-results==2.5.0
django-redis==5.2.0
whitenoise==6.4.0
```

---

## Conclusion

This cheat sheet covers the essential Docker and Django commands, configurations, and best practices for building, developing, and deploying Dockerized Django applications. Keep this guide handy for quick reference, and remember to always follow security best practices in production environments.

**Pro Tips:**
- Use `.env` files for environment variables
- Implement health checks for all services
- Always use specific image tags, never `latest`
- Keep images small and secure
- Regular updates and security patches
- Backup databases regularly
- Monitor logs and metrics
- Test in staging before production