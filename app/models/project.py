from app import db
from datetime import datetime

# Proje durumları için sabitler
PROJECT_STATUS_PLANNED = 'planlandi'
PROJECT_STATUS_INPROGRESS = 'devam_ediyor'
PROJECT_STATUS_COMPLETED = 'tamamlandi'
PROJECT_STATUS_CANCELLED = 'iptal_edildi'

PROJECT_STATUSES = [
    (PROJECT_STATUS_PLANNED, 'Planlandı'),
    (PROJECT_STATUS_INPROGRESS, 'Devam Ediyor'),
    (PROJECT_STATUS_COMPLETED, 'Tamamlandı'),
    (PROJECT_STATUS_CANCELLED, 'İptal Edildi')
]

class Project(db.Model):
    """Proje modeli - Şirket projelerini temsil eder"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default=PROJECT_STATUS_PLANNED)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    manager = db.relationship('User', foreign_keys=[manager_id])
    assignments = db.relationship('ProjectAssignment', back_populates='project', cascade='all, delete-orphan')
    tasks = db.relationship('Task', back_populates='project', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Project {self.name}>"

class ProjectAssignment(db.Model):
    """Proje Atama modeli - Projelere çalışan atamalarını temsil eder"""
    __tablename__ = 'project_assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    role = db.Column(db.String(50))
    start_date = db.Column(db.Date, default=datetime.utcnow)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    project = db.relationship('Project', back_populates='assignments')
    employee = db.relationship('Employee', back_populates='project_assignments')
    
    def __repr__(self):
        return f"<ProjectAssignment {self.employee.user.full_name} on {self.project.name}>"

# Görev durumları için sabitler
TASK_STATUS_TODO = 'yapilacak'
TASK_STATUS_INPROGRESS = 'devam_ediyor'
TASK_STATUS_COMPLETED = 'tamamlandi'
TASK_STATUS_BLOCKED = 'engellendi'

TASK_STATUSES = [
    (TASK_STATUS_TODO, 'Yapılacak'),
    (TASK_STATUS_INPROGRESS, 'Devam Ediyor'),
    (TASK_STATUS_COMPLETED, 'Tamamlandı'),
    (TASK_STATUS_BLOCKED, 'Engellendi')
]

class Task(db.Model):
    """Görev modeli - Projelere ait görevleri temsil eder"""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default=TASK_STATUS_TODO)
    priority = db.Column(db.Integer, default=0)  # 0-Düşük, 1-Normal, 2-Yüksek
    assigned_to = db.Column(db.Integer, db.ForeignKey('employees.id'))
    due_date = db.Column(db.Date)
    completion_percentage = db.Column(db.Integer, default=0)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    project = db.relationship('Project', back_populates='tasks')
    assignee = db.relationship('Employee', foreign_keys=[assigned_to])
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def __repr__(self):
        return f"<Task {self.title} for {self.project.name}>" 