from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Employee, Project, ProjectAssignment, Task
from app.models import PROJECT_STATUSES, TASK_STATUSES
from app.controllers.employee import admin_or_manager_required
from datetime import datetime

project = Blueprint('project', __name__)

@project.route('/')
@login_required
def index():
    """Proje listesi"""
    if current_user.is_admin() or current_user.is_manager():
        # Yöneticiler tüm projeleri görebilir
        projects = Project.query.all()
    else:
        # Normal çalışanlar sadece katıldıkları projeleri görebilir
        employee = Employee.query.filter_by(user_id=current_user.id).first()
        if not employee:
            flash('Çalışan kaydınız bulunamadı.', 'danger')
            return redirect(url_for('main.dashboard'))
        
        projects = Project.query.join(ProjectAssignment).filter(
            ProjectAssignment.employee_id == employee.id
        ).all()
    
    return render_template('project/index.html', projects=projects, project_statuses=dict(PROJECT_STATUSES))

@project.route('/create', methods=['GET', 'POST'])
@login_required
@admin_or_manager_required
def create():
    """Yeni proje oluştur"""
    managers = User.query.filter(User.role.in_(['admin', 'yonetici']), User.is_active == True).all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        manager_id = request.form.get('manager_id')
        
        if not name:
            flash('Proje adı gereklidir.', 'danger')
            return redirect(url_for('project.create'))
        
        project = Project(
            name=name,
            description=description,
            manager_id=manager_id if manager_id else None
        )
        
        if start_date_str:
            project.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        
        if end_date_str:
            project.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        db.session.add(project)
        db.session.commit()
        
        flash('Proje başarıyla oluşturuldu.', 'success')
        return redirect(url_for('project.view', id=project.id))
    
    return render_template('project/create.html', managers=managers)

@project.route('/<int:id>')
@login_required
def view(id):
    """Proje detaylarını görüntüle"""
    project = Project.query.get_or_404(id)
    
    # Yetki kontrolü
    if not (current_user.is_admin() or current_user.is_manager()):
        employee = Employee.query.filter_by(user_id=current_user.id).first()
        if not employee or not ProjectAssignment.query.filter_by(
            project_id=id, employee_id=employee.id
        ).first():
            flash('Bu projeye erişim yetkiniz yok.', 'danger')
            return redirect(url_for('project.index'))
    
    # Proje ekibi
    team_members = ProjectAssignment.query.filter_by(project_id=id).all()
    
    # Görevler
    tasks = Task.query.filter_by(project_id=id).order_by(Task.priority.desc()).all()
    
    # İstatistikler
    stats = {}
    stats['total_tasks'] = len(tasks)
    stats['completed_tasks'] = sum(1 for t in tasks if t.status == 'tamamlandi')
    stats['completion_percentage'] = int(stats['completed_tasks'] / stats['total_tasks'] * 100) if stats['total_tasks'] > 0 else 0
    
    return render_template('project/view.html', project=project, team_members=team_members, 
                          tasks=tasks, stats=stats, task_statuses=dict(TASK_STATUSES)) 