import google.generativeai as genai
from flask import jsonify
from Models.Artigo import Artigo
from config import Config
from db import db
import re

class ChatbotService:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')

    def get_articles_by_keyword(self, keyword):
        articles = []
        # Try to extract an article number from the keyword
        match = re.search(r'(Art\.º|Artigo)\s*(\d+)', keyword, re.IGNORECASE)
        if match:
            article_number = match.group(2)
            # Search for exact article number match
            articles = Artigo.query.filter(Artigo.artigo.ilike(f'%Art.º {article_number}º%')).all()
            if not articles:
                articles = Artigo.query.filter(Artigo.artigo.ilike(f'%Artigo {article_number}%')).all()

        # If no specific article number match, or no article number extracted, perform a broader search
        if not articles:
            articles = Artigo.query.filter(
                (Artigo.artigo.ilike(f'%{keyword}%')) |
                (Artigo.corpo.ilike(f'%{keyword}%'))
            ).all()
        return articles

    def generate_response(self, prompt, articles):
        # Construct the prompt for the Gemini API
        article_text = ""
        if articles:
            article_text = "\n\nRelevant Articles:\n"
            for article in articles:
                article_text += f"Title: {article.artigo}\nContent: {article.corpo}\n\n"

        # full_prompt = f"Based on the following articles, answer the question: '{prompt}'. If the articles don't contain enough information, state that you don't have enough information.\n{article_text}"
        full_prompt = f"""
Você é um assistente amigável e educativo, especializado em explicar o Código Civil de Moçambique para cidadãos comuns.
Sua missão é traduzir a linguagem jurídica para uma linguagem simples, clara e fácil de entender.


CONTEXTO (ARTIGOS DO CÓDIGO CIVIL RECUPERADOS):
{article_text}

PERGUNTA DO USUÁRIO: "{prompt}"

COMO VOCÊ DEVE RESPONDER:
1. **Seja Humano e Didático**: Explique o assunto como se estivesse ensinando um amigo que não conhece leis. Evite termos técnicos difíceis ou, se usar, explique-os logo em seguida.
2. **Exemplos Hipotéticos**: Quando a pergunta for sobre o Código Civil e houver base nos artigos, utilize exemplos hipotéticos simples para facilitar a compreensão, sem criar novas regras.
3. **Situações Pessoais**: Se o usuário descrever uma situação pessoal, NÃO dê conselhos nem soluções práticas. Explique, em poucas palavras, quais matérias do Código Civil tratam dessa situação, com base exclusiva nos artigos fornecidos.
4. **Foco Total na Explicação**: Se a pessoa perguntar "O que é herança?", não responda apenas "O Artigo X diz Y". Responda: "Herança é o conjunto de bens... Isso acontece quando..." e depois cite o artigo no final.
5. **Use Somente o Contexto Fornecido**: Baseie sua resposta EXCLUSIVAMENTE nos artigos listados acima. Não invente informações.
6. **Sem Informação Suficiente**: Se os artigos acima não responderem à pergunta, diga de forma gentil: "Desculpe, mas não encontrei informações específicas sobre isso nos artigos do Código Civil que tenho acesso no momento."
7. **Cite a Fonte no Final**: Sempre mencione em qual artigo a informação está baseada (ex: "Isso está detalhado no Artigo [Número]").

OBJETIVO: Que o usuário saia da conversa entendendo perfeitamente o conceito ou a regra, de forma simples e humana.
"""




        # Interact with the Gemini API
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini API: {str(e)}"

    def chatbot_query(self, query):
        # First, try to find relevant articles
        relevant_articles = self.get_articles_by_keyword(query)

        # Then, generate a response using Gemini API
        response_text = self.generate_response(query, relevant_articles)

        return jsonify({"response": response_text})
