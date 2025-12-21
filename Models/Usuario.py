from db import db

class Usuario(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    apelido = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    tipo_usuario_id = db.Column(db.Integer, db.ForeignKey("tipo_usuario.id"), unique=False, nullable=False)
    estado = db.Column(db.Integer, db.ForeignKey("estados.id"), unique=False, nullable=False, default=1)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    # Relationship
    tipo_usuario = db.relationship("TipoUsuario", back_populates="usuario_tipo", cascade="all, delete")
    estados = db.relationship("Estado", back_populates="usuario_estado", cascade="all, delete")

    token_user = db.relationship("TokenBlocklist", back_populates="user")


    def __init__(self,nome,apelido,username,email, password, tipo_usuario_id):
        self.nome = nome
        self.apelido = apelido
        self.email = email
        self.username = username
        self.password = password
        self.tipo_usuario_id = tipo_usuario_id
       
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self,usuario_data):
        self.nome = usuario_data['nome']
        self.apelido = usuario_data['apelido']
        self.username = usuario_data['username']
        self.password = usuario_data['password']
        self.tipo_usuario_id = usuario_data['tipo_usuario_id']
        db.session.add(self)
        db.session.commit()
    
    def updateSenha(self,password):
        self.password = password
        db.session.add(self)
        db.session.commit()


    def delete(self,estado):
        self.estado = estado
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "apelido": self.apelido,
            "username": self.username,
            "email": self.email,
            "tipo_usuario": self.tipo_usuario.format(),
            "estado": self.estados.format(),
            "created_at": self.created_at.strftime("%d-%m-%Y %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%d-%m-%Y %H:%M:%S")
        }