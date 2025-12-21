import uuid
from flask import request, jsonify, json, session
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from blocklist import BLOCKLIST
from db import db
from Models import Usuario,TokenBlocklist
from Validations import Validation
import variables


class UsuarioService():

    def getAll(user_filters):
        filters = Usuario.query
        if Validation.nullOrEmpty(user_filters['estado']) is not None:
            filters = filters.filter(Usuario.estado == user_filters['estado'])

        if Validation.nullOrEmpty(user_filters['tipo_usuario_id']) is not None:
            filters = filters.filter(Usuario.tipo_usuario_id == user_filters['tipo_usuario_id'])
        if Validation.nullOrEmpty(user_filters['escola_id']) is not None:
            filters = filters.filter(Usuario.escola_id == user_filters['escola_id'])

        if Validation.nullOrEmpty(user_filters['nome']) is not None:
            filters = filters.filter(Usuario.nome.like(f"%{user_filters['nome']}%"))

        filters = filters.paginate(page=int(user_filters['page']), per_page=int(user_filters['per_page']))

        prev = "null"
        next = "null"
        if filters.prev_num != None:
            prev = f"{variables.url}user?page={filters.prev_num}"
        if filters.next_num != None:
            next = f"{variables.url}user?page={filters.next_num}"

        links = {
            "first": f"{variables.url}user?page=1",
            "last": f"{variables.url}user?page={filters.pages}",
            "prev": prev,
            "next": next
        }
        meta = {
            "current_page": filters.page,
            "last_page": filters.pages,
            "total": filters.total,
            "prev_page": filters.prev_num,
            "next_page": filters.next_num,
            "has_next": filters.has_next,
            "has_prev": filters.has_prev,
        }

        data = list(map(Usuario.format,filters))
                 
        return jsonify({"data":data, "links": links, "meta": meta})

    def getOne(usuario_id):
        user = Usuario.query.get_or_404(usuario_id,"Usuário não encontrado")
        return user.format(), 200

    def insert(usuario_data):
        if Usuario.query.filter(Usuario.username == usuario_data['username']).first():
            abort(409, message="Já existe um usuário com este username.")

        if Usuario.query.filter(Usuario.email == usuario_data['email']).first():
            abort(409, message="Já existe um usuário com este email.")
        try:
            usuario_data['password'] = pbkdf2_sha256.hash(usuario_data['password'])
            usuario = Usuario(**usuario_data)
            usuario.insert()
            return jsonify({"data":{"id": usuario.id}, "message": "Usuário registado com sucesso.", "code": 201}), 201
        except SQLAlchemyError as ex:
            db.session.rollback()
            abort(
                500,
                message=f"Ocorreu um erro ao registar o usuário. {str(ex)}",
            )

    def update(usuario_id, usuario_data):
        usuario = Usuario.query.get_or_404(usuario_id,"Usuário não encontrado")
        try:
            usuario.update(usuario_data)
            return jsonify({"data":{"id": usuario.id}, "message": "Usuário actualizado com sucesso.", "code": 200}), 200
        except Exception as ex:
            db.session.rollback()
            abort(
                500,
                message=f"Ocorreu um erro ao actualizar o usuário. {str(ex)}",
            )

    def delete(usuario_id):
        usuario = Usuario.query.get_or_404(usuario_id,"Usuário não encontrado")
        try:
            usuario.delete(2)
            return jsonify({"data":{"id": usuario.id}, "message": "Usuário eliminado com sucesso.", "code": 200}), 200
        except Exception as ex:
            db.session.rollback()
            abort(
                500,
                message=f"Ocorreu um erro ao eliminar o usuário. {str(ex)}",
            )

    def login(usuario_data):
        user = Usuario.query.filter(Usuario.email == usuario_data['email_username']).first() if Usuario.query.filter(Usuario.email == usuario_data['email_username']).first() is not None else Usuario.query.filter(Usuario.username == usuario_data['email_username']).first()
        if user: 
            if user.estado == 1:

                if pbkdf2_sha256.verify(usuario_data['password'], user.password):
                    
                    access_token = create_access_token(
                        identity=user.id, fresh=True)
                    refresh_token = create_refresh_token(identity=user.id)

                    session['usuario_id'] = user.id

                    return jsonify({"data": user.format(), "access_token": access_token, "refresh_token": refresh_token, "code": 200}),200
                else:
                    abort(401, message="Senha incorrecta. Por favor verifique seus dados e volte a tentar.")
            else:
                abort(401, message="Usuário inactivo. Por favor contacte o administrador do sistema para mais informações.")
        else:
            abort(401, message="Credencias inválidas. Por favor verifique seus dados de e volte a tentar.")


    def refresh_token():
        current_user = get_jwt_identity()
        token = get_jwt()
        jti = token["jti"]
        type = token["type"]
        token_blocklist = TokenBlocklist(jti=jti,type=type,usuario_id=current_user)
        token_blocklist.insert()
        new_token = create_access_token(identity=current_user, fresh=False)

        return {"access_token": new_token}
    
    def logout():
        current_user = get_jwt_identity()
        token = get_jwt()
        jti = token["jti"]
        type = token["type"]
        
        token_blocklist = TokenBlocklist(jti=jti,type=type,usuario_id=current_user)
        token_blocklist.insert()
        
        return jsonify(message=f"{type.capitalize()} token successfully revoked",success=True)
