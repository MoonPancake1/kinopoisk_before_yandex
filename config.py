import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config:
    UPLOAD_FOLDER = BASE_DIR + '/app/static/img'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False