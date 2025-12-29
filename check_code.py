from app import app
from Models.AccessCode import AccessCode
from datetime import datetime

def check_code(code_to_check):
    with app.app_context():
        code = AccessCode.query.filter_by(code=code_to_check).first()
        
        if not code:
            print(f"❌ Código '{code_to_check}' NÃO encontrado no banco de dados.")
            return

        print(f"🔍 Detalhes do Código: {code_to_check}")
        print(f"   - Existe no DB: Sim")
        print(f"   - Ativo (is_active): {code.is_active}")
        print(f"   - Usado (is_used): {code.is_used}")
        print(f"   - Criado em: {code.created_at}")
        print(f"   - Expira em: {code.expires_at}")
        print(f"   - Hora Atual (UTC): {datetime.utcnow()}")
        
        if code.is_used:
            print("\n⚠️  MOTIVO PROVÁVEL DO ERRO: O código já consta como USADO.")
            print("   (Lembre-se: configuramos para ser de uso único)")
        elif code.expires_at < datetime.utcnow():
            print("\n⚠️  MOTIVO PROVÁVEL DO ERRO: O código está EXPIRADO.")
        elif not code.is_active:
             print("\n⚠️  MOTIVO PROVÁVEL DO ERRO: O código está INATIVO.")
        else:
            print("\n✅ O código PARECE VÁLIDO. Se falhar, pode ser algo no Controller.")

if __name__ == "__main__":
    check_code("98A6WLVM")
