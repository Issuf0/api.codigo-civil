from datetime import datetime, timedelta, timezone
from flask import Flask,jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS

from db_config import db_config
from db import db
from blocklist import BLOCKLIST
import Models
from Models.Artigo import Artigo


from Controllers.EstadoController import blp as EstadoBlueprint
from Controllers.TipoUsuarioController import blp as TipoUsuarioBlueprint
from Controllers.UsuarioController import blp as UsuarioBlueprint
from Controllers.ChatbotController import blp as ChatbotBlueprint
# def create_app(db_url=None):

app = Flask(__name__)

CORS(app)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Gestor de Processos Rest API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
# Use the SQLAlchemy URI provided by db_config (explicit single source)
app.config["SQLALCHEMY_DATABASE_URI"] = db_config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

migrate = Migrate(app, db)

api = Api(app)

app.config["JWT_SECRET_KEY"] = "ACSUN"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=10)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "description": "The token is not fresh.",
                "error": "fresh_token_required",
            }
        ),
        401
    )


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "O token expirou.", "error": "token_expired"}),
        401,
    )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify({"message": "Signature verification failed.", "error": "invalid_token"}),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
            ),
        401,
    )


@app.before_first_request
def create_tables():
    db.create_all()

api.register_blueprint(EstadoBlueprint)
api.register_blueprint(TipoUsuarioBlueprint)
api.register_blueprint(UsuarioBlueprint)
api.register_blueprint(ChatbotBlueprint)