#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies and compile Tailwind CSS v4
npm install
npm run build:css

# Collect static files into STATIC_ROOT
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate
