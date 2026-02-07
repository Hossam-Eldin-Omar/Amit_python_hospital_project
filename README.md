# Hospital Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Poetry](https://img.shields.io/badge/Poetry-1.8+-blue.svg)](https://python-poetry.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![ScyllaDB](https://img.shields.io/badge/ScyllaDB-5.0+-brightgreen.svg)](https://www.scylladb.com/)

**Hospital Management System** is a comprehensive Python-based healthcare management platform built with ScyllaDB for high-performance distributed data storage. It provides automated patient registration, data validation, hospital operations management, staff management, department organization, and a modern Streamlit web interface with professional logging and complete Docker containerization.

## <span id="table-of-contents"></span>📋 Table of Contents

- [Welcome](#welcome)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Docker Deployment](#docker-deployment)
- [Streamlit Web Application](#streamlit-web-application)
- [Navigation & Application Map](#navigation-application-map)
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
- **🏥 Hospital Management**: Complete hospital creation and management with location tracking
- **🏢 Department Management**: Organize departments within hospitals with hierarchical structure
- **👤 Patient Management**: Comprehensive patient registration, profiles, and medical records
- **👥 Staff Management**: Employee tracking with positions, departments, and credentials
- **🗄️ Distributed Database**: High-performance ScyllaDB backend with automatic schema initialization
- **📊 Data Validation**: Intelligent input validation and error handling
- **🔍 Advanced Search**: Multi-criteria search (ID, Name, Phone) with real-time results
- **📝 Auto-Generated IDs**: UUID-based identification for all entities

### **Advanced Capabilities** 
- **Multi-threaded Architecture**: High-performance concurrent processing
- **Professional Logging**: Comprehensive logging with DEBUG, INFO, and ERROR levels
- **Streamlit Web Interface**: Modern, professional web UI with 7 pages
- **Dashboard & Analytics**: Visual statistics, interactive charts, and real-time metrics
- **Patient Registration Form**: Intuitive form with validation and auto-calculation
- **Multiple Search Methods**: Search by ID, Name, Phone, or view all
- **Dockerized Environment**: Complete containerization with Docker Compose orchestration
- **Input Validation**: Date format validation, required field enforcement, email validation
- **Timestamp Tracking**: Automatic creation timestamp recording
- **Database Persistence**: ScyllaDB distributed NoSQL database integration
- **Responsive Design**: Mobile-friendly interface that works on all devices

### **UML Relationship Chain**
The system implements a complete hierarchical structure:
```
Hospital ──contains──> Department ──manages──> Patient
                                  └──employs──> Staff
```

## <span id="system-architecture"></span>🏗️ System Architecture

### Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│  ┌──────────────────┐         ┌───────────────────┐    │
│  │  Streamlit UI    │         │  CLI Application  │    │
│  │  (Port 8501)     │         │  (main.py)        │    │
│  └──────────────────┘         └───────────────────┘    │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                   Application Layer                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Business Logic & Repository Pattern              │  │
│  │  • HospitalRepository  • DepartmentRepository     │  │
│  │  • PatientRepository   • StaffRepository          │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                    Data Layer                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │  ScyllaDB (NoSQL Distributed Database)           │  │
│  │  • hospital keyspace                              │  │
│  │  • Replication Strategy: SimpleStrategy          │  │
│  │  • CQL Protocol (Port 9042)                       │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Deployment Architecture

```
┌──────────────────────────────────────────────────────────┐
│              Docker Network: new-scylla-net               │
│                                                            │
│  ┌─────────────────────┐      ┌──────────────────────┐  │
│  │  hospital-app       │      │  new-scylla-node     │  │
│  │  Container          │◄────►│  Container           │  │
│  │                     │      │                      │  │
│  │  • Streamlit App    │      │  • ScyllaDB 5.0+     │  │
│  │  • Python 3.12      │      │  • Data Persistence  │  │
│  │  • Poetry Deps      │      │  • Health Checks     │  │
│  │                     │      │                      │  │
│  │  Port: 8501        │      │  Ports: 9042, 9160   │  │
│  └─────────────────────┘      └──────────────────────┘  │
│           │                              │                │
└───────────┼──────────────────────────────┼───────────────┘
            │                              │
            ▼                              ▼
      localhost:8501              localhost:9042
      (Web Interface)             (CQL Protocol)
```

## <span id="prerequisites"></span>🔧 Prerequisites

Before setting up the Hospital Management System, ensure you have the following installed:

### Required Software

- **Python 3.10+**
  - Download from [python.org](https://www.python.org/downloads/)

- **Poetry** (for dependency management)
  - Install from [python-poetry.org](https://python-poetry.org/docs/#installation)
  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```

- **ScyllaDB 5.0+** (or Cassandra 4.0+)
  - Download from [scylladb.com](https://www.scylladb.com/download/)
  - Or use Docker (recommended)

- **Docker Desktop** (recommended for easy deployment)
  - Windows/macOS: [Docker Desktop](https://www.docker.com/products/docker-desktop)
  - Linux: [Docker Engine](https://docs.docker.com/engine/install/)

- **Docker Compose** (included with Docker Desktop)
  - For orchestrating multi-container deployments

- **Git** (Latest version)
  - Download from [git-scm.com](https://git-scm.com/downloads)

### System Requirements

- **RAM**: Minimum 4GB (8GB recommended for Docker deployment)
- **Storage**: At least 2GB free space
- **OS**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Network**: Internet connection for initial setup and dependency installation

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
# ScyllaDB Configuration
SCYLLA_HOST=localhost
SCYLLA_PORT=9042
SCYLLA_KEYSPACE=hospital

# Application Configuration
LOG_LEVEL=INFO
PYTHONUNBUFFERED=1

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### 3. Install Dependencies

Using Poetry (for local development):

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### 4. Start ScyllaDB

**Option A: Using Docker (Recommended)**

```bash
# Start ScyllaDB container
docker run -d --name scylla -p 9042:9042 scylladb/scylla

# Wait for ScyllaDB to be ready (takes 30-60 seconds)
docker exec -it scylla nodetool status
```

**Option B: Using Docker Compose (Easiest)**

```bash
# Start both ScyllaDB and application
docker-compose up -d

# Check status
docker-compose ps
```

**Option C: Local Installation**

```bash
# If ScyllaDB is installed locally
scylladb
```

## <span id="quick-start"></span>⚡ Quick Start

### Option 1: Docker Compose (Recommended)

The fastest way to get started:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f hospital-app

# Access the application
# Open browser to: http://localhost:8501

# Stop services
docker-compose down
```

### Option 2: Local Development

```bash
# Ensure ScyllaDB is running
docker run -d --name scylla -p 9042:9042 scylladb/scylla

# Install dependencies
poetry install

# Run the CLI application
poetry run python main.py

# Or run the Streamlit web app
poetry run streamlit run streamlit_app/app.py
```

### Option 3: CLI Application Only

```bash
# Run the command-line interface
python main.py
```

### Example CLI Usage

```
Enter new patient data
Hospital name: City General Hospital
Location: New York, NY
Phone (optional): +1-555-100-2000

Available hospitals:
  [0] City General Hospital – New York, NY (ID: 550e8400-...)

Select hospital index: 0
Department name: Emergency
Description (optional): 24/7 Emergency Services

✓ Department created: 660e9500-...

First name: John
Last name: Doe
Date of birth (YYYY-MM-DD): 1990-05-15
Phone: +1-555-123-4567

✓ Patient created: 770e1600-...
```

## <span id="docker-deployment"></span>🐳 Docker Deployment

### Complete Docker Setup Guide

#### Docker Architecture Overview

The application uses a multi-container Docker setup with:
- **ScyllaDB Container**: Database backend
- **Application Container**: Streamlit web interface
- **Custom Network**: `new-scylla-net` for container communication
- **Persistent Volumes**: Data persistence for ScyllaDB

### Deployment Methods

#### Method 1: Docker Compose (Production Ready)

**Step 1: Review docker-compose.yml**

```yaml
version: '3.8'

services:
  # ScyllaDB Service - NoSQL Database
  new-scylla-node:
    image: scylladb/scylla:latest
    container_name: new-scylla-node
    ports:
      - "9042:9042"  # CQL Port
      - "9160:9160"  # Thrift Port
      - "10000:10000"  # Admin Port
    volumes:
      - scylla_data:/var/lib/scylla
    environment:
      - SCYLLA_SEEDS=new-scylla-node
    networks:
      - new-scylla-net
    healthcheck:
      test: ["CMD", "cqlsh", "-e", "select * from system.peers"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Streamlit Web Application
  hospital-app:
    build:
      context: .
      dockerfile: dockerfile
    container_name: hospital-app
    ports:
      - "8501:8501"  # Streamlit Port
    environment:
      - SCYLLA_HOST=new-scylla-node
      - SCYLLA_PORT=9042
      - PYTHONUNBUFFERED=1
    depends_on:
      new-scylla-node:
        condition: service_healthy
    networks:
      - new-scylla-net
    restart: unless-stopped
    volumes:
      - .:/app

networks:
  new-scylla-net:
    driver: bridge

volumes:
  scylla_data:
    driver: local
```

**Step 2: Deploy**

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service health
docker-compose ps

# Access the application
# Open browser to: http://localhost:8501
```

**Step 3: Manage**

```bash
# Stop services (keeps data)
docker-compose stop

# Start services
docker-compose start

# Restart services
docker-compose restart

# Stop and remove containers (keeps volumes)
docker-compose down

# Remove everything including volumes
docker-compose down -v

# View real-time logs
docker-compose logs -f hospital-app

# Execute commands in container
docker-compose exec hospital-app python main.py
```

#### Method 2: Manual Docker Build

**Step 1: Build the Docker Image**

```bash
# Build the application image
docker build -t hospital-management-app .

# Build without cache (for clean build)
docker build -t hospital-management-app . --no-cache

# Verify image
docker images | grep hospital-management-app
```

**Step 2: Create Docker Network**

```bash
# Create custom network
docker network create new-scylla-net

# Verify network
docker network ls | grep scylla
```

**Step 3: Start ScyllaDB**

```bash
# Start ScyllaDB on custom network
docker run -d \
  --name new-scylla-node \
  --network new-scylla-net \
  -p 9042:9042 \
  -p 9160:9160 \
  -p 10000:10000 \
  -v scylla_data:/var/lib/scylla \
  scylladb/scylla:latest

# Wait for ScyllaDB to be ready (30-60 seconds)
docker exec -it new-scylla-node nodetool status

# Check logs
docker logs new-scylla-node
```

**Step 4: Start Application**

```bash
# Run Streamlit app
docker run -d \
  --name hospital-app \
  --network new-scylla-net \
  -p 8501:8501 \
  -e SCYLLA_HOST=new-scylla-node \
  -e SCYLLA_PORT=9042 \
  -e PYTHONUNBUFFERED=1 \
  -v $(pwd):/app \
  hospital-management-app

# Check logs
docker logs -f hospital-app

# Access: http://localhost:8501
```

**Step 5: Run CLI Application (Optional)**

```bash
# Run the CLI interface
docker run -it --rm \
  --network new-scylla-net \
  -e SCYLLA_HOST=new-scylla-node \
  -e SCYLLA_PORT=9042 \
  hospital-management-app \
  python main.py
```

### Dockerfile Explanation

```dockerfile
# Base image with Python 3.12
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

# Configure Poetry to not create virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
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

# Create streamlit credentials and config
RUN echo '[general]' > /app/.streamlit/credentials.toml && \
    echo 'email = ""' >> /app/.streamlit/credentials.toml

# Run Streamlit app by default
CMD ["streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
```

### Docker Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SCYLLA_HOST` | ScyllaDB hostname | `new-scylla-node` | Yes |
| `SCYLLA_PORT` | ScyllaDB CQL port | `9042` | Yes |
| `SCYLLA_KEYSPACE` | Database keyspace | `hospital` | No |
| `PYTHONUNBUFFERED` | Python output buffering | `1` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |

### Docker Volume Management

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect scylla_data

# Backup volume
docker run --rm -v scylla_data:/data -v $(pwd):/backup ubuntu tar czf /backup/scylla_backup.tar.gz /data

# Restore volume
docker run --rm -v scylla_data:/data -v $(pwd):/backup ubuntu tar xzf /backup/scylla_backup.tar.gz -C /

# Remove volume (WARNING: Deletes all data)
docker volume rm scylla_data
```

### Docker Health Checks

```bash
# Check ScyllaDB health
docker exec -it new-scylla-node nodetool status

# Check application health
docker exec -it hospital-app curl -f http://localhost:8501 || echo "App not ready"

# Monitor container resources
docker stats hospital-app new-scylla-node

# View container details
docker inspect hospital-app
docker inspect new-scylla-node
```

## <span id="streamlit-web-application"></span>🌐 Streamlit Web Application

The Hospital Management System includes a modern, professional **Streamlit-based web interface** for comprehensive hospital management.

### Running the Streamlit App

**Method 1: Docker Compose (Recommended)**

```bash
# Start all services
docker-compose up -d

# Access at: http://localhost:8501
```

**Method 2: Local with Poetry**

```bash
# Install dependencies
poetry install

# Run Streamlit app
poetry run streamlit run streamlit_app/app.py

# Access at: http://localhost:8501
```

**Method 3: Docker (Manual)**

```bash
# Build Docker image
docker build -t hospital-app .

# Run container
docker run -p 8501:8501 \
  -e SCYLLA_HOST=new-scylla-node \
  -e SCYLLA_PORT=9042 \
  --network new-scylla-net \
  hospital-app

# Access at: http://localhost:8501
```

**Method 4: Python Directly**

```bash
# Activate virtual environment
poetry shell

# Run Streamlit
streamlit run streamlit_app/app.py

# Or without Poetry
python -m streamlit run streamlit_app/app.py
```

### Streamlit Configuration

Create `.streamlit/config.toml` for customization:

```toml
[server]
port = 8501
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
serverAddress = "localhost"

[theme]
primaryColor = "#667eea"
backgroundColor = "#f5f7fa"
secondaryBackgroundColor = "#e3f2fd"
textColor = "#2c3e50"
font = "sans serif"
```

### Web Application Features

The Streamlit interface provides **7 comprehensive pages**:

#### 📊 Dashboard
**Purpose**: Hospital system overview and analytics

**Features**:
- Real-time system statistics
- Total patients, departments, hospitals, and staff count
- 30-day patient registration trends (interactive line chart)
- Patient distribution by department (interactive pie chart)
- Recent patient registrations table
- Key performance metrics
- System health indicators

**Charts & Visualizations**:
- Line chart: Patient registrations over last 30 days
- Pie chart: Patient distribution across departments
- Metric cards: Total patients, active today, departments, system health

#### 🏥 Manage Hospitals
**Purpose**: Hospital creation and management

**Features**:
- Add new hospitals with name, location, and contact information
- View all hospitals in the system
- Edit hospital information
- Delete hospitals (with confirmation)
- Search and filter hospitals
- Hospital details display
- Department count per hospital

**Form Fields**:
- Hospital Name (required)
- Location (required)
- Phone Number (optional)
- Email (optional)

#### 🏢 Manage Departments
**Purpose**: Department organization and hierarchy

**Features**:
- Create departments linked to hospitals
- View all departments with hospital association
- Edit department details
- Delete departments (with validation)
- Department description management
- Staff count per department
- Patient count per department

**Form Fields**:
- Department Name (required)
- Hospital Selection (dropdown, required)
- Description (optional)

#### 👤 Add Patient
**Purpose**: Patient registration and enrollment

**Features**:
- Comprehensive patient registration form
- Personal information collection
- Contact information management
- Medical information tracking
- Automatic age calculation from date of birth
- Real-time form validation with feedback
- Success confirmation with patient summary
- Department assignment

**Form Sections**:

**Personal Information**:
- First Name (required, 2-50 characters)
- Last Name (required, 2-50 characters)
- Date of Birth (required, YYYY-MM-DD format)
- Calculated Age (auto-computed)
- Gender (optional dropdown: Male/Female/Other/Not Specified)

**Contact Information**:
- Phone Number (required, must contain digits)
- Email Address (optional, validated format)

**Medical Information**:
- Blood Type (optional dropdown: A+, A-, B+, B-, AB+, AB-, O+, O-)
- Department Assignment (required, dropdown)
- Medical Record Number (auto-generated)

**Validation Rules**:
- Name: Min 2 chars, max 50 chars, no special characters
- Date of Birth: Must be valid date, not in future
- Phone: Must contain digits, international format supported
- Email: Valid email format (if provided)

#### 🔍 Search Patients
**Purpose**: Patient lookup and information retrieval

**Features**:
- **Multiple Search Options**:
  - **Patient ID Search**: Find by unique patient identifier
  - **Name Search**: Search by first name, last name, or both
  - **Phone Search**: Find by phone number
  - **View All**: Display all patients in the system

- **Two Result Display Modes**:
  - **Table View**: Organized columns with sortable data
    - Columns: Patient ID, First Name, Last Name, Age, Phone, DOB, Department
    - Sortable and filterable
    - Pagination support
  
  - **Detailed Card View**: Expandable cards with complete information
    - Personal information section
    - Contact information section
    - Medical information section
    - System metadata
    - Action buttons (Edit, View, Delete)

**Search Features**:
- Real-time search results
- Case-insensitive matching
- Partial name matching
- Results counter
- No results message with suggestions
- Search tips and help

#### 👥 Manage Staff
**Purpose**: Hospital staff and employee management

**Features**:
- Add new staff members
- Assign staff to departments
- View all staff with department information
- Edit staff details
- Remove staff members
- Position tracking
- Staff credentials management

**Form Fields**:
- First Name (required)
- Last Name (required)
- Age (required, numeric)
- Position (required: Doctor, Nurse, Administrator, Technician, etc.)
- Department Assignment (required, dropdown)
- Employee ID (auto-generated)

#### ⚙️ Settings
**Purpose**: System configuration and administration

**Features**:

**System Information**:
- Application version and build info
- Python version
- Database status
- License information
- Last backup date
- Support contact information

**Display Settings**:
- Theme selection (Light/Dark)
- Rows per page configuration
- Date format preferences
- Time zone settings

**Database Settings**:
- ScyllaDB host (read-only display)
- Port configuration (read-only display)
- Keyspace information (read-only display)
- Consistency level selection
- Connection test button
- Database statistics

**Logging Settings**:
- Log level selection (DEBUG, INFO, WARNING, ERROR)
- Enable/disable file logging
- View logs button
- Clear logs option
- Log rotation settings

**User Management**:
- Username display (read-only)
- Role display (read-only)
- Change password button
- Session information

**Backup & Maintenance**:
- Database backup button
- Database optimization
- Cache clearing
- Data export options

### Web Interface Design Principles

**Visual Design**:
- **Professional UI**: Clean, modern interface with gradient sidebar
- **Color Scheme**: Blue (#1f77b4) primary color with professional accents
- **Typography**: Clear, readable fonts with proper hierarchy
- **Spacing**: Generous white space for clarity

**Interactive Components**:
- Charts and graphs with Plotly for interactivity
- Real-time data updates
- Loading indicators and spinners
- Success/error notifications
- Toast messages for feedback

**Responsive Design**:
- Desktop-optimized layout (1024px+)
- Tablet-friendly (768px-1023px)
- Mobile-accessible (< 768px)
- Touch-friendly buttons and inputs
- Collapsible sidebar on small screens

**Form Validation**:
- Real-time field validation
- Helpful error messages
- Required field indicators (*)
- Input format hints
- Success confirmations

**User Experience**:
- Intuitive navigation
- Clear page titles and descriptions
- Breadcrumb navigation
- Quick action buttons
- Keyboard shortcuts support
- Accessibility features

## <span id="navigation-application-map"></span>🗺️ Navigation & Application Map

### Complete Application Navigation Structure

```
┌──────────────────────────────────────────────────────────────────┐
│                   Hospital Management System 🏥                   │
│                              v2.0                                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  SIDEBAR NAVIGATION              MAIN CONTENT AREA               │
│  ═══════════════════              ══════════════════              │
│                                                                    │
│  🏥 Hospital System                                               │
│  ───────────────────                                              │
│                                   ┌──────────────────────────┐   │
│  📊 Dashboard ──────────────────► │  Dashboard Page          │   │
│                                   │  • Statistics Overview   │   │
│  🏥 Hospitals                     │  • Charts & Graphs       │   │
│  ─────────────                    │  • Recent Activity       │   │
│  Manage Hospitals ──────────────► │  • Key Metrics          │   │
│                                   └──────────────────────────┘   │
│  🏢 Departments                                                   │
│  ───────────────                  ┌──────────────────────────┐   │
│  Manage Departments ────────────► │  Department Management   │   │
│                                   │  • Create Departments    │   │
│  🧑‍⚕️ Patients                     │  • View & Edit          │   │
│  ──────────                       │  • Assign to Hospitals   │   │
│  Add Patient ───────────────────► └──────────────────────────┘   │
│  Search Patients ───────────────►                                │
│                                   ┌──────────────────────────┐   │
│  👥 Staff                         │  Patient Management      │   │
│  ────────                         │  • Registration Form     │   │
│  Manage Staff ──────────────────► │  • Search & Filter      │   │
│                                   │  • Medical Records       │   │
│  ⚙️ System                        └──────────────────────────┘   │
│  ─────────                                                        │
│  Settings ──────────────────────► ┌──────────────────────────┐   │
│                                   │  System Settings         │   │
│  ─────────────────────────────── │  • Configuration         │   │
│                                   │  • User Management       │   │
│  Hospital Management System v2.0  │  • Database Settings     │   │
│  Streamlit + ScyllaDB             └──────────────────────────┘   │
│                                                                    │
└──────────────────────────────────────────────────────────────────┘
```

### Detailed Page Flow Diagram

```
                    ┌─────────────────┐
                    │   Dashboard     │
                    │   (Landing)     │
                    └────────┬────────┘
                             │
             ┌───────────────┼───────────────┐
             │               │               │
             ▼               ▼               ▼
    ┌─────────────┐  ┌─────────────┐  ┌──────────────┐
    │  Hospitals  │  │ Departments │  │   Patients   │
    │ Management  │  │ Management  │  │  Management  │
    └──────┬──────┘  └──────┬──────┘  └──────┬───────┘
           │                │                │
           │                │                │
           ▼                ▼                ▼
    ┌──────────────────────────────────────────────┐
    │         Create → View → Edit → Delete        │
    └──────────────────┬───────────────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Staff          │
              │  Management     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   Settings      │
              │   & Config      │
              └─────────────────┘
```

### User Journey Map

#### Journey 1: New Patient Registration
```
1. Dashboard (Overview)
   ↓
2. Navigate to "Add Patient"
   ↓
3. Fill Patient Form
   • Personal Info
   • Contact Info
   • Medical Info
   ↓
4. Submit Registration
   ↓
5. View Confirmation
   ↓
6. Search Patients (Verify)
```

#### Journey 2: Hospital Setup
```
1. Dashboard
   ↓
2. Manage Hospitals
   ↓
3. Create Hospital
   • Name & Location
   • Contact Info
   ↓
4. Manage Departments
   ↓
5. Create Department
   • Link to Hospital
   • Add Description
   ↓
6. Dashboard (Verify Setup)
```

#### Journey 3: Staff Management
```
1. Manage Staff
   ↓
2. View Current Staff
   ↓
3. Add New Staff Member
   • Personal Info
   • Position
   • Department Assignment
   ↓
4. Verify in Department View
```

### Navigation Controls

**Sidebar Navigation**:
- Single-click navigation
- Active page highlighting
- Grouped by category
- Icons for visual clarity

**Page Navigation**:
- Breadcrumb navigation (future feature)
- Back buttons where applicable
- Quick action buttons
- Search functionality

**Keyboard Shortcuts** (Streamlit Default):
- `Ctrl/Cmd + Enter`: Submit form
- `Escape`: Close modals
- `Tab`: Navigate fields
- `Enter`: Activate buttons

### Application Flow Chart

```
┌──────────────┐
│ Application  │
│   Start      │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Check Database   │
│  Connection      │
└──────┬───────────┘
       │
       ├─── Connected ────► ┌──────────────────┐
       │                    │ Initialize       │
       │                    │ Schema           │
       │                    └────────┬─────────┘
       │                             │
       │                             ▼
       │                    ┌──────────────────┐
       │                    │ Load Dashboard   │
       │                    └────────┬─────────┘
       │                             │
       │                             ▼
       │                    ┌──────────────────┐
       │                    │ User Interaction │
       │                    └────────┬─────────┘
       │                             │
       │                    ┌────────┴─────────┐
       │                    │                  │
       │                    ▼                  ▼
       │           ┌──────────────┐   ┌──────────────┐
       │           │  CRUD Ops    │   │  Analytics   │
       │           └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       │                  └────────┬─────────┘
       │                           │
       │                           ▼
       │                  ┌──────────────────┐
       │                  │ Update Database  │
       │                  └──────────────────┘
       │
       └─── Not Connected ──► ┌──────────────────┐
                              │ Show Error       │
                              │ Connection Tips  │
                              └──────────────────┘
```

## <span id="configuration"></span>⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SCYLLA_HOST` | ScyllaDB host address | `localhost` | No |
| `SCYLLA_PORT` | ScyllaDB CQL port | `9042` | No |
| `SCYLLA_KEYSPACE` | Database keyspace name | `hospital` | No |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, ERROR) | `INFO` | No |
| `PYTHONUNBUFFERED` | Python output buffering | `1` | No |
| `STREAMLIT_SERVER_PORT` | Streamlit server port | `8501` | No |
| `STREAMLIT_SERVER_ADDRESS` | Streamlit server address | `0.0.0.0` | No |

### Database Configuration

**ScyllaDB Configuration in `.env`**:

```env
SCYLLA_HOST=localhost
SCYLLA_PORT=9042
SCYLLA_KEYSPACE=hospital
```

**For Multi-Node ScyllaDB Clusters**:

```env
SCYLLA_HOST=node1,node2,node3
SCYLLA_PORT=9042
SCYLLA_KEYSPACE=hospital
```

**Connection Settings** (`src/config/settings.py`):

```python
from dataclasses import dataclass
import os
from dotenv import load_env

load_dotenv()

@dataclass
class Settings:
    scylla_host: str = os.getenv("SCYLLA_HOST", "localhost")
    scylla_port: int = int(os.getenv("SCYLLA_PORT", "9042"))
    scylla_keyspace: str = os.getenv("SCYLLA_KEYSPACE", "hospital")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
```

### Logging Configuration

**Log Levels**:
- `DEBUG`: Detailed information for diagnosing problems
- `INFO`: General information about program execution
- `WARNING`: Warning messages for potentially harmful situations
- `ERROR`: Error messages for serious problems
---

### Streamlit Configuration

**Create `.streamlit/config.toml`**:

```toml
[server]
port = 8501
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200

[browser]
gatherUsageStats = false
serverAddress = "localhost"
serverPort = 8501

[theme]
primaryColor = "#667eea"
backgroundColor = "#f5f7fa"
secondaryBackgroundColor = "#e3f2fd"
textColor = "#2c3e50"
font = "sans serif"

[runner]
magicEnabled = true
fastReruns = true

[client]
showErrorDetails = true
toolbarMode = "minimal"
```

**Create `.streamlit/credentials.toml`**:

```toml
[general]
email = ""
```

## <span id="usage"></span>📖 Usage

### Command Line Interface (CLI)

The CLI application provides a menu-driven interface for hospital management:

```bash
# Run the CLI
python main.py
```

**CLI Menu Options**:

```
--- Menu ---
1. Add Hospital
2. Add Department
3. Add Patient
4. Add Staff
5. View all (tree)
6. Exit
```

**Example CLI Session**:

```bash
$ python main.py

============================================================
Hospital Management System
============================================================

--- Menu ---
1. Add Hospital
2. Add Department
3. Add Patient
4. Add Staff
5. View all (tree)
6. Exit

Choice (1-6): 1

Hospital name: City General Hospital
Location: New York, NY
Phone (optional): +1-555-100-2000

✓ Hospital created: 550e8400-e29b-41d4-a716-446655440000

--- Menu ---
1. Add Hospital
2. Add Department
3. Add Patient
4. Add Staff
5. View all (tree)
6. Exit

Choice (1-6): 5

🏥  City General Hospital | New York, NY | +1-555-100-2000
    Hospital ID: 550e8400-e29b-41d4-a716-446655440000
    └─ (no departments)
```

### Web Interface Usage

#### Using the Dashboard

1. **Access the Dashboard**:
   - Navigate to `http://localhost:8501`
   - Dashboard loads automatically

2. **View System Statistics**:
   - Total patients count
   - Active departments
   - Recent registrations
   - System health status

3. **Analyze Trends**:
   - 30-day patient registration trend
   - Department distribution
   - Key performance metrics

#### Adding a Hospital

1. **Navigate**: Sidebar → "Manage Hospitals"
2. **Click**: "Add New Hospital" button
3. **Fill Form**:
   - Hospital Name (required)
   - Location (required)
   - Phone Number (optional)
4. **Submit**: Click "Create Hospital"
5. **Verify**: Check confirmation message

#### Registering a Patient

1. **Navigate**: Sidebar → "Add Patient"
2. **Fill Personal Information**:
   - First Name
   - Last Name
   - Date of Birth (YYYY-MM-DD)
   - Gender (optional)

3. **Fill Contact Information**:
   - Phone Number
   - Email (optional)

4. **Fill Medical Information**:
   - Blood Type (optional)
   - Select Department

5. **Submit**: Click "Register Patient"
6. **Review**: Check patient summary

#### Searching for Patients

1. **Navigate**: Sidebar → "Search Patients"
2. **Select Search Method**:
   - Patient ID
   - Name
   - Phone
   - View All

3. **Enter Search Criteria**
4. **Choose View Mode**:
   - Table View (compact)
   - Detailed View (full information)

5. **Interact with Results**:
   - Click to expand details
   - Use action buttons

### Python API Usage

```python
from src.database.connection import ScyllaDBConnection
from src.database.repositories.patient_repository import PatientRepository
from src.database.repositories.hospital_repository import HospitalRepository
from uuid import uuid4

# Initialize connection
db = ScyllaDBConnection()
session = db.connect()

# Create repositories
hospital_repo = HospitalRepository(session)
patient_repo = PatientRepository(session)

# Create a hospital
hospital_id = hospital_repo.create(
    name="City General",
    location="New York, NY",
    phone="+1-555-100-2000"
)

# Create a patient
patient_id = patient_repo.create(
    first_name="John",
    last_name="Doe",
    date_of_birth="1990-05-15",
    age=34,
    phone="+1-555-123-4567",
    department_id=department_id,
    medical_record="Initial checkup"
)

# Search patients
patient = patient_repo.get_by_id(patient_id)
all_patients = patient_repo.get_all()

# Close connection
db.close()
```

## <span id="project-structure"></span>📁 Project Structure

### Complete Directory Tree

```
hospital-management/
│
├── 📄 README.md                          # This file
├── 📄 .gitignore                         # Git ignore rules
├── 📄 pyproject.toml                     # Poetry dependencies
├── 📄 poetry.lock                        # Locked dependencies
├── 🐳 dockerfile                         # Docker image definition
├── 🐳 docker-compose.yml                 # Multi-container orchestration
│
├── 📂 src/                               # Source code
│   ├── 📂 config/                        # Configuration
│   │   ├── __init__.py
│   │   └── settings.py                   # App settings
│   │
│   ├── 📂 database/                      # Database layer
│   │   ├── __init__.py
│   │   ├── connection.py                 # ScyllaDB connection
│   │   ├── init_db.py                    # Schema initialization
│   │   └── 📂 repositories/              # Data access layer
│   │       ├── __init__.py
│   │       ├── hospital_repository.py    # Hospital CRUD
│   │       ├── department_repository.py  # Department CRUD
│   │       ├── patient_repository.py     # Patient CRUD
│   │       └── staff_repository.py       # Staff CRUD
│   │
│   ├── 📂 models/                        # Data models
│   │   ├── __init__.py
│   │   ├── person.py                     # Base Person class
│   │   ├── patient.py                    # Patient model
│   │   ├── staff.py                      # Staff model
│   │   ├── department.py                 # Department model
│   │   └── hospital.py                   # Hospital model
│   │
│   └── 📂 utils/                         # Utilities
│       ├── __init__.py
│       └── logger.py                     # Logging setup
│
├── 📂 streamlit_app/                     # Streamlit web interface
│   ├── app.py                            # Main Streamlit app
│   ├── config.py                         # Streamlit configuration
│   ├── utils.py                          # UI utilities
│   └── 📂 pages/                         # Page components
│       ├── __init__.py
│       ├── dashboard.py                  # Dashboard page
│       ├── manage_hospitals.py           # Hospital management
│       ├── manage_departments.py         # Department management
│       ├── add_patient.py                # Patient registration
│       ├── search_patient.py             # Patient search
│       ├── manage_staff.py               # Staff management
│       └── settings.py                   # Settings page
│
├── 📂 .streamlit/                        # Streamlit config
│   ├── config.toml                       # Streamlit settings
│   └── credentials.toml                  # Streamlit credentials
│
└── 📄 main.py                            # CLI entry point
```

### Module Descriptions

#### Source Code (`src/`)

**config/**:
- `settings.py`: Application configuration, environment variables

**database/**:
- `connection.py`: ScyllaDB connection management
- `init_db.py`: Database schema initialization
- `repositories/`: Data access layer with CRUD operations
  - `hospital_repository.py`: Hospital operations
  - `department_repository.py`: Department operations
  - `patient_repository.py`: Patient operations
  - `staff_repository.py`: Staff operations

**models/**:
- `person.py`: Base Person class (inheritance)
- `patient.py`: Patient data model
- `staff.py`: Staff data model
- `department.py`: Department data model
- `hospital.py`: Hospital data model

**utils/**:
- `logger.py`: Logging configuration and setup

#### Streamlit App (`streamlit_app/`)

**Main Files**:
- `app.py`: Main Streamlit application with routing
- `config.py`: Streamlit-specific configuration
- `utils.py`: UI utility functions and helpers

**Pages**:
- `dashboard.py`: Main dashboard with analytics
- `manage_hospitals.py`: Hospital CRUD interface
- `manage_departments.py`: Department CRUD interface
- `add_patient.py`: Patient registration form
- `search_patient.py`: Patient search and display
- `manage_staff.py`: Staff management interface
- `settings.py`: Application settings page

### File Naming Conventions

- **Python Files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions**: `snake_case()`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`

## <span id="database-schema"></span>🗄️ Database Schema

### ScyllaDB Keyspace and Tables

**Keyspace**: `hospital`

**Replication Strategy**: `SimpleStrategy` with replication factor 1

### Table Schemas

#### 1. hospitals

```cql
CREATE TABLE IF NOT EXISTS hospitals (
    hospital_id uuid PRIMARY KEY,
    name text,
    location text,
    phone text,
    created_at timestamp
);
```

**Fields**:
- `hospital_id`: UUID, Primary Key
- `name`: Hospital name
- `location`: Hospital location
- `phone`: Contact phone number
- `created_at`: Creation timestamp

**Indexes**:
```cql
CREATE INDEX IF NOT EXISTS ON hospitals (name);
```

#### 2. departments

```cql
CREATE TABLE IF NOT EXISTS departments (
    department_id uuid PRIMARY KEY,
    name text,
    hospital_id uuid,
    description text,
    created_at timestamp
);
```

**Fields**:
- `department_id`: UUID, Primary Key
- `name`: Department name
- `hospital_id`: Foreign key to hospitals
- `description`: Department description
- `created_at`: Creation timestamp

**Indexes**:
```cql
CREATE INDEX IF NOT EXISTS ON departments (hospital_id);
CREATE INDEX IF NOT EXISTS ON departments (name);
```

#### 3. patients

```cql
CREATE TABLE IF NOT EXISTS patients (
    patient_id uuid PRIMARY KEY,
    first_name text,
    last_name text,
    date_of_birth text,
    age int,
    phone text,
    email text,
    gender text,
    blood_type text,
    department_id uuid,
    medical_record text,
    created_at timestamp
);
```

**Fields**:
- `patient_id`: UUID, Primary Key
- `first_name`: Patient's first name
- `last_name`: Patient's last name
- `date_of_birth`: DOB in YYYY-MM-DD format
- `age`: Patient age in years
- `phone`: Contact phone number
- `email`: Email address (optional)
- `gender`: Gender (Male/Female/Other)
- `blood_type`: Blood type (A+, A-, B+, B-, AB+, AB-, O+, O-)
- `department_id`: Foreign key to departments
- `medical_record`: Medical record notes
- `created_at`: Registration timestamp

**Indexes**:
```cql
CREATE INDEX IF NOT EXISTS ON patients (department_id);
CREATE INDEX IF NOT EXISTS ON patients (first_name);
CREATE INDEX IF NOT EXISTS ON patients (last_name);
CREATE INDEX IF NOT EXISTS ON patients (phone);
```

#### 4. staff

```cql
CREATE TABLE IF NOT EXISTS staff (
    staff_id uuid PRIMARY KEY,
    first_name text,
    last_name text,
    age int,
    position text,
    department_id uuid,
    created_at timestamp
);
```

**Fields**:
- `staff_id`: UUID, Primary Key
- `first_name`: Staff's first name
- `last_name`: Staff's last name
- `age`: Staff age
- `position`: Job position (Doctor, Nurse, etc.)
- `department_id`: Foreign key to departments
- `created_at`: Hire/creation timestamp

**Indexes**:
```cql
CREATE INDEX IF NOT EXISTS ON staff (department_id);
CREATE INDEX IF NOT EXISTS ON staff (position);
```

### Entity Relationship Diagram

```
┌─────────────────┐
│    Hospital     │
│─────────────────│
│ hospital_id PK  │───┐
│ name            │   │
│ location        │   │
│ phone           │   │
│ created_at      │   │
└─────────────────┘   │
                      │ 1:N
                      │
                      ▼
              ┌─────────────────┐
              │   Department    │
              │─────────────────│
              │ department_id PK│───┐
              │ name            │   │
              │ hospital_id  FK │   │
              │ description     │   │
              │ created_at      │   │
              └─────────────────┘   │
                                    │ 1:N
                 ┌──────────────────┴──────────────────┐
                 │                                      │
                 ▼                                      ▼
         ┌─────────────────┐                  ┌─────────────────┐
         │     Patient     │                  │      Staff      │
         │─────────────────│                  │─────────────────│
         │ patient_id   PK │                  │ staff_id     PK │
         │ first_name      │                  │ first_name      │
         │ last_name       │                  │ last_name       │
         │ date_of_birth   │                  │ age             │
         │ age             │                  │ position        │
         │ phone           │                  │ department_id FK│
         │ email           │                  │ created_at      │
         │ gender          │                  └─────────────────┘
         │ blood_type      │
         │ department_id FK│
         │ medical_record  │
         │ created_at      │
         └─────────────────┘
```

### Database Initialization

The database schema is automatically initialized when the application starts:

```python
from src.database.init_db import initialize_database

# Initialize schema
initialize_database(session)
```

This creates:
1. Keyspace `hospital` (if not exists)
2. All tables with proper schema
3. All indexes for efficient querying

## <span id="development"></span>💻 Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/your-username/hospital-management.git
cd hospital-management

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Start ScyllaDB
docker run -d --name scylla -p 9042:9042 scylladb/scylla

# Run application
python main.py

# Or run Streamlit
streamlit run streamlit_app/app.py
```

### Development Workflow

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**:
   - Edit code
   - Add tests
   - Update documentation

3. **Run Tests**:
   ```bash
   poetry run pytest
   ```

4. **Format Code**:
   ```bash
   poetry run black src/
   ```

5. **Lint Code**:
   ```bash
   poetry run flake8 src/
   ```

6. **Type Check**:
   ```bash
   poetry run mypy src/
   ```

7. **Commit Changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

8. **Push and Create PR**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Code Formatting

```bash
# Format all Python files
poetry run black src/ streamlit_app/ tests/

# Check formatting without changes
poetry run black --check src/

# Format specific file
poetry run black src/models/patient.py
```

### Linting

```bash
# Run flake8 linter
poetry run flake8 src/

# With specific max line length
poetry run flake8 --max-line-length=88 src/

# Ignore specific errors
poetry run flake8 --ignore=E501,W503 src/
```

### Type Checking

```bash
# Run mypy type checker
poetry run mypy src/

# Check specific module
poetry run mypy src/models/

# Strict mode
poetry run mypy --strict src/
```

### Code Style Guide

- **Follow PEP 8**: Python Enhancement Proposal 8 style guidelines
- **Line Length**: Maximum 88 characters (Black default)
- **Imports**: Group by stdlib, third-party, local
- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Add type hints to function signatures
- **Comments**: Explain why, not what
- **Naming**:
  - Functions: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`
  - Private: `_leading_underscore`

**Example**:

```python
from typing import Optional
from uuid import UUID


def create_patient(
    first_name: str,
    last_name: str,
    date_of_birth: str,
    age: int,
    phone: str,
    department_id: UUID,
    medical_record: Optional[str] = None,
) -> UUID:
    """Create a new patient in the system.
    
    Args:
        first_name: Patient's first name
        last_name: Patient's last name
        date_of_birth: DOB in YYYY-MM-DD format
        age: Patient age in years
        phone: Contact phone number
        department_id: Department UUID
        medical_record: Optional medical notes
        
    Returns:
        UUID of the created patient
        
    Raises:
        ValueError: If required fields are missing
    """
    # Implementation
    pass
```

### Adding New Features

1. **Models** (`src/models/`):
   - Create data class
   - Add validation
   - Include docstrings

2. **Repository** (`src/database/repositories/`):
   - Implement CRUD operations
   - Add query methods
   - Handle errors

3. **Streamlit Page** (`streamlit_app/pages/`):
   - Create new page file
   - Add to navigation in `app.py`
   - Implement UI components

4. **Tests** (`tests/`):
   - Write unit tests
   - Test edge cases
   - Aim for >80% coverage

## <span id="testing"></span>🧪 Testing

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_patient_registration.py

# Run with verbose output
poetry run pytest -v

# Run with coverage
poetry run pytest --cov=src

# Run with coverage report
poetry run pytest --cov=src --cov-report=html

# Run specific test function
poetry run pytest tests/test_patient_registration.py::test_create_patient

# Run tests matching pattern
poetry run pytest -k "patient"
```

### Test Coverage

```bash
# Generate coverage report
poetry run pytest --cov=src --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser

# Coverage report in terminal
poetry run pytest --cov=src --cov-report=term

# Coverage with missing lines
poetry run pytest --cov=src --cov-report=term-missing
```

### Writing Tests

**Example Test** (`tests/test_patient_registration.py`):

```python
import pytest
from uuid import uuid4
from src.database.repositories.patient_repository import PatientRepository


def test_create_patient(patient_repo):
    """Test patient creation."""
    department_id = uuid4()
    
    patient_id = patient_repo.create(
        first_name="John",
        last_name="Doe",
        date_of_birth="1990-05-15",
        age=34,
        phone="+1-555-123-4567",
        department_id=department_id,
        medical_record="Initial checkup"
    )
    
    assert patient_id is not None
    
    # Verify patient was created
    patient = patient_repo.get_by_id(patient_id)
    assert patient.first_name == "John"
    assert patient.last_name == "Doe"
    assert patient.age == 34


def test_find_patient_by_name(patient_repo):
    """Test finding patient by name."""
    department_id = uuid4()
    
    # Create test patient
    patient_repo.create(
        first_name="Jane",
        last_name="Smith",
        date_of_birth="1985-03-20",
        age=39,
        phone="+1-555-987-6543",
        department_id=department_id
    )
    
    # Search by first name
    results = patient_repo.find_by_name(first_name="Jane")
    assert len(results) > 0
    assert results[0].first_name == "Jane"


def test_invalid_patient_creation(patient_repo):
    """Test patient creation with invalid data."""
    with pytest.raises(ValueError):
        patient_repo.create(
            first_name="",  # Empty name should raise error
            last_name="Doe",
            date_of_birth="1990-05-15",
            age=34,
            phone="+1-555-123-4567",
            department_id=uuid4()
        )


@pytest.fixture
def patient_repo(session):
    """Fixture to provide patient repository."""
    return PatientRepository(session)
```

### Test Organization

```
tests/
├── __init__.py
├── conftest.py                      # Shared fixtures
├── test_patient_registration.py    # Patient tests
├── test_hospital_management.py     # Hospital tests
├── test_department_management.py   # Department tests
├── test_staff_management.py        # Staff tests
└── integration/                     # Integration tests
    ├── __init__.py
    └── test_full_workflow.py
```

### Fixtures (`tests/conftest.py`):

```python
import pytest
from src.database.connection import ScyllaDBConnection
from src.database.init_db import initialize_database


@pytest.fixture(scope="session")
def db_connection():
    """Database connection fixture."""
    db = ScyllaDBConnection()
    session = db.connect()
    initialize_database(session)
    yield session
    db.close()


@pytest.fixture
def session(db_connection):
    """Session fixture."""
    return db_connection
```

## <span id="docker-commands"></span>🐳 Docker Commands

### Image Management

```bash
# Build Docker image
docker build -t hospital-management-app .

# Build without cache
docker build -t hospital-management-app . --no-cache

# Build with specific tag
docker build -t hospital-management-app:v2.0 .

# List images
docker images | grep hospital

# Remove image
docker rmi hospital-management-app

# Remove all unused images
docker image prune -a
```

### Container Operations

```bash
# Run container (interactive)
docker run -it --rm hospital-management-app python main.py

# Run container (detached)
docker run -d --name hospital-app hospital-management-app

# Run with environment file
docker run -it --rm --env-file .env hospital-management-app python main.py

# Run Streamlit container
docker run -p 8501:8501 \
  -e SCYLLA_HOST=new-scylla-node \
  -e SCYLLA_PORT=9042 \
  --network new-scylla-net \
  hospital-management-app

# Run with volume mount (development)
docker run -p 8501:8501 \
  -v $(pwd):/app \
  -e SCYLLA_HOST=new-scylla-node \
  --network new-scylla-net \
  hospital-management-app

# Stop container
docker stop hospital-app

# Start container
docker start hospital-app

# Restart container
docker restart hospital-app

# Remove container
docker rm hospital-app

# Remove all stopped containers
docker container prune
```

### Docker Compose Commands

```bash
# Start services
docker-compose up

# Start in detached mode
docker-compose up -d

# Build and start
docker-compose up --build

# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Remove volumes too
docker-compose down -v

# View logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Logs for specific service
docker-compose logs -f hospital-app

# List services
docker-compose ps

# Restart specific service
docker-compose restart hospital-app

# Execute command in service
docker-compose exec hospital-app python main.py

# Scale service (if configured)
docker-compose up -d --scale hospital-app=3
```

### Network Configuration

```bash
# Create network for ScyllaDB
docker network create new-scylla-net

# List networks
docker network ls

# Inspect network
docker network inspect new-scylla-net

# Remove network
docker network rm new-scylla-net

# Connect container to network
docker network connect new-scylla-net hospital-app

# Disconnect container from network
docker network disconnect new-scylla-net hospital-app

# Run ScyllaDB on network
docker run -d --network new-scylla-net --name scylladb scylladb/scylla

# Run application on same network
docker run -it --rm --network new-scylla-net hospital-management-app python main.py
```

### Volume Management

```bash
# List volumes
docker volume ls

# Create volume
docker volume create scylla_data

# Inspect volume
docker volume inspect scylla_data

# Remove volume
docker volume rm scylla_data

# Remove all unused volumes
docker volume prune

# Backup volume to tar
docker run --rm \
  -v scylla_data:/data \
  -v $(pwd):/backup \
  ubuntu tar czf /backup/scylla_backup.tar.gz /data

# Restore volume from tar
docker run --rm \
  -v scylla_data:/data \
  -v $(pwd):/backup \
  ubuntu tar xzf /backup/scylla_backup.tar.gz -C /
```

### Debugging

```bash
# View container logs
docker logs hospital-app

# Follow logs in real-time
docker logs -f hospital-app

# Execute shell in container
docker exec -it hospital-app /bin/bash

# Execute Python in container
docker exec -it hospital-app python

# Check container stats
docker stats hospital-app

# Inspect container
docker inspect hospital-app

# View container processes
docker top hospital-app

# Port mappings
docker port hospital-app
```

### System Management

```bash
# View Docker system info
docker system info

# Check disk usage
docker system df

# Clean up everything
docker system prune -a

# Clean up with volumes
docker system prune -a --volumes

# Monitor events
docker events

# Monitor events for specific container
docker events --filter 'container=hospital-app'
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
| `/patients/search` | POST | Search patients | Patient array |

### Hospital Management

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/hospitals` | GET | List all hospitals | Hospital array |
| `/hospitals/<id>` | GET | Get hospital by ID | Hospital object |
| `/hospitals` | POST | Create new hospital | Created hospital object |
| `/hospitals/<id>` | PUT | Update hospital | Updated hospital object |
| `/hospitals/<id>` | DELETE | Delete hospital | Success message |

### Department Management

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/departments` | GET | List all departments | Department array |
| `/departments/<id>` | GET | Get department by ID | Department object |
| `/departments` | POST | Create new department | Created department object |
| `/departments/<id>` | PUT | Update department | Updated department object |
| `/departments/<id>` | DELETE | Delete department | Success message |
| `/departments/hospital/<id>` | GET | Get by hospital | Department array |

### Staff Management

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/staff` | GET | List all staff | Staff array |
| `/staff/<id>` | GET | Get staff by ID | Staff object |
| `/staff` | POST | Create new staff | Created staff object |
| `/staff/<id>` | PUT | Update staff | Updated staff object |
| `/staff/<id>` | DELETE | Delete staff | Success message |
| `/staff/department/<id>` | GET | Get by department | Staff array |

### System Status

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/health` | GET | System health check | Health status |
| `/status` | GET | Application status | Status information |
| `/metrics` | GET | System metrics | Metrics data |

## <span id="troubleshooting"></span>🔧 Troubleshooting

### Database Connection Issues

**Error: Connection refused**

```bash
# Solution 1: Check ScyllaDB is running
docker ps | grep scylla

# Solution 2: Start ScyllaDB
docker run -d --name scylla scylladb/scylla

# Solution 3: Check network connectivity
docker network inspect new-scylla-net

# Solution 4: Verify connection settings in .env
cat .env | grep SCYLLA

# Solution 5: Test connection
docker exec -it new-scylla-node cqlsh

# Solution 6: Check ScyllaDB logs
docker logs new-scylla-node
```

**Error: Keyspace not found**

```bash
# Solution: Initialize database
python -c "from src.database.init_db import initialize_database; \
from src.database.connection import ScyllaDBConnection; \
db = ScyllaDBConnection(); \
initialize_database(db.connect())"
```

### Docker Issues

**Error: Port already in use**

```bash
# Solution 1: Use different port
docker run -p 9043:9042 scylladb/scylla

# Solution 2: Stop conflicting container
docker ps | grep 9042
docker stop <container_id>

# Solution 3: Kill process using port
lsof -i :9042
kill -9 <PID>
```

**Error: Docker daemon not running**

```bash
# Solution: Start Docker Desktop or Docker Engine
# Windows/macOS: Launch Docker Desktop
# Linux:
sudo systemctl start docker
sudo systemctl enable docker
```

**Error: Cannot connect to Docker daemon**

```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker run hello-world
```

**Error: No space left on device**

```bash
# Clean up Docker system
docker system prune -a --volumes

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune
```

### Streamlit Issues

**Error: Streamlit not found**

```bash
# Solution: Install dependencies
poetry install

# Or install streamlit directly
pip install streamlit
```

**Error: Port 8501 already in use**

```bash
# Solution 1: Use different port
streamlit run streamlit_app/app.py --server.port=8502

# Solution 2: Kill process on port
lsof -i :8501
kill -9 <PID>
```

**Error: Module not found**

```bash
# Solution: Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src:$(pwd)"

# Or in dockerfile
ENV PYTHONPATH="/app/src:/app"
```

### Input Validation Errors

**Error: Date format invalid**

```
Error: time data '05-15-1990' does not match format '%Y-%m-%d'

# Solution: Use YYYY-MM-DD format
# Correct: 1990-05-15
# Wrong: 05-15-1990 or 1990/05/15
```

**Error: Required field missing**

```
ValueError: First and last name are required

# Solution: Ensure all required fields are filled
# Check form for asterisk (*) indicating required
```

### Poetry Issues

**Error: Package not found**

```bash
# Solution 1: Update poetry
poetry self update

# Solution 2: Clear cache
poetry cache clear pypi --all

# Solution 3: Reinstall dependencies
rm poetry.lock
poetry install
```

**Error: Dependency conflicts**

```bash
# Solution: Update dependencies
poetry update

# Or update specific package
poetry update streamlit
```

### Application Errors

**Error: ImportError**

```bash
# Solution: Check Python path
echo $PYTHONPATH

# Add src to path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

**Error: Permission denied**

```bash
# Solution: Fix file permissions
chmod +x main.py
chmod -R 755 streamlit_app/
```

### Performance Issues

**Slow Database Queries**

```bash
# Solution 1: Check indexes
docker exec -it new-scylla-node cqlsh -e "DESCRIBE INDEX ON hospital.patients"

# Solution 2: Analyze query performance
# Enable tracing in CQL

# Solution 3: Optimize queries
# Use WHERE clauses on indexed columns
```

**High Memory Usage**

```bash
# Solution: Monitor Docker resources
docker stats

# Limit container memory
docker run --memory="2g" hospital-management-app

# In docker-compose.yml:
# services:
#   hospital-app:
#     mem_limit: 2g
```

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `Connection refused` | ScyllaDB not running | Start ScyllaDB container |
| `Module not found` | Missing dependencies | Run `poetry install` |
| `Port already in use` | Port conflict | Change port or stop conflicting service |
| `Permission denied` | File permissions | Use `chmod` to fix permissions |
| `No space left` | Disk full | Clean up Docker with `docker system prune` |
| `Invalid date format` | Wrong date format | Use YYYY-MM-DD format |
| `Keyspace not found` | DB not initialized | Run `initialize_database()` |

## <span id="contributing"></span>🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Workflow

1. **Fork the Repository**:
   ```bash
   # Click "Fork" on GitHub
   git clone https://github.com/your-username/hospital-management.git
   cd hospital-management
   ```

2. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/add-doctor-management
   ```

3. **Make Your Changes**:
   - Write code
   - Add tests
   - Update documentation

4. **Test Thoroughly**:
   ```bash
   # Run tests
   poetry run pytest
   
   # Check coverage
   poetry run pytest --cov=src
   
   # Format code
   poetry run black src/
   
   # Lint
   poetry run flake8 src/
   ```

5. **Commit with Clear Messages**:
   ```bash
   git add .
   git commit -m 'feat: add doctor management feature'
   ```

6. **Push to Your Fork**:
   ```bash
   git push origin feature/add-doctor-management
   ```

7. **Open a Pull Request**:
   - Go to GitHub
   - Click "New Pull Request"
   - Provide detailed description
   - Link related issues

### Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

**Examples**:
```bash
feat(patients): add blood type field to patient model
fix(search): resolve case-sensitive search issue
docs(readme): update Docker deployment instructions
test(patients): add tests for patient validation
```

### Code Standards

- **Follow PEP 8**: Python style guidelines
- **Add Tests**: New features need tests
- **Update Documentation**: Keep docs current
- **Use Meaningful Names**: Clear variable and function names
- **Add Docstrings**: Document functions and classes
- **Type Hints**: Use type annotations
- **Error Handling**: Handle exceptions gracefully

### Before Submitting PR

```bash
# Format code
poetry run black src/ streamlit_app/ tests/

# Run linter
poetry run flake8 src/ streamlit_app/

# Run tests
poetry run pytest

# Check coverage
poetry run pytest --cov=src

# Type checking
poetry run mypy src/

# Update documentation
# Edit README.md if needed
```

### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] Tests added for new features
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main
- [ ] No merge conflicts
- [ ] PR description is detailed

### Code Review Process

1. **Automated Checks**: CI/CD runs tests
2. **Peer Review**: Maintainers review code
3. **Feedback**: Address review comments
4. **Approval**: Get approval from maintainer
5. **Merge**: PR is merged to main

### Getting Help

- **GitHub Issues**: Report bugs or request features
- **Discussions**: Ask questions
- **Discord/Slack**: Join community chat
- **Email**: Contact maintainers

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

- **Documentation**: Check this README first
- **Troubleshooting**: See the [Troubleshooting](#troubleshooting) section
- **GitHub Issues**: [Create an issue](https://github.com/your-username/hospital-management/issues)
- **Stack Overflow**: Tag with `hospital-management-system`
- **Email**: support@hospital-management.local

### Common Issues and Solutions

#### ScyllaDB Won't Connect

```bash
# Check ScyllaDB is running
docker ps | grep scylla

# Check connection settings
grep SCYLLA .env

# Test connection
python -c "from src.database.connection import ScyllaDBConnection; \
ScyllaDBConnection().connect()"

# Check Docker network
docker network inspect new-scylla-net
```

#### Streamlit App Won't Start

```bash
# Check dependencies
poetry install

# Check port availability
lsof -i :8501

# Run with explicit config
streamlit run streamlit_app/app.py \
  --server.port=8501 \
  --server.address=0.0.0.0
```

#### Date Validation Error

```
Error: time data '05-15-1990' does not match format '%Y-%m-%d'

# Use correct format: YYYY-MM-DD
# Correct: 1990-05-15
# Wrong: 05-15-1990 or 05/15/1990
```

#### Missing Dependencies

```bash
# Reinstall dependencies
poetry install

# Update dependencies
poetry update

# Check Python version
python --version  # Should be 3.10+

# Check Poetry version
poetry --version
```

#### Docker Compose Issues

```bash
# Rebuild containers
docker-compose up --build

# Reset everything
docker-compose down -v
docker-compose up -d

# View logs
docker-compose logs -f

# Check service health
docker-compose ps
```

### Feature Requests

To request a new feature:

1. **Check existing issues**: Search for similar requests
2. **Create new issue**: Use feature request template
3. **Provide details**:
   - Use case description
   - Expected behavior
   - Benefits to users
   - Implementation ideas (optional)

### Bug Reports

To report a bug:

1. **Check existing issues**: Avoid duplicates
2. **Create new issue**: Use bug report template
3. **Include**:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Error messages
   - Environment details
   - Screenshots (if applicable)

**Bug Report Template**:

```markdown
## Bug Description
[Clear description of the bug]

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.10.5]
- Docker: [e.g., 24.0.6]
- Browser: [e.g., Chrome 120]

## Error Messages
```
[Paste error messages here]
```

## Screenshots
[If applicable]
```

### Security Issues

**Do not report security vulnerabilities publicly.**

Instead:
1. Email: security@hospital-management.local
2. Include detailed description
3. Wait for response before disclosure

### Community

- **GitHub Discussions**: Ask questions, share ideas
- **Discord**: [Join our server](https://discord.gg/hospital-mgmt)
- **Twitter**: [@HospitalMgmtSys](https://twitter.com/HospitalMgmtSys)
- **Blog**: [blog.hospital-management.local](https://blog.hospital-management.local)

### Resources

- **Official Documentation**: [docs.hospital-management.local](https://docs.hospital-management.local)
- **API Reference**: [api.hospital-management.local](https://api.hospital-management.local)
- **Video Tutorials**: [YouTube Channel](https://youtube.com/@HospitalMgmt)
- **ScyllaDB Docs**: [docs.scylladb.com](https://docs.scylladb.com)
- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)

---

**Made with ❤️ by the Hospital Management System Team**

*Empowering healthcare providers with scalable, modern patient management solutions.*

---

## 🔗 Quick Links

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Docker Deployment](#docker-deployment)
- [Streamlit App](#streamlit-web-application)
- [API Documentation](#api-endpoints)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
