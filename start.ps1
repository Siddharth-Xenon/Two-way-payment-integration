# start.ps1

Write-Host "Starting Two Way Strip Payment System Sync Project setup..."

# Check if Docker is installed
if (-Not (Get-Command "docker" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Docker is not installed." -ForegroundColor Red
    exit 1
}

# Check if Docker Compose is installed
if (-Not (Get-Command "docker-compose" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Docker Compose is not installed." -ForegroundColor Red
    exit 1
}

# Start Docker containers
Write-Host "Starting Docker containers..."
docker-compose up -d

Write-Host "Setting up environment configuration..."
Copy-Item "example.env" -Destination ".env" -Force
Write-Host "Environment configuration file (.env) created from example.env."


# Fetch the path to the Python 3.10 executable and create a virtual environment
# $pythonPath = Get-Command "python3.10" -ErrorAction SilentlyContinue
# if ($null -eq $pythonPath) {
#     Write-Host "Python 3.10 is required. Please install it to proceed." -ForegroundColor Red
#     exit 1
# }

# Create a virtual environment
Write-Host "Creating virtual environment..."
python -m venv venv
. .\venv\Scripts\Activate.ps1
# Install Python dependencies
Write-Host "Installing Python dependencies..."
pip install -r requirements.txt

# Set up environment variables
if (-Not (Test-Path ".env")) {
    Write-Host "Environment file not found. Please create a .env file with the necessary configurations." -ForegroundColor Red
    exit 1
}

# Start the FastAPI server
# Write-Host "Starting FastAPI server..."
# uvicorn app.main:app --reload



Write-Host "Setup completed. Please enter the necessary details in the .env file."
Write-Host "Expose 8000 port to Ngrok and use the url to configure the webhook in the stripe dashboard."
Write-Host "To start the server, run: uvicorn app.main:app --port 8000"
Write-Host "Visit http://localhost:8000/docs for API documentation."

