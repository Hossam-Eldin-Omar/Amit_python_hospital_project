FROM python:3.12-slim

# Install system dependencies for Poetry
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Configure Poetry to not create virtual environment and install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Copy the entire project
COPY . .

# Set Python path to include src directory
ENV PYTHONPATH="/app/src:/app"

# Set environment variables for ScyllaDB connection
ENV SCYLLA_HOST=scylla-node
ENV SCYLLA_PORT=9042

# Default command - test database connection
CMD ["python", "-m", "src.database.connection"]