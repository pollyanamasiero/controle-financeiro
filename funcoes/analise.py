import pandas as pd
from funcoes.banco import conectar

def analisar_dados():
        
    conexao = conectar()
    
    df = pd.read_sql_query(
        "SELECT * FROM transacoes",
        conexao
    )
    
    conexao.close()
    
    if df.empty:
        print("Sem dados para análise.")
        return
    
    df["valor"] = pd.to_numeric(df["valor"])
    df["tipo"] = df["tipo"].str.strip().str.lower()
    
    receitas = df[df["tipo"] == "receita"]["valor"].sum()
    despesas = df[df["tipo"] == "despesa"]["valor"].sum()
    saldo = receitas - despesas
    
    print("\n--- ANÁLISE FINANCEIRA ---")
    print(f"Total de receitas: R$ {receitas:.2f}")
    print(f"Total de despesas: R$ {despesas:.2f}")
    print(f"Saldo final: R$ {saldo:.2f}")
    
    print("\nGastos por categoria:")
    gastos_categoria = df[df["tipo"] == "despesa"].groupby("categoria")["valor"].sum()
    
    for categoria, valor in gastos_categoria.items():
        print(f"- {categoria}: R$ {valor:.2f}")