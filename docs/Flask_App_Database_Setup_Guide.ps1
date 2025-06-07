
# Flask App Database Setup Guide (with Flask-Migrate)

# 📁 Project Overview
# This script helps initialize and manage the SQLite database schema for a Flask app using Flask-Migrate.

# 🧰
# 0. Requirements: Install required packages
pip install flask flask_sqlalchemy flask_migrate flask_cors werkzeug

# 🏗️ Step-by-Step Setup

# 1. Set FLASK_APP Environment Variable
# For PowerShell (Windows)
$env:FLASK_APP = "app.py"

# 2. Initialize Migration Directory (Once Only)
flask db init # This creates a migrations directory in your project root. (Eg: migrations/) and # sets up the instance database directory.

# 3. Create Initial Migration Script
flask db migrate -m "Initial DB migration - 1st commit" # This command generates a migration script based on the current state of your models and database file is creaated.

# 4. Apply the Migration to Create Tables
flask db upgrade # This command applies the migration script to the database, creating the necessary tables finally.

# 🔄 Making Schema Changes Later
# Whenever you update a model, run the following:
# flask db migrate -m "Describe your schema change"
# flask db upgrade

# ❌ Important Note
# Avoid calling db.create_all() in production code when using Flask-Migrate.
# Migrations give you more control and safety over your schema changes.

# ✅ Done!
# Your Flask app now uses a reliable and professional approach for managing database changes!

# Yes, after setting everything up with Flask-Migrate, you can run your Flask app using:
# 5. Run the Flask Application
flask run

# (Optional) Enable development mode for auto-reload and debug mode
$env:FLASK_ENV = "development"

# Make sure migrations are complete
flask db upgrade

# 5. Run the Flask Application
flask run

# 📝 If all is set correctly, you should see something like:
#  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

# 🖥️ Open the Flask App in Chrome
# Ensure you have Chrome installed and available in your PATH.
# If you want to open the Flask app in Chrome automatically, you can use the following command:
# 🚀 Start the Flask server and open it in Chrome
# Note: Ensure you have Chrome installed and available in your PATH.
# This command will start the Flask server and open the app in Chrome.
# If you want to run the Flask app in the background, you can use:
Start-Process "chrome.exe" "http://127.0.0.1:5000/" 
flask run 
