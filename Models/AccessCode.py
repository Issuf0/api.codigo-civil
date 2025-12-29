from db import db
from datetime import datetime, timedelta

class AccessCode(db.Model):
    __tablename__ = 'access_codes'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, code, is_active=True, validity_days=30):
        self.code = code
        self.is_active = is_active
        self.is_used = False
        self.created_at = datetime.utcnow()
        self.expires_at = self.created_at + timedelta(days=validity_days)
