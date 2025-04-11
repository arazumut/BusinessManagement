from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import User, Employee, Leave, LEAVE_TYPES, LEAVE_STATUSES
from app.models import LEAVE_STATUS_PENDING, LEAVE_STATUS_APPROVED, LEAVE_STATUS_REJECTED
from datetime import datetime, timedelta
from app.controllers.employee import admin_or_manager_required

leave = Blueprint('leave', __name__)

@leave.route('/')
@login_required
def index():
    """İzin taleplerini listele (rol bazlı)"""
    if current_user.is_admin() or current_user.is_manager():
        # Yöneticiler tüm izin taleplerini görebilir
        leaves = Leave.query.order_by(Leave.created_at.desc()).all()
    else:
        # Normal çalışanlar sadece kendi izin taleplerini görebilir
        employee = Employee.query.filter_by(user_id=current_user.id).first()
        if not employee:
            flash('Çalışan kaydınız bulunamadı.', 'danger')
            return redirect(url_for('main.dashboard'))
        
        leaves = Leave.query.filter_by(employee_id=employee.id).order_by(Leave.created_at.desc()).all()
    
    return render_template('leave/index.html', leaves=leaves, leave_types=dict(LEAVE_TYPES),
                          leave_statuses=dict(LEAVE_STATUSES))

@leave.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
    """İzin başvurusu yap"""
    employee = Employee.query.filter_by(user_id=current_user.id).first()
    if not employee:
        flash('Çalışan kaydınız bulunamadı. İzin başvurusu yapamazsınız.', 'danger')
        return redirect(url_for('leave.index'))
    
    if request.method == 'POST':
        leave_type = request.form.get('leave_type')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        reason = request.form.get('reason')
        
        # Validasyonlar
        if end_date < start_date:
            flash('Bitiş tarihi başlangıç tarihinden önce olamaz.', 'danger')
            return redirect(url_for('leave.apply'))
        
        # İzin gün sayısını hesapla (hafta sonlarını çıkararak)
        days = 0
        current_date = start_date
        while current_date <= end_date:
            # 0: Pazartesi, 6: Pazar
            if current_date.weekday() < 5:  # Hafta içi günler
                days += 1
            current_date += timedelta(days=1)
        
        leave = Leave(
            employee_id=employee.id,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            days=days,
            reason=reason,
            status=LEAVE_STATUS_PENDING
        )
        
        db.session.add(leave)
        db.session.commit()
        
        flash('İzin başvurunuz başarıyla kaydedildi.', 'success')
        return redirect(url_for('leave.index'))
    
    return render_template('leave/apply.html', leave_types=LEAVE_TYPES)

@leave.route('/cancel/<int:id>', methods=['POST'])
@login_required
def cancel(id):
    """İzin talebini iptal et"""
    employee = Employee.query.filter_by(user_id=current_user.id).first()
    if not employee:
        abort(403)
    
    leave = Leave.query.get_or_404(id)
    
    # Sadece kendi izin taleplerini iptal edebilir ve sadece beklemedeki talepler iptal edilebilir
    if leave.employee_id != employee.id:
        abort(403)
    
    if leave.status != LEAVE_STATUS_PENDING:
        flash('Sadece beklemede olan izin talepleri iptal edilebilir.', 'danger')
        return redirect(url_for('leave.index'))
    
    leave.status = 'iptal_edildi'
    db.session.commit()
    
    flash('İzin talebiniz iptal edildi.', 'success')
    return redirect(url_for('leave.index'))

@leave.route('/review/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_or_manager_required
def review(id):
    """İzin talebini değerlendir (yöneticiler için)"""
    leave = Leave.query.get_or_404(id)
    
    if request.method == 'POST':
        status = request.form.get('status')
        review_comment = request.form.get('review_comment')
        
        if status not in [LEAVE_STATUS_APPROVED, LEAVE_STATUS_REJECTED]:
            flash('Geçersiz izin durumu.', 'danger')
            return redirect(url_for('leave.review', id=id))
        
        leave.status = status
        leave.reviewed_by = current_user.id
        leave.review_date = datetime.utcnow()
        leave.review_comment = review_comment
        
        db.session.commit()
        
        status_text = 'onaylandı' if status == LEAVE_STATUS_APPROVED else 'reddedildi'
        flash(f'İzin talebi {status_text}.', 'success')
        return redirect(url_for('leave.index'))
    
    return render_template('leave/review.html', leave=leave, leave_types=dict(LEAVE_TYPES)) 