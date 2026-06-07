import pandas as pd
import matplotlib.pyplot as plt
from funcoes.banco import conectar


def grafico_gastos_categoria():
    conexao = conectar()
    
    df = pd.read_sql_query(
        "SELECT * FROM transacoes",
        conexao
    )

    conexao.close()

    if df.empty:
        print("Sem dados para gerar gráfico.")
        return
    
    df["tipo"] = df["tipo"].str.strip().str.lower()
    
    despesas = df[df["tipo"] == "despesa"]
    
    if despesas.empty:
        print("Sem despesas para analisar.")
        return
    
    gastos_categoria = despesas.groupby("categoria")["valor"].sum()
    
    plt.figure()
    plt.pie(gastos_categoria, labels=gastos_categoria.index, autopct='%1.1f%%')
    plt.title("Gastos por Categoria")
    
    plt.savefig("grafico_gastos_categoria.png")
    print("Gráfico salvo como grafico_gastos_categoria.png")
    
    plt.show()
    
def grafico_receitas_despesas():
    conexao = conectar()
    
    df = pd.read_sql_query(
        "SELECT * FROM transacoes",
        conexao
    )

    conexao.close()

    if df.empty:
        print("Sem dados para gerar gráfico.")
        return
    
    df["tipo"] = df["tipo"].str.strip().str.lower()
    df["valor"] = pd.to_numeric(df["valor"])
    
    receitas = df[df["tipo"] == "receita"]["valor"].sum()
    despesas = df[df["tipo"] == "despesa"]["valor"].sum()
    
    categorias = ["Receitas", "Despesas"]
    valores = [receitas, despesas]
    
    plt.figure()
    plt.bar(categorias, valores)
    plt.title("Receitas vs Despesas")
    
    plt.savefig("grafico_receitas_despesas.png")
    print("Gráfico salvo como grafico_receitas_despesas.png")
    
    plt.show()