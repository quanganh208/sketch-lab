import os

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Upload settings
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads', 'original')
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads', 'processed')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Flask settings
SECRET_KEY = 'your-secret-key-change-this-in-production'
DEBUG = True

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
