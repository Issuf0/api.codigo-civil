import json
from flask import Flask, abort, Response
from flask_sqlalchemy import SQLAlchemy, BaseQuery

class CustomBaseQuery(BaseQuery):
    def get_or_404(self, ident,description:str=None):
        rv = self.get(ident)
        if not rv:
            if description is None:
                description="Not Found"
            error_message = json.dumps({'message':f'{description} com id {ident}','status':"Nao encontrado","code":404})
            abort(Response(error_message, 404))
        return rv
    
db = SQLAlchemy(query_class=CustomBaseQuery)