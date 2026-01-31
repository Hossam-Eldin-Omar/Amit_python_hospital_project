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
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to not create virtual environment first
RUN poetry config virtualenvs.create false

# Install dependencies (this will also sync the lock file if needed)
RUN poetry install --no-interaction --no-ansi --no-root

# Copy the entire project
COPY . .

# Set Python path to include src directory
ENV PYTHONPATH="/app/src:/app"

# Set environment variables for ScyllaDB connection
ENV SCYLLA_HOST=new-scylla-node
ENV SCYLLA_PORT=9042

# Expose Streamlit port
EXPOSE 8501

# Create .streamlit config directory
RUN mkdir -p /app/.streamlit

# Create streamlit credentials and config if they don't exist
RUN echo '[general]' > /app/.streamlit/credentials.toml && \
    echo 'email = ""' >> /app/.streamlit/credentials.toml

# Run Streamlit app
ENTRYPOINT []
CMD ["streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]