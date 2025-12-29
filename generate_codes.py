import random
import string
from app import app
from db import db
from Models.AccessCode import AccessCode

def generate_code(length=8):
    """Gera um código alfanumérico aleatório."""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def main():
    with app.app_context():
        # Recria a tabela para garantir o esquema atualizado
        # ATENÇÃO: Isso apaga todos os dados da tabela access_codes!
        try:
            AccessCode.__table__.drop(db.engine)
            print("Tabela antiga removida.")
        except Exception:
            pass # Tabela pode não existir
            
        db.create_all()
        print("Nova tabela criada.")
        
        codes = set()
        while len(codes) < 100:
            codes.add(generate_code())
        
        codes_list = list(codes)
        
        # Salva no banco de dados
        try:
            for code in codes_list:
                # Cria com validade padrão de 30 dias
                new_access = AccessCode(code=code)
                db.session.add(new_access)
            
            db.session.commit()
            print(f"Sucesso: 100 códigos de acesso gerados e salvos no banco de dados.")
            
            # Adiciona ao arquivo de texto
            with open("chatbot_questions.txt", "a") as f:
                f.write("\n\n--- CÓDIGOS DE ACESSO (PREMIUM) ---\n")
                f.write("IMPORTANTE: Estes códigos são de USO ÚNICO e válidos por 30 DIAS.\n")
                f.write("Use um destes códigos no campo 'access_code' da sua requisição:\n")
                for i, code in enumerate(codes_list):
                    f.write(f"{code}\n")
            
            print("Sucesso: Códigos adicionados ao final de 'chatbot_questions.txt'.")
            
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar códigos: {e}")

if __name__ == "__main__":
    main()
