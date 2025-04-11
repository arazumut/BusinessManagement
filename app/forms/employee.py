from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError, Regexp
from app.models import Employee

class EmployeeForm(FlaskForm):
    """Çalışan ekleme/düzenleme formu"""
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
    tc_kimlik = StringField('TC Kimlik No', validators=[
        DataRequired(message='TC Kimlik No gerekli'),
        Regexp('^[0-9]{11}$', message='TC Kimlik No 11 haneli rakam olmalıdır')
    ])
    phone = StringField('Telefon', validators=[
        Optional(),
        Regexp('^[0-9+ ()-]{10,20}$', message='Geçerli bir telefon numarası girin')
    ])
    address = TextAreaField('Adres', validators=[Optional()])
    department_id = SelectField('Departman', coerce=int, validators=[Optional()])
    position_id = SelectField('Pozisyon', coerce=int, validators=[Optional()])
    salary = FloatField('Maaş', validators=[Optional()])
    hire_date = DateField('İşe Başlangıç Tarihi', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Kaydet')
    
    def validate_tc_kimlik(self, field):
        """TC Kimlik No benzersiz olmalı"""
        employee = Employee.query.filter_by(tc_kimlik=field.data).first()
        if employee and (not self.id.data or employee.id != int(self.id.data)):
            raise ValidationError('Bu TC Kimlik No zaten kullanılıyor. Lütfen kontrol edin.')
    
    def validate_email(self, field):
        """E-posta benzersiz olmalı"""
        from app.models import User
        user = User.query.filter_by(email=field.data).first()
        if user and (not self.id.data or (hasattr(user, 'employee_profile') and 
                                           user.employee_profile and 
                                           user.employee_profile.id != int(self.id.data))):
            raise ValidationError('Bu e-posta adresi zaten kullanılıyor. Lütfen başka bir tane deneyin.')

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        # id alanı formda görünmez, ancak güncelleme için kullanılır
        self.id = StringField('ID') 