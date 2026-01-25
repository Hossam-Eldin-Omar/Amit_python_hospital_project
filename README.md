# Hospital Management System

A Python-based hospital management system built with ScyllaDB (a Cassandra-compatible distributed database) for managing patient information and hospital operations.

## Overview

This project implements a scalable hospital management system that allows for:
- **Patient Management**: Create and manage patient records with personal information
- **Database Schema**: Organized data models for hospitals, departments, and patients
- **Distributed Storage**: Uses ScyllaDB for high-performance, distributed data storage
- **Logging**: Comprehensive logging for debugging and monitoring

## Project Structure

```
.
├── main.py                          # Main entry point for the application
├── pyproject.toml                   # Poetry configuration and dependencies
├── dockerfile                       # Docker configuration for containerization
├── README.md                        # This file
├── HowToRun                         # Quick start guide
├── logs/                            # Application logs
├── src/
│   ├── config/
│   │   └── settings.py             # Application settings and configuration
│   ├── database/
│   │   ├── connection.py           # ScyllaDB connection management
│   │   ├── init_db.py              # Database schema initialization
│   │   └── repositories/
│   │       └── patient_repository.py # Patient data access layer
│   ├── models/
│   │   ├── patient.py              # Patient model
│   │   └── person.py               # Base Person model
│   └── utils/
│       └── logger.py               # Logging configuration
└── __pycache__/                     # Python cache files
```

## Features

- **Patient Registration**: Add new patients with personal information (name, DOB, phone)
- **Auto-generated IDs**: Uses UUID for unique patient and department identification
- **Timestamp Tracking**: Automatically records creation timestamps
- **Input Validation**: Validates patient data format and required fields
- **Database Initialization**: Automatic schema creation on first run
- **Comprehensive Logging**: All operations are logged for monitoring and debugging

## Requirements

- Python 3.9+
- ScyllaDB 5.0+ (or Cassandra 4.0+)
- Poetry (for dependency management)

## Dependencies

- `cassandra-driver`: Python driver for Cassandra/ScyllaDB
- `python-dotenv`: Environment variable management
- `pytest`: Testing framework
- `black`: Code formatting
- `flake8`: Code linting
- `mypy`: Static type checking

## Installation

### Using Poetry (Recommended)

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Using pip

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the root directory with your database connection settings:

```env
SCYLLA_HOST=localhost
SCYLLA_PORT=9042
SCYLLA_KEYSPACE=hospital
```

## Usage

### Running the Application

#### Option 1: Local Execution

```bash
# Run the main application
python main.py
```

#### Option 2: Using Poetry Script

```bash
poetry run hospital
```

#### Option 3: Using Docker

```bash
# Build the Docker image
docker build -t hospital-python-poetry-app .

# Run the container (requires ScyllaDB container on scylla-net network)
docker run -it --rm --network scylla-net hospital-python-poetry-app python main.py
```

### Application Flow

1. **Connect to Database**: Establishes connection to ScyllaDB instance
2. **Initialize Schema**: Creates the keyspace and tables if they don't exist
3. **Add Patient**: Prompts user to enter new patient information:
   - First name
   - Last name
   - Date of birth (YYYY-MM-DD format)
   - Phone number
4. **Display Patients**: Shows all patients currently in the database

### Example Input

```
Enter new patient data
First name: John
Last name: Doe
Date of birth (YYYY-MM-DD): 1990-05-15
Phone: 555-123-4567
```

## Database Schema

### Keyspace
- `hospital`: Main keyspace with SimpleStrategy replication

### Tables
- **hospitals**: Hospital records
- **departments**: Department information
- **patients**: Patient details with partition key on `department_id` and clustering key on `patient_id`

Patient table fields:
- `patient_id` (UUID)
- `department_id` (UUID)
- `first_name` (text)
- `last_name` (text)
- `date_of_birth` (text)
- `age` (int)
- `phone` (text)
- `created_at` (timestamp)

## Development

### Running Tests

```bash
poetry run pytest
```

### Running Tests with Coverage

```bash
poetry run pytest --cov=src tests/
```

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

## Logging

Logs are stored in the `logs/` directory with the following levels:
- `DEBUG`: Detailed diagnostic information
- `INFO`: General informational messages
- `ERROR`: Error messages for failures

## Docker Setup

The project includes a `dockerfile` for containerization. To run with Docker:

1. Ensure ScyllaDB is running on a Docker network named `scylla-net`
2. Build the image: `docker build -t hospital-python-poetry-app .`
3. Run the container: `docker run -it --rm --network scylla-net hospital-python-poetry-app python main.py`

## Troubleshooting

### Database Connection Issues
- Verify ScyllaDB is running and accessible
- Check `SCYLLA_HOST` and `SCYLLA_PORT` settings in `.env`
- Ensure the keyspace and tables are created (run `initialize_database()`)

### Input Validation Errors
- Date of birth must be in `YYYY-MM-DD` format
- First name and last name cannot be empty
- Phone number should be valid format (validation rules apply)

## Future Enhancements

- [ ] Add doctor and appointment management
- [ ] Implement patient search and filtering
- [ ] Add medical record management
- [ ] Create REST API endpoints
- [ ] Implement user authentication
- [ ] Add data export functionality

## License

This project is part of the DEPI ML Track hospital management system training.

## Author

Amit - DEPI ML Track Student

## Support

For issues, questions, or contributions, please refer to the project documentation or contact the development team.