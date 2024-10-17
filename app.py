@ -1,30 +1,31 @@
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from urllib.parse import urlparse
import math 

app = Flask(__name__)

# Load configuration from environment variables
app.secret_key = os.getenv('SECRET_KEY', 'your_fallback_secret_key')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/images')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB limit by default

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Retrieve the Internal Database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for the Flask application")

result = urlparse(DATABASE_URL)

# Function to connect to the database
