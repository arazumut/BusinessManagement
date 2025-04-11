from app import db
from datetime import datetime

class Employee(db.Model):
    """Çalışan modeli - Tüm çalışanları temsil eder"""
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tc_kimlik = db.Column(db.String(11), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'))
    salary = db.Column(db.Float)
    hire_date = db.Column(db.Date, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    user = db.relationship('User', back_populates='employee_profile')
    department = db.relationship('Department', back_populates='employees')
    position = db.relationship('Position', back_populates='employees')
    leaves = db.relationship('Leave', back_populates='employee', cascade='all, delete-orphan')
    project_assignments = db.relationship('ProjectAssignment', back_populates='employee', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Employee {self.user.full_name}>" 