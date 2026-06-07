import pandas as pd
from funcoes.banco import conectar

def exportar_excel():
    conexao = conectar()

    df = pd.read_sql_query(
        "SELECT * FROM transacoes",
        conexao
    )

    conexao.close()

    if df.empty:
        print("Sem dados para exportar.")
        return

    df.to_excel("transacoes.xlsx", index=False)

    print("Arquivo Excel gerado com sucesso!")