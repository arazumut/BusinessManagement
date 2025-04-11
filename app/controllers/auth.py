from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, ROLE_EMPLOYEE
from app.forms.auth import LoginForm, RegistrationForm, PasswordResetRequestForm, PasswordResetForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Kullanıcı giriş sayfası"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('main.dashboard')
            flash('Giriş başarılı!', 'success')
            return redirect(next_page)
        flash('Geçersiz e-posta veya şifre', 'danger')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """Kullanıcı çıkış işlemi"""
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Kullanıcı kayıt sayfası"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data,
            role=ROLE_EMPLOYEE  # Varsayılan rol: Personel
        )
        db.session.add(user)
        db.session.commit()
        flash('Hesabınız başarıyla oluşturuldu! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    """Şifre sıfırlama isteği sayfası"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Burada şifre sıfırlama e-postası gönderme işlemi yapılabilir
            # Şimdilik sadece flash mesajı ile belirteceğiz
            flash('Şifre sıfırlama talimatları e-posta adresinize gönderildi.', 'info')
        else:
            flash('Bu e-posta adresiyle kayıtlı bir kullanıcı bulunamadı.', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', form=form)

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Şifre sıfırlama sayfası"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    # Token doğrulama işlemi burada yapılacak
    # Şimdilik test için direkt form göstereceğiz
    
    form = PasswordResetForm()
    if form.validate_on_submit():
        # Burada şifre değiştirme işlemi yapılacak
        flash('Şifreniz başarıyla değiştirildi. Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/profile', methods=['GET'])
@login_required
def profile():
    """Kullanıcı profili sayfası"""
    return render_template('auth/profile.html') 