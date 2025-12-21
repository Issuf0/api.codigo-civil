from db import db
class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(255), nullable=False, index=True)
    type = db.Column(db.String(45), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    # Relationship
    user = db.relationship("Usuario", back_populates="token_user", cascade="all, delete")

    def __init__(self,jti,type,user_id):
        self.jti = jti
        self.type = type
        self.user_id = user_id
       
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    

    def format(self):
        return {
            "id": self.id,
            "jti": self.jti,
            "type": self.type,
            "user": self.user.format(),
            "created_at": self.created_at.strftime("%d-%m-%Y %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%d-%m-%Y %H:%M:%S")
        }
