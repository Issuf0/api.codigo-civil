from marshmallow import Schema, fields

##########################################################################################################
#  PLAIN
##########################################################################################################

# Tipo de usuario
class PlainTipoUsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    descricao = fields.Str(required=True)



##########################################################################################################
#  SCHEMA
##########################################################################################################

# Estado
class EstadoSchema(Schema):
    id = fields.Int(dump_only=True)
    descricao = fields.Str(required=True)
    # user_id = fields.Int(required=False, default=None, allow_none=True)

# Delete Estado
class DeleteEstadoSchema(Schema):
    user_id = fields.Int(required=False, default=None, allow_none=True)


# Usuario
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    apelido = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    tipo_usuario_id = fields.Int(required=True)
    
# Usuario update
class UserUpdateSchema(Schema):
    nome = fields.Str(required=True)
    apelido = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    tipo_usuario_id = fields.Int(required=True)
    escola_id = fields.Int(required=True)
    user_id = fields.Int(required=False, default=None, allow_none=True)

class UserUpdateSenhaSchema(Schema):
    password = fields.Str(required=True)
    user_id = fields.Int(required=False, default=None, allow_none=True)

# Delete Usuario
class DeleteUserSchema(Schema):
    user_id = fields.Int(required=False, default=None, allow_none=True)



# Filtro de users
class FilterUserSchema(Schema):
    estado = fields.Str(required=False,default=None, allow_none=True)
    nome = fields.Str(required=False,default=None, allow_none=True)
    tipo_usuario_id = fields.Str(required=False,default=None, allow_none=True)
    page = fields.Int(required=False)
    escola_id = fields.Int(required=False)
    per_page = fields.Int(required=False)

# Tipo de usuario
class TipoUsuarioSchema(PlainTipoUsuarioSchema):
    estado = fields.Int(required=False)
    estados = fields.Nested(EstadoSchema(), dump_only=True)
    # user_id = fields.Int(required=False, default=None, allow_none=True)


# Delete Tipo de usuario
class DeleteTipoUsuarioSchema(Schema):
    user_id = fields.Int(required=False, default=None, allow_none=True)


# Login
class LoginSchema(Schema):
    email_username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

