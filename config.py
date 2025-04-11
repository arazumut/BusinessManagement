import os
from datetime import timedelta

class Config:
    # Flask ve uygulama ayarları
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gizli-anahtar-gelistirme-icin'
    FLASK_APP = os.environ.get('FLASK_APP') or 'run.py'
    
    # SQLAlchemy ayarları
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Oturum ayarları
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    
    # Upload ayarları
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///app.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'

# Yapılandırma ortamlarının bir sözlüğü
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 