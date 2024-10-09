import os

class Config:
    SECRET_KEY = 'your_secret_key_here'
    CKEDITOR_PKG_TYPE = 'standard'
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
