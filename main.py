import json
import pandas as pd

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
            
    categoria = input("Categoria: ")
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
    
def menu():
    while True:
        print("\n===== CONTROLE FINANCEIRO =====")
        print("1 - Adicionar transação")
        print("2 - Listar transações")
        print("3 - Ver saldo")
        print("4 - Exportar para Excel")
        print("5 - Sair")
        
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
            print("Saindo...")
            break
        else:
            print("Opção inválida!")
menu()