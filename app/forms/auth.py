from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    """Kullanıcı giriş formu"""
    email = StringField('E-posta', validators=[
        DataRequired(message='E-posta adresi gerekli'),
        Email(message='Geçerli bir e-posta adresi girin')
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired(message='Şifre gerekli')
    ])
    remember_me = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')

class RegistrationForm(FlaskForm):
    """Kullanıcı kayıt formu"""
    first_name = StringField('Ad', validators=[
        DataRequired(message='Ad gerekli'),
        Length(min=2, max=50, message='Ad 2 ile 50 karakter arasında olmalıdır')
    ])
    last_name = StringField('Soyad', validators=[
        DataRequired(message='Soyad gerekli'),
        Length(min=2, max=50, message='Soyad 2 ile 50 karakter arasında olmalıdır')
    ])
    email = StringField('E-posta', validators=[
        DataRequired(message='E-posta adresi gerekli'),
        Email(message='Geçerli bir e-posta adresi girin'),
        Length(max=100, message='E-posta adresi çok uzun')
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired(message='Şifre gerekli'),
        Length(min=8, message='Şifre en az 8 karakter olmalıdır')
    ])
    confirm_password = PasswordField('Şifreyi Onayla', validators=[
        DataRequired(message='Şifre onayı gerekli'),
        EqualTo('password', message='Şifreler eşleşmiyor')
    ])
    submit = SubmitField('Kayıt Ol')
    
    def validate_email(self, field):
        """E-posta adresi benzersiz olmalı"""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Bu e-posta adresi zaten kullanılıyor. Lütfen başka bir tane deneyin.')

class PasswordResetRequestForm(FlaskForm):
    """Şifre sıfırlama isteği formu"""
    email = StringField('E-posta', validators=[
        DataRequired(message='E-posta adresi gerekli'),
        Email(message='Geçerli bir e-posta adresi girin')
    ])
    submit = SubmitField('Şifre Sıfırlama İsteği Gönder')

class PasswordResetForm(FlaskForm):
    """Şifre sıfırlama formu"""
    password = PasswordField('Yeni Şifre', validators=[
        DataRequired(message='Şifre gerekli'),
        Length(min=8, message='Şifre en az 8 karakter olmalıdır')
    ])
    confirm_password = PasswordField('Şifreyi Onayla', validators=[
        DataRequired(message='Şifre onayı gerekli'),
        EqualTo('password', message='Şifreler eşleşmiyor')
    ])
    submit = SubmitField('Şifreyi Sıfırla') 