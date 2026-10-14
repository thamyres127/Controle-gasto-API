import sqlite3
import pandas as pd

def executar_pipeline():
    print("🚀 Iniciando o Back-End de Limpeza de Dados...")
    
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT, telefone TEXT
    );
    """)
    conn.commit()
    
    df = pd.read_sql_query("SELECT * FROM clientes", conn)
    
    if df.empty:
        print("⚠️ O banco está vazio. Insira dados para testar!")
        return

    print(f"📊 Total de registros originais: {len(df)}")
    
    df = df.dropna(subset=['nome'])
    df = df[df['nome'] != '']
    df = df.drop_duplicates(subset=['nome'], keep='first')
    df = df[df['email'].str.contains('@', na=False)]
    df = df[df['telefone'].str.len() >= 10]

    print(f"✅ Dados higienizados! Registros válidos restantes: {len(df)}")
    
    df.to_sql('clientes_limpos', conn, if_exists='replace', index=False)
    
    conn.close()
    print("💾 Alterações salvas com sucesso em 'dados.db'.")

if __name__ == "__main__":
    executar_pipeline()
