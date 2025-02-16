#!/bin/bash

echo "Setting up Secure Code Fix Recommendation System..."

# Step 1: Update and install required packages
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Step 2: Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Set up the database
echo "Initializing database..."
python -c "import database; database.init_db()"

# Step 4: Export environment variables
echo "Exporting environment variables..."
export $(grep -v '^#' .env | xargs)

# Step 5: Start the application
echo "Starting the Flask application..."
python backend/app.py &

echo "Setup completed successfully!"
