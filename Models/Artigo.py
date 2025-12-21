from db import db

class Artigo(db.Model):
    __tablename__ = 'artigos'

    id = db.Column(db.Integer, primary_key=True)
    capitulo_id = db.Column(db.Integer, nullable=True)
    artigo = db.Column(db.String(255), nullable=False)
    corpo = db.Column(db.Text, nullable=True)

    def __init__(self, capitulo_id, artigo, corpo):
        self.capitulo_id = capitulo_id
        self.artigo = artigo
        self.corpo = corpo
