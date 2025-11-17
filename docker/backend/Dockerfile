# Stage 1: Build the application
FROM python:3.9-slim as builder

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy only files needed for dependency installation
COPY backend/poetry.lock backend/pyproject.toml /app/

# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Stage 2: Create the final, smaller image
FROM python:3.9-slim

WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /app /app

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "-k", "uvicorn.worker.UvicornWorker", "-c", "gunicorn_conf.py", "backend.main:app"]
