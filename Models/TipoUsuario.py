from db import db

class TipoUsuario(db.Model):
    __tablename__ = "tipo_usuario"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), unique=True, nullable=False)
    estado = db.Column(db.Integer, db.ForeignKey("estados.id"), unique=False, nullable=False, default=1)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    estados = db.relationship("Estado", back_populates="tipo_usuario_estado", cascade="all, delete")
    # Others Relationships
    usuario_tipo = db.relationship("Usuario", back_populates="tipo_usuario")

    def __init__(self,descricao):
        self.descricao = descricao
       
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self,tipo_usuario_data):
        self.descricao = tipo_usuario_data['descricao']
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
            "estado": self.estados.format(),
            "created_at": self.created_at.strftime("%d-%m-%Y %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%d-%m-%Y %H:%M:%S")
        }
