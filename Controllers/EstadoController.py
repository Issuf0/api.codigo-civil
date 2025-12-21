from flask import request, jsonify, session
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from schemas import EstadoSchema
from Services import EstadoService
blp = Blueprint("estado", __name__, description="estado")

@blp.route("/estado/<int:estado_id>")
class EstadoController(MethodView):
    @jwt_required()
    def get(self,estado_id):
        return EstadoService.getOne(estado_id)

    @jwt_required()
    @blp.arguments(EstadoSchema)
    def put(self, estado_data, estado_id):
        return EstadoService.update(estado_id,estado_data)

    @jwt_required()
    def delete(self, estado_id):
        return EstadoService.delete(estado_id)

@blp.route("/estado")
class EstadoController(MethodView):
    @jwt_required()
    def get(self):
        return EstadoService.getAll()

    @jwt_required()
    @blp.arguments(EstadoSchema)
    def post(self, estado_data):
        # estado_data['estado'] = '1'
        # estado_data['user_id'] = 1
        return EstadoService.post(estado_data)