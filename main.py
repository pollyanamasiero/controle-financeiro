import json
import pandas as pd
import matplotlib.pyplot as plt

ARQUIVO = "dados.json"


def carregar_dados():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
def salvar_dados(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
        
def adicionar_transacao():
    tipo = input("Digite o tipo (receita/despesa): ").lower()
    
    while tipo not in ["receita", "despesa"]:
        print("Tipo inválido!")
        tipo = input("Digite o tipo (receita/despesa): ").lower()
        
    while True:
        try:
            valor = float(input("Digite o valor: "))
            break
        except ValueError:
            print("Valor inválido! Digite um número.")
            
    categoria = input("Categoria: ").strip().title()
    data = input("Data (YYYY-MM-DD): ")
    
    dados = carregar_dados()
    
    dados.append({
        "tipo": tipo,
        "valor": valor,
        "categoria": categoria,
        "data": data
    })
    
    salvar_dados(dados)
    print("Transação salva!")
    
def listar_transacoes():
    dados = carregar_dados()
    
    if not dados:
        print("Nenhuma transação encontrada.")
        return
    
    print("\n--- TRANSAÇÕES ---")
    
    for i, t in enumerate(dados, start=1):
        tipo = t["tipo"].capitalize()
        valor = f"R$ {t['valor']:.2f}"
        categoria = t["categoria"]
        data = t["data"]
        
        print(f"{i}. [{tipo}] {valor} | {categoria} | {data}")
        
def ver_saldo():
    dados = carregar_dados()
    saldo = 0
    
    for t in dados:
        if t["tipo"] == "receita":
            saldo += t["valor"]
        else:
            saldo -= t["valor"]
            
    print(f"Saldo atual: {saldo:.2f}")
    
def exportar_excel():
    dados = carregar_dados()
    
    if not dados:
        print("Sem dados para exportar.")
        return
    
    df = pd.DataFrame(dados)
    df.to_excel("transacoes.xlsx", index=False)
    
    print("Arquivo Excel gerado com sucesso!")
    
def analisar_dados():
    dados = carregar_dados()
    
    if not dados:
        print("Sem dados para análise.")
        return
    
    df = pd.DataFrame(dados)
    
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
        
def grafico_gastos_categoria():
    dados = carregar_dados()
    
    if not dados:
        print("Sem dados para gerar gráfico.")
        return
    
    df = pd.DataFrame(dados)
    
    despesas = df[df["tipo"] == "despesa"]
    
    if despesas.empty:
        print("Sem despesas para analisar.")
        return
    
    gastos_categoria = despesas.groupby("categoria")["valor"].sum()
    
    plt.figure()
    plt.pie(gastos_categoria, labels=gastos_categoria.index, autopct='%1.1f%%')
    plt.title("Gastos por Categoria")
    
    plt.show()
    
def grafico_receitas_despesas():
    dados = carregar_dados()
    
    if not dados:
        print("Sem dados para gerar gráfico.")
        return
    
    df = pd.DataFrame(dados)
    
    df["tipo"] = df["tipo"].str.strip().str.lower()
    df["valor"] = pd.to_numeric(df["valor"])
    
    receitas = df[df["tipo"] == "receita"]["valor"].sum()
    despesas = df[df["tipo"] == "despesa"]["valor"].sum()
    
    print("Receitas:", receitas)
    print("Despesas:", despesas)
    
    categorias = ["Receitas", "Despesas"]
    valores = [receitas, despesas]
    
    plt.figure()
    plt.bar(categorias, valores)
    plt.title("Receitas vs Despesas")
    
    plt.show()
    
    
def menu():
    while True:
        print("\n===== CONTROLE FINANCEIRO =====")
        print("1 - Adicionar transação")
        print("2 - Listar transações")
        print("3 - Ver saldo")
        print("4 - Exportar para Excel")
        print("5 - Analisar dados")
        print("6 - Gráfico de gastos por categoria")
        print("7 - Gráfico receitas vs despesas")
        print("8 - Sair")
        
        opcao = input("Escolha: ")
        
        if opcao == "1":
            adicionar_transacao()
        elif opcao == "2":
            listar_transacoes()
        elif opcao == "3":
            ver_saldo()
        elif opcao == "4":
            exportar_excel()
        elif opcao == "5":
            analisar_dados()
        elif opcao == "6":
            grafico_gastos_categoria()
        elif opcao == "7":
            grafico_receitas_despesas()
        elif opcao == "8":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")
menu()