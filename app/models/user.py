from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Kullanıcı rolleri için sabitler
ROLE_ADMIN = 'admin'
ROLE_MANAGER = 'yonetici'
ROLE_EMPLOYEE = 'personel'

class User(UserMixin, db.Model):
    """Kullanıcı modeli - Tüm sistem kullanıcılarını temsil eder"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default=ROLE_EMPLOYEE)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    employee_profile = db.relationship('Employee', back_populates='user', uselist=False)
    
    @property
    def full_name(self):
        """Kullanıcının tam adını döndürür"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def password(self):
        """Şifre özelliğini okumak için hata verir"""
        raise AttributeError('Şifre salt-okunur bir alandır')
    
    @password.setter
    def password(self, password):
        """Şifreyi hashlenir ve kaydeder"""
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """Verilen şifreyi doğrular"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Kullanıcının admin olup olmadığını kontrol eder"""
        return self.role == ROLE_ADMIN
    
    def is_manager(self):
        """Kullanıcının yönetici olup olmadığını kontrol eder"""
        return self.role == ROLE_MANAGER
    
    def __repr__(self):
        return f"<User {self.email}>"

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login için kullanıcı yükleyici fonksiyonu"""
    return User.query.get(int(user_id)) 