from flask import request, jsonify, json
from flask_smorest import abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from Models import TipoUsuario

class TipoUsuarioService():

    def getAll():
        return jsonify({"data":list(map(TipoUsuario.format,TipoUsuario.query.all())),"success":True})

    def getOne(tipo_usuario_id):
        tipo_usuario = TipoUsuario.query.filter(TipoUsuario.id==tipo_usuario_id).first_or_404()

        return jsonify(tipo_usuario.format()) 

    def post(tipo_usuario_data):
        try:
            tipo_usuario = TipoUsuario(**tipo_usuario_data)
            tipo_usuario.insert()
            return jsonify({"data":{"id": tipo_usuario.id}, "message": "Perfil registado com sucesso."}), 201
        except Exception as ex:
            abort(
                500,
                message=f"Ocorreu um erro ao registar o perfil. {str(ex)}",
            )

    def update(tipo_usuario_id, tipo_usuario_data):
        try:
            tipo_usuario = TipoUsuario.query.filter(TipoUsuario.id==tipo_usuario_id).first_or_404()
            tipo_usuario.update(tipo_usuario_data)
            return jsonify({"data":{"id": tipo_usuario.id}, "message": "Perfil actualizado com sucesso."}), 200
        except Exception as ex:
            abort(
                500,
                message=f"Ocorreu um erro ao actualizar o perfil. {str(ex)}",
            )

    def delete(tipo_usuario_id):
        try:
            tipo_usuario = TipoUsuario.query.filter(TipoUsuario.id==tipo_usuario_id).first_or_404()
            tipo_usuario.delete(2)
            return jsonify({"data":{"id": tipo_usuario.id}, "message": "Perfil eliminado com sucesso."}), 200
        except Exception as ex:
            abort(
                500,
                message=f"Ocorreu um erro ao eliminar o perfil. {str(ex)}",
            )