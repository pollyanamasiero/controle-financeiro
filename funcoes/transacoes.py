import json
from datetime import datetime
from funcoes.banco import conectar

ARQUIVO = "dados.json"

def teste_banco():
    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO transacoes
        (tipo, valor, categoria, data)
        VALUES (?, ?, ?, ?)
    """, ("receita", 999.99, "Teste", "2026-06-03"))

    conexao.commit()
    conexao.close()

    print("Registro inserido!")
    

def carregar_dados():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
    
def salvar_dados(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
        
        
def ver_saldo():
    dados = carregar_dados()
    saldo = 0
    
    for t in dados:
        if t["tipo"] == "receita":
            saldo += float(t["valor"])
        else:
            saldo -= float(t["valor"])
            
    print(f"Saldo atual: {saldo:.2f}")
    
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
        
def adicionar_transacao():
    tipo = input("Digite o tipo (receita/despesa): ").lower()
    
    while tipo not in ["receita", "despesa"]:
        print("Tipo inválido!")
        tipo = input("digite o tipo (receita/despesa): ").lower()
        
    while True:
        try:
            valor = float(input("Digite um valor: R$ "))
            break
        except ValueError:
            print("Valor inválido! Digite um número.")
            
    while True:
        data = input("Data (YYYY-MM-DD): ")
        
        try:
            datetime.strptime(data, "%Y-%m-%d")
            break
        except ValueError:
            print("Data inválida! Use o formato YYYY-MM-DD.")
            
    categoria = input("Categoria: ").strip().title()
    
    # dados = carregar_dados()
    
    # dados.append({
    #     "tipo": tipo,
    #     "valor": valor,
    #     "categoria": categoria,
    #     "data": data
    # })
    
    conexao = conectar()
    
    cursor = conexao.cursor()
    
    cursor.execute("""
        INSERT INTO transacoes
        (tipo, valor, categoria, data)
        VALUES (?, ?, ?, ?)
    """, (tipo, valor, categoria, data))

    conexao.commit()
    conexao.close()
    
    # salvar_dados(dados)
    print("Transação salva!")
    
    
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
        print("Digite um número válido")
        
def editar_transacao():
    dados = carregar_dados()
    
    if not dados:
        print("Nenhuma transação encontrada")
        return
    
    print('\n--- TRANSAÇÕES ---')
    
    for i, t in enumerate(dados, start=1):
        print(f"{i}. [{t['tipo'].capitalize()}] R$ {float(t['valor']):.2f} | {t['categoria']} | {t['data']}")
        
    try:
        indice = int(input("\nDigite o número da transação que deseja editar: "))
        
        if 1 <= indice <= len(dados):
            
            transacao = dados[indice -1]
            
            print("\nDeixe vazio para manter o valor atual.")
            
            novo_tipo = input(f"Tipo ({transacao['tipo']}): ").lower()
            novo_valor = input(f"Valor ({transacao['valor']}): ")
            nova_categoria = input(f"Categoria ({transacao['categoria']}): ").title()
            nova_data = input(f"Data ({transacao['data']}): ")
            
            if novo_tipo:
                transacao['tipo'] = novo_tipo
                
            if novo_valor:
                transacao['valor'] = float(novo_valor)
                
            if nova_categoria:
                transacao['categoria'] = nova_categoria
                
            if nova_data:
                transacao['data'] = nova_data
                
            salvar_dados(dados)
            
            print('\nTransação atualizada com sucesso!')
            
        else:
            print('Número inválido.')
            
    except ValueError:
        print("Digite um número válido.")