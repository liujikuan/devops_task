# DevOps Task Package

## Overview
This project is a simple Flask web application that provides a health check endpoint. It is containerized using Docker and includes a CI/CD pipeline configured with GitHub Actions.

## Project Structure
```
DevOps_Task_Package
├── app
│   └── app.py          # Main application code
├── tests
│   └── test_app.py     # Tests for the application
├── .github
│   └── workflows
│       └── myworkflow.yml  # GitHub Actions workflow for CI/CD
├── Dockerfile           # Dockerfile for building the application image
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd DevOps_Task_Package
   ```

2. **Install dependencies:**
   Make sure you have Docker installed on your machine. You can build the Docker image and run the application using the following commands:
   ```bash
   docker build -t python-demo .
   docker run -d -p 5000:5000 python-demo
   ```

3. **Access the application:**
   Open your web browser and navigate to `http://localhost:5000/` to see the greeting message. You can also check the health endpoint at `http://localhost:5000/healthz`.

## Running Tests
To run the tests, you can execute the following command after starting the Docker container:
```bash
pytest tests
```

## CI/CD Pipeline
The project includes a GitHub Actions workflow that automatically builds the Docker image and runs tests on every push to the repository. You can also manually trigger the workflow from the GitHub Actions tab in your repository.

## License
This project is licensed under the MIT License.