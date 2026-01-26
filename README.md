# Hospital Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/Poetry-1.8+-blue.svg)](https://python-poetry.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![ScyllaDB](https://img.shields.io/badge/ScyllaDB-5.0+-brightgreen.svg)](https://www.scylladb.com/)

**Hospital Management System** is a comprehensive Python-based healthcare management platform built with ScyllaDB for high-performance distributed data storage. It provides automated patient registration, data validation, and hospital operations management with professional logging and Docker containerization.

## <span id="table-of-contents"></span>📋 Table of Contents

- [Welcome](#welcome)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Development](#development)
- [Testing](#testing)
- [Docker Commands](#docker-commands)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## <span id="welcome"></span>🌟 Welcome

Welcome to the Hospital Management System! This guide is designed for developers, system administrators, and healthcare IT professionals collaborating on the platform. Inside you will find actionable setup steps, architecture notes, and collaboration expectations so new team members can contribute confidently. If you are unsure where to begin, start with the Quick Start section.

## <span id="features"></span>🎯 Features

### **Core System Components**
- **👤 Patient Management**: Comprehensive patient registration and profile management
- **🗄️ Distributed Database**: High-performance ScyllaDB backend with automatic schema initialization
- **📊 Data Validation**: Intelligent input validation and error handling
- **🔍 Advanced Search**: Patient lookup by ID, name, and other attributes
- **📝 Auto-Generated IDs**: UUID-based identification for patients and departments

### **Advanced Capabilities** 
- **Multi-threaded Architecture**: High-performance concurrent processing
- **Professional Logging**: Comprehensive logging with DEBUG, INFO, and ERROR levels
- **Web Interface**: Python-based CLI and database management interface
- **Dockerized Environment**: Complete containerization with easy deployment
- **Input Validation**: Date format validation, required field enforcement
- **Timestamp Tracking**: Automatic creation timestamp recording
- **Database Persistence**: ScyllaDB distributed NoSQL database integration

## <span id="prerequisites"></span>🔧 Prerequisites

Before setting up the Hospital Management System, ensure you have the following installed:

### Required Software

- **Python 3.9+**
  - Download from [python.org](https://www.python.org/downloads/)

- **Poetry** (for dependency management)
  - Install from [python-poetry.org](https://python-poetry.org/docs/#installation)

- **ScyllaDB 5.0+** (or Cassandra 4.0+)
  - Download from [scylladb.com](https://www.scylladb.com/download/)

- **Docker Desktop** (optional, for containerization)
  - Windows/macOS: [Docker Desktop](https://www.docker.com/products/docker-desktop)
  - Linux: [Docker Engine](https://docs.docker.com/engine/install/)

- **Git** (Latest version)
  - Download from [git-scm.com](https://git-scm.com/downloads)

### System Requirements

- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: At least 2GB free space
- **OS**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)

## <span id="installation"></span>🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/hospital-management.git
cd hospital-management
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
SCYLLA_HOST=localhost
SCYLLA_PORT=9042
SCYLLA_KEYSPACE=hospital
```

### 3. Install Dependencies

Using Poetry:

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### 4. Start ScyllaDB

```bash
# If using Docker
docker run -d --name scylla -p 9042:9042 scylladb/scylla

# Or if ScyllaDB is installed locally
scylladb
```

## <span id="quick-start"></span>⚡ Quick Start

### Run the Application

```bash
# Run the main application
python main.py
```

### Using Docker

```bash
# Build the Docker image
docker build -t hospital-management-app .

# Run the container with ScyllaDB network
docker run -it --rm --network scylla-net hospital-management-app python main.py
```

### Docker Compose

```bash
# Start both ScyllaDB and application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Access the Application

The application will:
1. Connect to ScyllaDB
2. Initialize the database schema
3. Prompt for patient data input
4. Display all patients in the database

### Example Usage

```
Enter new patient data
First name: John
Last name: Doe
Date of birth (YYYY-MM-DD): 1990-05-15
Phone: +1-555-123-4567

✓ Patient inserted with ID 550e8400-e29b-41d4-a716-446655440000

====================================================
PATIENTS IN DATABASE
====================================================
ID: 550e8400-e29b-41d4-a716-446655440000 | John Doe
  DOB: 1990-05-15
  Age: 34
  Phone: +1-555-123-4567
```

## <span id="configuration"></span>⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SCYLLA_HOST` | ScyllaDB host address | `localhost` | No |
| `SCYLLA_PORT` | ScyllaDB CQL port | `9042` | No |
| `SCYLLA_KEYSPACE` | Database keyspace name | `hospital` | No |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, ERROR) | `INFO` | No |

### Database Configuration

ScyllaDB Configuration in `.env`:

```env
SCYLLA_HOST=localhost
SCYLLA_PORT=9042
SCYLLA_KEYSPACE=hospital
```

For multi-node ScyllaDB clusters:

```env
SCYLLA_HOST=node1.example.com,node2.example.com,node3.example.com
SCYLLA_PORT=9042
SCYLLA_KEYSPACE=hospital
```

## <span id="usage"></span>📖 Usage

### Patient Registration Workflow

```bash
python main.py
```

**Steps:**
1. Application connects to ScyllaDB
2. Database schema is initialized (if not exists)
3. User is prompted to enter patient information:
   - First name (required)
   - Last name (required)
   - Date of birth in YYYY-MM-DD format (required)
   - Phone number (required)
4. Patient is inserted with auto-generated UUID
5. System displays all registered patients

### Data Input Format

```
First name: Required, alphanumeric
Last name: Required, alphanumeric
Date of birth: YYYY-MM-DD format (e.g., 1990-05-15)
Phone: Any format (e.g., +1-555-123-4567, (555) 123-4567)
```

## <span id="project-structure"></span>📁 Project Structure

```
hospital-management/
├── main.py                          # Main entry point
├── pyproject.toml                   # Poetry configuration
├── poetry.lock                      # Dependency lock file
├── dockerfile                       # Docker configuration
├── .env.example                     # Environment variables template
├── README.md                        # This file
├── logs/                            # Application logs directory
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py              # Application settings
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py            # ScyllaDB connection management
│   │   ├── init_db.py               # Database schema initialization
│   │   └── repositories/
│   │       ├── __init__.py
│   │       └── patient_repository.py # Patient data access layer
│   ├── models/
│   │   ├── __init__.py
│   │   ├── patient.py               # Patient model class
│   │   └── person.py                # Base Person model
│   └── utils/
│       ├── __init__.py
│       └── logger.py                # Logging configuration
└── __pycache__/                     # Python cache
```

## <span id="database-schema"></span>🗄️ Database Schema

### Keyspace: `hospital`

High-performance NoSQL keyspace with SimpleStrategy replication.

### Table: `patients`

Primary storage for patient information.

**Schema:**
```sql
CREATE TABLE IF NOT EXISTS patients (
    department_id UUID,
    patient_id UUID,
    first_name TEXT,
    last_name TEXT,
    date_of_birth TEXT,
    age INT,
    phone TEXT,
    created_at TIMESTAMP,
    PRIMARY KEY (department_id, patient_id)
)
WITH CLUSTERING ORDER BY (patient_id ASC)
```

**Fields:**
- `department_id` (UUID) - Partition key for scalability
- `patient_id` (UUID) - Clustering key and unique identifier
- `first_name` (TEXT) - Patient's first name
- `last_name` (TEXT) - Patient's last name
- `date_of_birth` (TEXT) - DOB in YYYY-MM-DD format
- `age` (INT) - Calculated age at registration
- `phone` (TEXT) - Contact phone number
- `created_at` (TIMESTAMP) - Registration timestamp

### Additional Tables

- `hospitals` - Hospital organization records
- `departments` - Department information

## <span id="development"></span>👨‍💻 Development

### Code Formatting

```bash
poetry run black src/
```

### Linting

```bash
poetry run flake8 src/
```

### Type Checking

```bash
poetry run mypy src/
```

### Code Style Guide

- Follow PEP 8 style guidelines
- Use type hints for function parameters and returns
- Write descriptive docstrings for modules and classes
- Keep functions focused and single-responsibility

## <span id="testing"></span>🧪 Testing

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_patient_registration.py

# Run with verbose output
poetry run pytest -v
```

### Test Coverage

```bash
poetry run pytest --cov=src
```

### Writing Tests

Tests are organized in the `tests/` directory and use pytest framework.

```python
def test_patient_registration():
    """Test patient registration process"""
    # Test implementation
    pass
```

## <span id="docker-commands"></span>🐳 Docker Commands

### Image Management

```bash
# Build Docker image
docker build -t hospital-management-app .

# Build without cache
docker build -t hospital-management-app . --no-cache
```

### Container Operations

```bash
# Run container
docker run -it --rm hospital-management-app python main.py

# Run with environment file
docker run -it --rm --env-file .env hospital-management-app python main.py

# Run in background
docker run -d --env-file .env hospital-management-app python main.py
```

### Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes
docker-compose down -v
```

### Network Configuration

```bash
# Create network for ScyllaDB
docker network create scylla-net

# Run ScyllaDB on network
docker run -d --network scylla-net --name scylladb scylladb/scylla

# Run application on same network
docker run -it --rm --network scylla-net hospital-management-app python main.py
```

## <span id="api-endpoints"></span>📡 API Endpoints

### Patient Management

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/patients` | GET | List all patients | Patient array |
| `/patients/<id>` | GET | Get patient by ID | Patient object |
| `/patients` | POST | Create new patient | Created patient object |
| `/patients/<id>` | PUT | Update patient | Updated patient object |
| `/patients/<id>` | DELETE | Delete patient | Success message |

### System Status

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/health` | GET | System health check | Health status |
| `/status` | GET | Application status | Status information |

## <span id="troubleshooting"></span>🔧 Troubleshooting

### Database Connection Issues

```bash
# Error: Connection refused

# Solution 1: Check ScyllaDB is running
docker ps | grep scylla

# Solution 2: Start ScyllaDB
docker run -d --name scylla scylladb/scylla

# Solution 3: Verify connection settings in .env
cat .env
```

### Input Validation Errors

```
Error: Date format invalid

# Solution: Use YYYY-MM-DD format
# Correct: 1990-05-15
# Wrong: 05-15-1990 or 1990/05/15
```

### Docker Issues

```bash
# Error: Port already in use
# Solution: Use different port
docker run -p 9043:9042 scylladb/scylla

# Error: Docker daemon not running
# Solution: Start Docker Desktop or Docker Engine
```

### Poetry Issues

```bash
# Error: Package not found
# Solution: Update poetry
poetry self update

# Solution: Reinstall dependencies
rm poetry.lock
poetry install
```

## <span id="contributing"></span>🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Workflow

1. **Create a feature branch**: `git checkout -b feature/add-doctor-management`
2. **Make your changes** and test thoroughly
3. **Commit with clear messages**: `git commit -m 'Add doctor management feature'`
4. **Push to your fork**: `git push origin feature/add-doctor-management`
5. **Open a Pull Request** with detailed description

### Code Standards

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Use meaningful variable names
- Add docstrings to functions

### Before Submitting PR

```bash
# Format code
poetry run black src/

# Run linter
poetry run flake8 src/

# Run tests
poetry run pytest

# Type checking
poetry run mypy src/
```

## <span id="license"></span>📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Hospital Management System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## <span id="support"></span>📞 Support

### Getting Help

- Check the [Troubleshooting](#troubleshooting) section above
- Review existing issues on GitHub
- Create a new GitHub issue with detailed information
- Contact the development team

### Common Issues and Solutions

#### ScyllaDB Won't Connect

```bash
# Check ScyllaDB is running
docker ps | grep scylla

# Check connection settings
grep SCYLLA .env

# Test connection
python -c "from src.database.connection import ScyllaDBConnection; ScyllaDBConnection().connect()"
```

#### Date Validation Error

```
Error: time data '05-15-1990' does not match format '%Y-%m-%d'

# Use correct format: YYYY-MM-DD
# Correct: 1990-05-15
```

#### Missing Dependencies

```bash
# Reinstall dependencies
poetry install

# Update dependencies
poetry update
```

---

**Made with ❤️ by the Hospital Management System Team**

*Empowering healthcare providers with scalable patient management.*
