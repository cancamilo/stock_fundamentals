FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
# Copy project and lock files
COPY ./pyproject.toml ./uv.lock* /app/
# The uv.lock* will copy uv.lock if it exists.

# Install Python dependencies using uv (uv is now in /usr/local/bin, which is in PATH)
# --system installs packages into the global site-packages of the current Python environment
RUN uv pip install --system -r pyproject.toml

# Copy the rest of the backend source code into the container
COPY ./src /app/src

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
# uvicorn should be in PATH if installed by 'uv pip install --system'
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
