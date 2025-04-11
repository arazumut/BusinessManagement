from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import User, ROLE_ADMIN
from functools import wraps

admin = Blueprint('admin', __name__)

def admin_required(f):
    """Sadece admin rolünün erişebileceği route'lar için dekoratör"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            abort(403)  # Yetkisiz erişim
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@login_required
@admin_required
def index():
    """Admin panel ana sayfası"""
    return render_template('admin/index.html')

@admin.route('/users')
@login_required
@admin_required
def users():
    """Kullanıcı yönetim sayfası"""
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    """Kullanıcı düzenleme sayfası"""
    user = User.query.get_or_404(id)
    # Form işlemleri burada yapılacak
    return render_template('admin/edit_user.html', user=user)

@admin.route('/users/toggle/<int:id>', methods=['POST'])
@login_required
@admin_required
def toggle_user(id):
    """Kullanıcı aktif/pasif durumunu değiştir"""
    user = User.query.get_or_404(id)
    user.is_active = not user.is_active
    db.session.commit()
    flash(f"Kullanıcı {'aktif' if user.is_active else 'pasif'} duruma getirildi.", 'success')
    return redirect(url_for('admin.users'))

@admin.route('/system-settings')
@login_required
@admin_required
def system_settings():
    """Sistem ayarları sayfası"""
    return render_template('admin/system_settings.html') 