from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Department, Position
from functools import wraps
from app.controllers.employee import admin_or_manager_required

department = Blueprint('department', __name__)

@department.route('/')
@login_required
@admin_or_manager_required
def index():
    """Departmanları listele"""
    departments = Department.query.filter_by(is_active=True).all()
    return render_template('department/index.html', departments=departments)

@department.route('/create', methods=['GET', 'POST'])
@login_required
@admin_or_manager_required
def create():
    """Yeni departman ekle"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Departman adı gereklidir.', 'danger')
            return redirect(url_for('department.create'))
        
        # Aynı isimde departman var mı kontrol et
        existing = Department.query.filter_by(name=name).first()
        if existing:
            flash('Bu isimde bir departman zaten mevcut.', 'danger')
            return redirect(url_for('department.create'))
        
        department = Department(name=name, description=description)
        db.session.add(department)
        db.session.commit()
        
        flash('Departman başarıyla eklendi.', 'success')
        return redirect(url_for('department.index'))
    
    return render_template('department/create.html')

@department.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_or_manager_required
def edit(id):
    """Departman düzenle"""
    department = Department.query.get_or_404(id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Departman adı gereklidir.', 'danger')
            return redirect(url_for('department.edit', id=id))
        
        # Aynı isimde başka departman var mı kontrol et
        existing = Department.query.filter(Department.name == name, Department.id != id).first()
        if existing:
            flash('Bu isimde başka bir departman zaten mevcut.', 'danger')
            return redirect(url_for('department.edit', id=id))
        
        department.name = name
        department.description = description
        db.session.commit()
        
        flash('Departman başarıyla güncellendi.', 'success')
        return redirect(url_for('department.index'))
    
    return render_template('department/edit.html', department=department)

@department.route('/delete/<int:id>', methods=['POST'])
@login_required
@admin_or_manager_required
def delete(id):
    """Departmanı pasif yap (silme)"""
    department = Department.query.get_or_404(id)
    
    # İlişkili pozisyonlar ve çalışanlar var mı kontrol et
    if department.employees:
        flash('Bu departmanda çalışanlar bulunduğu için silinemez.', 'danger')
        return redirect(url_for('department.index'))
    
    # Gerçekten silme yerine pasif olarak işaretle
    department.is_active = False
    db.session.commit()
    
    flash('Departman başarıyla silindi.', 'success')
    return redirect(url_for('department.index'))

@department.route('/positions')
@login_required
@admin_or_manager_required
def positions():
    """Pozisyonları listele"""
    positions = Position.query.filter_by(is_active=True).all()
    departments = Department.query.filter_by(is_active=True).all()
    return render_template('department/positions.html', positions=positions, departments=departments)

@department.route('/positions/create', methods=['POST'])
@login_required
@admin_or_manager_required
def create_position():
    """Yeni pozisyon ekle"""
    name = request.form.get('name')
    department_id = request.form.get('department_id')
    description = request.form.get('description')
    
    if not name or not department_id:
        flash('Pozisyon adı ve departman seçimi gereklidir.', 'danger')
        return redirect(url_for('department.positions'))
    
    position = Position(
        name=name,
        department_id=department_id,
        description=description
    )
    db.session.add(position)
    db.session.commit()
    
    flash('Pozisyon başarıyla eklendi.', 'success')
    return redirect(url_for('department.positions'))

@department.route('/positions/edit/<int:id>', methods=['POST'])
@login_required
@admin_or_manager_required
def edit_position(id):
    """Pozisyon düzenle"""
    position = Position.query.get_or_404(id)
    
    name = request.form.get('name')
    department_id = request.form.get('department_id')
    description = request.form.get('description')
    
    if not name or not department_id:
        flash('Pozisyon adı ve departman seçimi gereklidir.', 'danger')
        return redirect(url_for('department.positions'))
    
    position.name = name
    position.department_id = department_id
    position.description = description
    db.session.commit()
    
    flash('Pozisyon başarıyla güncellendi.', 'success')
    return redirect(url_for('department.positions'))

@department.route('/positions/delete/<int:id>', methods=['POST'])
@login_required
@admin_or_manager_required
def delete_position(id):
    """Pozisyonu pasif yap (silme)"""
    position = Position.query.get_or_404(id)
    
    # İlişkili çalışanlar var mı kontrol et
    if position.employees:
        flash('Bu pozisyonda çalışanlar bulunduğu için silinemez.', 'danger')
        return redirect(url_for('department.positions'))
    
    # Gerçekten silme yerine pasif olarak işaretle
    position.is_active = False
    db.session.commit()
    
    flash('Pozisyon başarıyla silindi.', 'success')
    return redirect(url_for('department.positions'))