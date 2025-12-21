from flask import request, jsonify, session
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from schemas import TipoUsuarioSchema
from Services import TipoUsuarioService
blp = Blueprint("Tipo de Usuário", __name__, description="Tipo de Usuário")

@blp.route("/tipo_usuario/<int:tipo_usuario_id>")
class TipoUsuarioController(MethodView):
    @jwt_required()
    def get(self,tipo_usuario_id):
        return TipoUsuarioService.getOne(tipo_usuario_id)

    @jwt_required()
    @blp.arguments(TipoUsuarioSchema)
    def put(self, tipo_usuario_data, tipo_usuario_id):
        return TipoUsuarioService.update(tipo_usuario_id,tipo_usuario_data)

    @jwt_required()
    def delete(self, tipo_usuario_id):
        return TipoUsuarioService.delete(tipo_usuario_id)

@blp.route("/tipo_usuario")
class TipoUsuarioController(MethodView):
    @jwt_required()
    def get(self):
        return TipoUsuarioService.getAll()

    @jwt_required()
    @blp.arguments(TipoUsuarioSchema)
    def post(self, tipo_usuario_data):
        # tipo_usuario_data['user_id'] = 1
        return TipoUsuarioService.post(tipo_usuario_data)