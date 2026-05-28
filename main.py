import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

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
        data = input("Data (YYYY-MM-DD): ")
        
        try:
            datetime.strptime(data, "%Y-%m-%d")
            break
        except ValueError:
            print("Data inválida! Use o formato YYYY-MM-DD.")
            
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
        valor = f"R$ {float(t['valor']):.2f}"
        categoria = t["categoria"]
        data = t["data"]
        
        print(f"{i}. [{tipo}] {valor} | {categoria} | {data}")
        
def ver_saldo():
    dados = carregar_dados()
    saldo = 0
    
    for t in dados:
        if t["tipo"] == "receita":
            saldo += float(t["valor"])
        else:
            saldo -= float(t["valor"])
            
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
    dados = carregar_dados()
    
    if not dados:
        print("Sem dados para gerar gráfico.")
        return
    
    df = pd.DataFrame(dados)
    
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
    
def remover_transacao():
    dados = carregar_dados()
    
    if not dados:
        print("Nenhuma transação encontrada.") 
        return
    
    print("\n--- TRANSAÇÕES ---")
    
    for i, t in enumerate(dados, start=1):
        print(f"{i}. [{t['tipo'].capitalize()}] R$ {float(t['valor']):.2f} | {t['categoria']} | {t['data']}")
        
    try:
        indice = int(input("\nDigite o número da transação que deseja remover: "))    
        
        if 1 <= indice <= len(dados):
            removida = dados.pop(indice - 1)
            salvar_dados(dados)
            
            print("\nTransação removida com sucesso!")
            print(f"Removido: {removida['categoria']} - R$ {float(removida['valor']):.2f}")
            
        else:
            print('Número inválido.')
            
    except ValueError:
        print("Digite um número válido.")
        
def editar_transacao():
    dados = carregar_dados()
    
    if not dados:
        print('Nenhuma transação encontrada')
        return
    print('\n--- TRANSAÇÕES ---')
    
    for i, t in enumerate(dados, start=1):
        print(f"{i}. [{t['tipo'].capitalize()}] R$ {float(t['valor']):.2f} | {t['categoria']} | {t['data']}")
        
    try:
        indice = int(input("\nDigite o número da transação que deseja editar: "))
        
        if 1 <= indice <= len(dados):
            
            transacao = dados[indice - 1]
            
            print("\nDeixe vazio para manter o valor atual.")
            
            novo_tipo = input(f"Tipo ({transacao['tipo']}): ").lower()
            novo_valor = input(f"Valor ({transacao['valor']}): ")
            nova_categoria = input(f"Categoria ({transacao['categoria']}): ").title()
            nova_data = input(f"Data ({transacao['data']}): ")
            
            if novo_tipo:
                transacao["tipo"] = novo_tipo
                
            if novo_valor:
                transacao["valor"] = float(novo_valor)
                
            if nova_categoria:
                transacao["categoria"] = nova_categoria
                
            if nova_data:
                transacao["data"] = nova_data
                
            salvar_dados(dados)
            
            print("\nTransação atualizada com sucesso!")
            
        else:
            print("Número inválido.")
            
    except ValueError:
        print("Digite um número válido.")
    
    
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
        print("8 - Remover transação")
        print("9 - Editar transação")
        print("10 - Sair")
        
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
            remover_transacao()
        elif opcao == "9":
            editar_transacao()
        elif opcao == "10":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")
menu()