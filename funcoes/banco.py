import sqlite3

def conectar():
    return sqlite3.connect("financeiro.db")

def criar_banco():
    conexao = conectar()
    
    cursor = conexao.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria TEXT NOT NULL,
            data TEXT NOT NULL
        )
    """)
    
    conexao.commit()
    conexao.close()
