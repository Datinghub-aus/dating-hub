#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset

echo "========================================"
echo "STARTING DATING HUB BUILD PROCESS"
echo "========================================"

# Debug: Show current directory
echo "Current directory: $(pwd)"
echo "Listing files:"
ls -la

# Install requirements
echo "1. Installing dependencies..."
pip install -r requirements.txt

# Collect static files (CRITICAL)
echo "2. Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run migrations
echo "3. Running database migrations..."
python manage.py migrate --noinput

# List collected static files
echo "4. Verifying static files were collected..."
find staticfiles/ -type f -name "*.html" | head -5

echo "========================================"
echo "BUILD COMPLETED SUCCESSFULLY"
echo "========================================"
