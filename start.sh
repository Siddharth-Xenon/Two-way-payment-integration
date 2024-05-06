#!/bin/bash

echo "Starting Two Way Strip Payment System Sync Project setup..."

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Error: Docker is not installed." >&2
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null
then
    echo "Error: Docker Compose is not installed." >&2
    exit 1
fi

# Start Docker containers
echo "Starting Docker containers..."
docker-compose up -d

echo "Setting up environment configuration..."
cp example.env .env
echo "Environment configuration file (.env) created from example.env."

# Create a virtual environment
echo "Creating virtual environment..."
python -m venv venv
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    source ./venv/bin/activate
elif [[ "$OSTYPE" == "darwin"* ]]; then
    source ./venv/bin/activate
elif [[ "$OSTYPE" == "msys"* ]]; then
    .\\venv\\Scripts\\Activate
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Set up environment variables
if [ ! -f ".env" ]; then
    echo "Environment file not found. Please create a .env file with the necessary configurations." >&2
    exit 1
fi

# Start the FastAPI server
# echo "Starting FastAPI server..."
# uvicorn app.main:app --reload

echo "Setup completed. Please enter the necessary details in the .env file."
echo "Expose 8000 port to Ngrok and use the url to configure the webhook in the stripe dashboard."
echo "To start the server, run: uvicorn app.main:app --port 8000"
echo "Visit http://localhost:8000/docs for API documentation."