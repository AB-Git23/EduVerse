$ErrorActionPreference = "Stop"

Write-Host "Starting EduVerse Development Setup..." -ForegroundColor Cyan

# 1. Activate venv
$venvPath = ".venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    . $venvPath
} else {
    Write-Error "Virtual environment not found at .venv. Please create it first."
}

# 2. Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Green
pip install -r requirements.txt

# 3. specific migrations for apps if needed, but general migrate is usually enough
Write-Host "Running migrations..." -ForegroundColor Green
python manage.py migrate

# 4. Seed data
Write-Host "Seeding database..." -ForegroundColor Green
python manage.py dev_seed

# 5. System checks
Write-Host "Running system checks..." -ForegroundColor Green
python manage.py check

# 6. Linters
Write-Host "Running Black..." -ForegroundColor Green
black .
Write-Host "Running Flake8..." -ForegroundColor Green
flake8 .

# 7. Tests
Write-Host "Running tests..." -ForegroundColor Green
python manage.py test

# 8. Start server
Write-Host "Starting development server..." -ForegroundColor Green
python manage.py runserver
