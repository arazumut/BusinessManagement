from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import User, Employee, Department, Position, ROLE_EMPLOYEE
from app.forms.employee import EmployeeForm
from datetime import datetime
from functools import wraps

employee = Blueprint('employee', __name__)

def admin_or_manager_required(f):
    """Sadece admin veya yöneticilerin erişebileceği route'lar için dekoratör"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin() and not current_user.is_manager():
            abort(403)  # Yetkisiz erişim
        return f(*args, **kwargs)
    return decorated_function

@employee.route('/')
@login_required
@admin_or_manager_required
def index():
    """Tüm çalışanları listele"""
    employees = Employee.query.filter_by(is_active=True).all()
    return render_template('employee/index.html', employees=employees)

@employee.route('/create', methods=['GET', 'POST'])
@login_required
@admin_or_manager_required
def create():
    """Yeni çalışan ekle"""
    form = EmployeeForm()
    
    # Departman ve pozisyon seçeneklerini doldur
    form.department_id.choices = [(d.id, d.name) for d in Department.query.filter_by(is_active=True).all()]
    form.position_id.choices = [(0, 'Seçiniz')] + [(p.id, f"{p.name} ({p.department.name})") 
                                                  for p in Position.query.filter_by(is_active=True).all()]
    
    if form.validate_on_submit():
        try:
            # Önce kullanıcı kaydı oluştur
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password='gecici123',  # Geçici şifre, kullanıcı daha sonra değiştirebilir
                role=ROLE_EMPLOYEE
            )
            db.session.add(user)
            db.session.flush()  # ID almak için flush
            
            # Sonra çalışan kaydı oluştur
            employee = Employee(
                user_id=user.id,
                tc_kimlik=form.tc_kimlik.data,
                phone=form.phone.data,
                address=form.address.data,
                department_id=form.department_id.data if form.department_id.data != 0 else None,
                position_id=form.position_id.data if form.position_id.data != 0 else None,
                salary=form.salary.data,
                hire_date=form.hire_date.data
            )
            db.session.add(employee)
            db.session.commit()
            
            flash('Çalışan başarıyla eklendi.', 'success')
            return redirect(url_for('employee.index'))
            
        except IntegrityError as e:
            db.session.rollback()
            flash('Kayıt sırasında bir hata oluştu. Lütfen bilgileri kontrol edin.', 'danger')
    
    return render_template('employee/create.html', form=form)

@employee.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_or_manager_required
def edit(id):
    """Çalışan bilgilerini düzenle"""
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(id=str(employee.id))
    
    if request.method == 'GET':
        # Form alanlarını mevcut değerlerle doldur
        form.first_name.data = employee.user.first_name
        form.last_name.data = employee.user.last_name
        form.email.data = employee.user.email
        form.tc_kimlik.data = employee.tc_kimlik
        form.phone.data = employee.phone
        form.address.data = employee.address
        form.department_id.data = employee.department_id if employee.department_id else 0
        form.position_id.data = employee.position_id if employee.position_id else 0
        form.salary.data = employee.salary
        form.hire_date.data = employee.hire_date
    
    # Departman ve pozisyon seçeneklerini doldur
    form.department_id.choices = [(0, 'Seçiniz')] + [(d.id, d.name) for d in Department.query.filter_by(is_active=True).all()]
    form.position_id.choices = [(0, 'Seçiniz')] + [(p.id, f"{p.name} ({p.department.name})") 
                                                  for p in Position.query.filter_by(is_active=True).all()]
    
    if form.validate_on_submit():
        try:
            # Kullanıcı bilgilerini güncelle
            employee.user.first_name = form.first_name.data
            employee.user.last_name = form.last_name.data
            employee.user.email = form.email.data
            
            # Çalışan bilgilerini güncelle
            employee.tc_kimlik = form.tc_kimlik.data
            employee.phone = form.phone.data
            employee.address = form.address.data
            employee.department_id = form.department_id.data if form.department_id.data != 0 else None
            employee.position_id = form.position_id.data if form.position_id.data != 0 else None
            employee.salary = form.salary.data
            employee.hire_date = form.hire_date.data
            
            db.session.commit()
            flash('Çalışan bilgileri başarıyla güncellendi.', 'success')
            return redirect(url_for('employee.index'))
            
        except IntegrityError:
            db.session.rollback()
            flash('Güncelleme sırasında bir hata oluştu. Lütfen bilgileri kontrol edin.', 'danger')
    
    return render_template('employee/edit.html', form=form, employee=employee)

@employee.route('/delete/<int:id>', methods=['POST'])
@login_required
@admin_or_manager_required
def delete(id):
    """Çalışanı pasif yap (silme)"""
    employee = Employee.query.get_or_404(id)
    
    # Gerçekten silme yerine pasif olarak işaretle
    employee.is_active = False
    employee.user.is_active = False
    
    db.session.commit()
    flash('Çalışan kaydı pasif hale getirildi.', 'success')
    
    return redirect(url_for('employee.index'))

@employee.route('/view/<int:id>')
@login_required
def view(id):
    """Çalışan detaylarını görüntüle"""
    # Admin/yönetici değilse ve kendisine ait değilse 403 hatası
    if not current_user.is_admin() and not current_user.is_manager():
        employee = Employee.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    else:
        employee = Employee.query.get_or_404(id)
    
    return render_template('employee/view.html', employee=employee)

@employee.route('/get_positions/<int:department_id>')
@login_required
def get_positions(department_id):
    """AJAX ile belirli bir departmana ait pozisyonları getir"""
    positions = Position.query.filter_by(department_id=department_id, is_active=True).all()
    position_list = [{'id': p.id, 'name': p.name} for p in positions]
    return jsonify(position_list) 