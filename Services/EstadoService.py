from flask import request, jsonify, json
from flask_smorest import abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from Models import Estado

class EstadoService():

    def getAll():
        return jsonify({"data":list(map(Estado.format,Estado.query.all())),"success":True})

    def getOne(estado_id):
        estado = Estado.query.filter(Estado.id==estado_id).first_or_404()

        data = {
            "id": estado.id,
            "descricao": estado.descricao,
            "estado": estado.estado,
            "created_at": estado.created_at.strftime("%d-%m-%Y %H:%M:%S"),
            "updated_at": estado.updated_at.strftime("%d-%m-%Y %H:%M:%S")
        }
        return jsonify(data) 

    def post(estado_data):
        try:
            estado = Estado(**estado_data)
            estado.insert()
            return jsonify({"data":{"id": estado.id}, "message": "Estado registado com sucesso."}), 201
        except Exception as ex:
            abort(
                500,
                message=f"Ocorreu um erro ao registar o estado. {str(ex)}",
            )

    def update(estado_id, estado_data):
        try:
            estado = Estado.query.filter(Estado.id==estado_id).first_or_404()
            estado.update(estado_data['descricao'])
            return jsonify({"data":{"id": estado.id}, "message": "Estado actualizado com sucesso."}), 200
        except Exception as ex:
            abort(
                500,
                message=f"Ocorreu um erro ao actualizar o estado. {str(ex)}",
            )

    def delete(estado_id):
        try:
            estado = Estado.query.filter(Estado.id==estado_id).first_or_404()
            estado.delete('0')
            return jsonify({"data":{"id": estado.id}, "message": "Estado eliminado com sucesso."}), 200
        except Exception as ex:
            abort(
                500,
                message=f"Ocorreu um erro ao eliminar o estado. {str(ex)}",
            )