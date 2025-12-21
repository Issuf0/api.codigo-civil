
import sqlite3
import re
import os

DB_FILE = "chatbot.db"
SQL_FILE = "chatbot (2).sql"

def clean_sql(sql_content):
    # Remove comments and unsupported commands
    sql_content = re.sub(r'--.*', '', sql_content)
    sql_content = re.sub(r'SET .*;', '', sql_content)
    sql_content = re.sub(r'/\*!.*?\*/;', '', sql_content, flags=re.DOTALL)
    sql_content = re.sub(r'START TRANSACTION;', '', sql_content)
    sql_content = re.sub(r'COMMIT;', '', sql_content)
    
    # Remove engine/charset/collate specifications
    sql_content = re.sub(r'ENGINE=InnoDB.*?;', ';', sql_content)
    
    # Replace backticks with nothing (or double quotes if needed, but often not necessary in SQLite)
    sql_content = sql_content.replace('`', '')
    
    # Split into individual statements
    statements = [s.strip() for s in sql_content.split(';') if s.strip()]
    
    return statements

def setup_database():
    if os.path.exists(DB_FILE):
        print(f"O arquivo de banco de dados '{DB_FILE}' já existe. Removendo para recriar.")
        os.remove(DB_FILE)

    try:
        with open(SQL_FILE, 'r', encoding='utf-8') as f:
            sql_content = f.read()
    except UnicodeDecodeError:
        with open(SQL_FILE, 'r', encoding='latin-1') as f:
            sql_content = f.read()

    cleaned_statements = clean_sql(sql_content)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    print("Criando e populando o banco de dados...")
    for statement in cleaned_statements:
        try:
            # SQLite doesn't support inserting into multiple tables in one statement like some dumps do.
            # This dump seems to have separate INSERTs, but this is a good practice.
            if statement.upper().startswith('INSERT INTO'):
                # The dump file has multiple VALUES clauses per INSERT, which is fine for SQLite
                cursor.execute(statement)
            elif statement.upper().startswith('CREATE TABLE'):
                cursor.execute(statement)
            # Ignore other statements like DROP, etc.
        except sqlite3.OperationalError as e:
            print(f"Erro ao executar o comando: {statement[:100]}...")
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Um erro inesperado ocorreu: {e}")


    conn.commit()
    conn.close()
    print("Banco de dados configurado com sucesso.")

if __name__ == "__main__":
    setup_database()
