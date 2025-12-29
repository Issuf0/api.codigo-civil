from app import app
from Models.AccessCode import AccessCode
from datetime import datetime

def sync_file():
    marker = "--- CÓDIGOS DE ACESSO (PREMIUM) ---" 
    
    with app.app_context():
        # 1. Fetch valid codes from DB
        valid_codes = AccessCode.query.filter(
            AccessCode.is_used == False,
            AccessCode.is_active == True,
            AccessCode.expires_at > datetime.utcnow()
        ).all()
        
        codes_list = [c.code for c in valid_codes]
        print(f"Encontrados {len(codes_list)} códigos válidos no banco de dados.")

        # 2. Read current file content
        try:
            with open("chatbot_questions.txt", "r") as f:
                content = f.read()
        except FileNotFoundError:
            content = ""

        # 3. Split content to preserve questions
        if marker in content:
            # Keep everything before the marker
            clean_content = content.split(marker)[0].rstrip()
        else:
            # If marker not found, keep everything (assuming it's just questions)
            clean_content = content.rstrip()

        # 4. Write new content
        with open("chatbot_questions.txt", "w") as f:
            f.write(clean_content)
            f.write("\n\n")
            f.write(marker)
            f.write("\n")
            f.write("IMPORTANTE: Estes códigos são de USO ÚNICO e válidos por 30 DIAS.\n")
            f.write("Use um destes códigos no campo 'access_code' da sua requisição:\n")
            f.write("\n")
            
            for code in codes_list:
                f.write(f"{code}\n")
        
        print("Arquivo 'chatbot_questions.txt' atualizado com sucesso!")

if __name__ == "__main__":
    sync_file()
