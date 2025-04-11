from app import db
from datetime import datetime

# İzin türleri için sabitler
LEAVE_ANNUAL = 'yillik_izin'
LEAVE_SICK = 'hastalik_izni'
LEAVE_UNPAID = 'ucretsiz_izin'
LEAVE_MARRIAGE = 'evlilik_izni'
LEAVE_MATERNITY = 'dogum_izni'
LEAVE_PATERNITY = 'babalik_izni'
LEAVE_BEREAVEMENT = 'olum_izni'
LEAVE_OTHER = 'diger'

LEAVE_TYPES = [
    (LEAVE_ANNUAL, 'Yıllık İzin'),
    (LEAVE_SICK, 'Hastalık İzni'),
    (LEAVE_UNPAID, 'Ücretsiz İzin'),
    (LEAVE_MARRIAGE, 'Evlilik İzni'),
    (LEAVE_MATERNITY, 'Doğum İzni'),
    (LEAVE_PATERNITY, 'Babalık İzni'),
    (LEAVE_BEREAVEMENT, 'Ölüm İzni'),
    (LEAVE_OTHER, 'Diğer')
]

# İzin durumları için sabitler
LEAVE_STATUS_PENDING = 'beklemede'
LEAVE_STATUS_APPROVED = 'onaylandi'
LEAVE_STATUS_REJECTED = 'reddedildi'
LEAVE_STATUS_CANCELLED = 'iptal_edildi'

LEAVE_STATUSES = [
    (LEAVE_STATUS_PENDING, 'Beklemede'),
    (LEAVE_STATUS_APPROVED, 'Onaylandı'),
    (LEAVE_STATUS_REJECTED, 'Reddedildi'),
    (LEAVE_STATUS_CANCELLED, 'İptal Edildi')
]

class Leave(db.Model):
    """İzin modeli - Çalışan izinlerini temsil eder"""
    __tablename__ = 'leaves'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    leave_type = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default=LEAVE_STATUS_PENDING)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    review_date = db.Column(db.DateTime)
    review_comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    employee = db.relationship('Employee', back_populates='leaves')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])
    
    def __repr__(self):
        return f"<Leave {self.leave_type} for {self.employee.user.full_name}>" 