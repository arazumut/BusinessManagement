from app import db
from datetime import datetime

class Department(db.Model):
    """Departman modeli - Şirketteki departmanları temsil eder"""
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    employees = db.relationship('Employee', back_populates='department')
    positions = db.relationship('Position', back_populates='department', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Department {self.name}>"


class Position(db.Model):
    """Pozisyon modeli - Şirketteki iş pozisyonlarını temsil eder"""
    __tablename__ = 'positions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    department = db.relationship('Department', back_populates='positions')
    employees = db.relationship('Employee', back_populates='position')
    
    def __repr__(self):
        return f"<Position {self.name} in {self.department.name}>" 