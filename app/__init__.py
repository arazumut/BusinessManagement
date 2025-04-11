from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config

# Uzantıları başlat
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Bu sayfaya erişmek için lütfen giriş yapın.'
migrate = Migrate()

def create_app(config_name='default'):
    """Flask uygulaması oluşturur ve yapılandırır."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Uzantıları başlat
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Route ve view'ları kaydet
    from app.controllers.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.controllers.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from app.controllers.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    from app.controllers.employee import employee as employee_blueprint
    app.register_blueprint(employee_blueprint, url_prefix='/employee')
    
    from app.controllers.department import department as department_blueprint
    app.register_blueprint(department_blueprint, url_prefix='/department')
    
    from app.controllers.leave import leave as leave_blueprint
    app.register_blueprint(leave_blueprint, url_prefix='/leave')
    
    from app.controllers.project import project as project_blueprint
    app.register_blueprint(project_blueprint, url_prefix='/project')
    
    return app 