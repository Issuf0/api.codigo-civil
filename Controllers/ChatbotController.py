from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from Services.ChatbotService import ChatbotService

blp = Blueprint("chatbot", __name__, description="Chatbot operations")

@blp.route("/api/chatbot")
class Chatbot(MethodView):
    def post(self):
        query = request.json.get("query")
        if not query:
            abort(400, message="Query cannot be empty.")

        chatbot_service = ChatbotService()
        response = chatbot_service.chatbot_query(query)
        return response
