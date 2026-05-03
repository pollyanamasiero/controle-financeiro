import json

ARQUIVO = "dados.json"

def carregar_dados():
    try:
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
def salvar_dados(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f, indent=4)
        
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
    for t in dados:
        print(t)
        
def ver_saldo():
    dados = carregar_dados()
    saldo = 0
    
    for t in dados:
        if t["tipo"] == "receita":
            saldo += t["valor"]
        else:
            saldo -= t["valor"]
            
    print(f"Saldo atual: {saldo}")
    
def menu():
    while True:
        print("\n1 - Adicionar")
        print("2 - Listar")
        print("3 - Ver saldo")
        print("4 - Sair")
        
        opcao = input("Escolha: ")
        
        if opcao == "1":
            adicionar_transacao()
        elif opcao == "2":
            listar_transacoes()
        elif opcao == "3":
            ver_saldo()
        elif opcao == "4":
            break
menu()