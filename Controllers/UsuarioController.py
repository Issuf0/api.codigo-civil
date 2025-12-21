from flask import request, jsonify, session
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from schemas import UserSchema,UserUpdateSchema, UserUpdateSenhaSchema, FilterUserSchema, LoginSchema
from Services import UsuarioService

blp = Blueprint("Users", __name__, description="Users")


@blp.route("/user")
class UserController(MethodView):

    @jwt_required()
    @blp.arguments(FilterUserSchema)
    @blp.response(200, FilterUserSchema(many=True))
    def get(self, user_filters):
        return UsuarioService.getAll(user_filters)

    #Register user
    @jwt_required()
    @blp.arguments(UserSchema)
    def post(self, user_data):
        print(user_data)
        return UsuarioService.insert(user_data)


@blp.route("/user/<int:user_id>")
class UserController(MethodView):

    @jwt_required()
    def get(self, user_id):
        return UsuarioService.getOne(user_id)

    @jwt_required()
    def delete(self, user_id):
        return UsuarioService.delete(user_id)

    @jwt_required()
    @blp.arguments(UserUpdateSchema)
    def put(self, user_data, user_id):
        return UsuarioService.update(user_id, user_data)



@blp.route("/user-single/<int:user_id>")
class UserController(MethodView):
    @jwt_required()
    @blp.arguments(UserUpdateSenhaSchema)
    def put(self, user_data, user_id):
        return UsuarioService.update(user_id, user_data)


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, user_data):
        return UsuarioService.login(user_data)
        
@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        return UsuarioService.refresh_token()


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required(verify_type=False)
    def post(self):
        return UsuarioService.logout()
