from db import db

class Estado(db.Model):
    __tablename__ = "estados"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.Enum('1', '0'), unique=False, nullable=False, default='1')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    
    tipo_usuario_estado = db.relationship('TipoUsuario', back_populates='estados')
    usuario_estado = db.relationship('Usuario', back_populates='estados')

    
    def __init__(self,descricao):
        self.descricao = descricao
       
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self,descricao):
        self.descricao = descricao
        db.session.add(self)
        db.session.commit()

    def delete(self,estado):
        self.estado = estado
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "estado": self.estado,
            "created_at": self.created_at.strftime("%d-%m-%Y %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%d-%m-%Y %H:%M:%S")
        }
