# My Project

## Overview
A Python project with comprehensive diagnostics, database connectivity checks, API monitoring, and Docker status verification.

## Features
- 🔍 Comprehensive system diagnostics
- 🗄️ Database connectivity testing
- 🌐 API status monitoring
- 🐳 Docker daemon verification
- 📊 System resource monitoring
- 🔧 Environment variable validation

## Prerequisites
- Python 3.8+
- Poetry (for dependency management)
- Docker (optional, for containerization)

## Setup
1. Clone the repository
2. Install Poetry if not already installed:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Install dependencies:
   ```bash
   poetry install
   ```
4. Copy environment variables:
   ```bash
   cp .env.example .env
   ```
5. Update `.env` with your actual values, especially the `OPENAI_API_KEY`

## Usage

### Running Diagnostics
```bash
poetry run python diagnostics.py
```

### Available Make Commands
- `make install` - Install dependencies
- `make test` - Run tests
- `make lint` - Run linting
- `make format` - Format code with Black
- `make check` - Run type checking with MyPy
- `make run` - Run the main application
- `make clean` - Clean Poetry environment
- `make build` - Build the package
- `make publish` - Publish the package

## Folder Structure
- `data/` - Data files and databases
- `src/` - Source code
- `tests/` - Test cases
- `configs/` - Configuration files
- `scripts/` - Utility scripts
- `docs/` - Documentation
- `diagnostics.py` - Comprehensive health check script

## Diagnostics
The `diagnostics.py` script performs the following checks:
- System resources (CPU, memory, disk usage)
- Database connectivity
- External API status (OpenAI, GitHub)
- Docker daemon status
- Environment variable validation
- Python environment and dependencies

## Environment Variables
Required:
- `OPENAI_API_KEY` - Your OpenAI API key

Optional:
- `DEBUG` - Enable debug mode
- `DATABASE_URL` - Database connection string
- `API_BASE_URL` - Base URL for API calls

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request 