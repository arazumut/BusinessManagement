from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Employee, Department, Position, Leave, Project, Task, ProjectAssignment
from datetime import datetime

main = Blueprint('main', __name__)

@main.app_context_processor
def utility_processor():
    """Şablonlar için yardımcı işlevler"""
    return {
        'now': datetime.now()
    }

@main.route('/')
def index():
    """Ana sayfa"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    """Kontrol Paneli - rol bazlı içerik gösterir"""
    
    # İstatistikler - tüm roller için
    stats = {}
    stats['total_employees'] = Employee.query.filter_by(is_active=True).count()
    stats['total_departments'] = Department.query.filter_by(is_active=True).count()
    stats['pending_leaves'] = Leave.query.filter_by(status='beklemede').count()
    
    # Sadece admin veya yöneticiler için
    if current_user.is_admin() or current_user.is_manager():
        stats['total_projects'] = Project.query.count()
        
        # Departmanlara göre çalışan sayıları
        departments = Department.query.filter_by(is_active=True).all()
        dept_stats = []
        for dept in departments:
            dept_stats.append({
                'name': dept.name,
                'employee_count': Employee.query.filter_by(department_id=dept.id, is_active=True).count()
            })
        stats['departments'] = dept_stats
        
        # İzin talepleri
        pending_leave_requests = Leave.query.filter_by(status='beklemede').limit(5).all()
    else:
        # Normal çalışanlar için
        stats['total_projects'] = Project.query.join(
            ProjectAssignment, Project.id == ProjectAssignment.project_id
        ).join(
            Employee, ProjectAssignment.employee_id == Employee.id
        ).join(
            User, Employee.user_id == User.id
        ).filter(User.id == current_user.id).count()
        
        # Çalışanın izin talepleri
        employee = Employee.query.filter_by(user_id=current_user.id).first()
        if employee:
            pending_leave_requests = Leave.query.filter_by(
                employee_id=employee.id
            ).order_by(Leave.created_at.desc()).limit(5).all()
        else:
            pending_leave_requests = []
    
    return render_template('dashboard.html', stats=stats, leave_requests=pending_leave_requests) 