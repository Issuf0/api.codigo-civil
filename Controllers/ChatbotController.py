from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from Services.ChatbotService import ChatbotService
from Models.AccessCode import AccessCode
from db import db
from datetime import datetime

blp = Blueprint("chatbot", __name__, description="Chatbot operations")

@blp.route("/api/chatbot")
class Chatbot(MethodView):
    def post(self):
        # Access Code Verification
        access_code = request.json.get("access_code")
        if not access_code:
            abort(401, message="Access code is required.")
        
        valid_code = AccessCode.query.filter_by(code=access_code, is_active=True).first()
        
        if not valid_code:
            abort(403, message="Invalid access code.")
            
        if valid_code.expires_at < datetime.utcnow():
            abort(403, message="Access code has expired.")

        query = request.json.get("query")
        if not query:
            abort(400, message="Query cannot be empty.")

        chatbot_service = ChatbotService()
        response = chatbot_service.chatbot_query(query)
        return response
