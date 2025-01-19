# Automation

## Overview

This project is a Flask application that integrates with Autodesk Forge API and Monday.com. It uses test-driven development to ensure robust functionality.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```

2. **Copy the environment example file and fill in your credentials:**

   ```bash
   cp env-example .env
   ```

   Edit the `.env` file and replace the placeholder values with your actual credentials.

3. **Build and run the application:**

   ```bash
   docker-compose up --build
   ```

   This will start the Flask application and the test runner service.

## Testing

The application includes a test runner service that executes tests using the `tests/test_webhook.py` script. Ensure that the `TEST_MODE` environment variable is set to `true` in your `.env` file.

## Access

- The application will be accessible at `http://localhost:8080`.
- Health checks are performed at `http://localhost:8080/health`.

## Notes

- Ensure you have access to a project in BuildingConnected to fully test the integration.
- For any issues, please contact the development team.
