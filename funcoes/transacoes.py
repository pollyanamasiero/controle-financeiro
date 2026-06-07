from datetime import datetime
from funcoes.banco import conectar

def carregar_transacoes_db():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT tipo, valor, categoria, data
        FROM transacoes
    """)
    
    dados = cursor.fetchall()
    
    conexao.close()
    
    return dados
    
        
def ver_saldo():
    
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT tipo, valor
        FROM transacoes
    """)
    
    transacoes = cursor.fetchall()
    
    conexao.close()
    
    saldo = 0
    
    for tipo, valor in transacoes:
        if tipo == "receita":
            saldo += valor
        else:
            saldo -= valor
            
    print(f"Saldo atual: R$ {saldo:.2f}")
    
    
def listar_transacoes():
    dados = carregar_transacoes_db()
    
    if not dados:
        print("Nenhuma transação encontrada.")
        return
    
    print("\n--- TRANSAÇÕES ---")
    
    for i, t in enumerate(dados, start=1):
        tipo = t[0].capitalize()
        valor = f"R$ {float(t[1]):.2f}"
        categoria = t[2]
        data = t[3]
        
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
    
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        INSERT INTO transacoes
        (tipo, valor, categoria, data)
        VALUES (?, ?, ?, ?)
    """, (tipo, valor, categoria, data))

    conexao.commit()
    conexao.close()
    
    print("Transação salva!")
    
    
def remover_transacao():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT id, tipo, valor, categoria, data
        FROM transacoes
    """)
    
    dados = cursor.fetchall()
    
    if not dados:
        print("Nenhuma transação encontrada.")
        conexao.close()
        return
    
    print("\n--- TRANSAÇÕES ---")
    
    for i, t in enumerate(dados, start=1):
        print(f"{i}. [{t[1].capitalize()}] R$ {float(t[2]):.2f} | {t[3]} | {t[4]}")
        
    try:
        indice = int(input("\nDigite o número da transação que deseja remover: "))
        
        if 1 <= indice <= len(dados):
            
            id_transacao = dados[indice - 1][0]
            
            cursor.execute("""
                DELETE FROM transacoes
                WHERE id = ?
            """, (id_transacao,))
            
            conexao.commit()
            
            print("\nTransação removida com sucesso!")
                        
        else:
            print('Número inválido.')
            
    except ValueError:
        print("Digite um número válido")
        
    conexao.close()
        
def editar_transacao():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, tipo, valor, categoria, data
        FROM transacoes
    """)

    dados = cursor.fetchall()

    if not dados:
        print("Nenhuma transação encontrada")
        conexao.close()
        return

    print("\n--- TRANSAÇÕES ---")

    for i, t in enumerate(dados, start=1):
        print(
            f"{i}. [{t[1].capitalize()}] "
            f"R$ {float(t[2]):.2f} | "
            f"{t[3]} | {t[4]}"
        )

    try:
        indice = int(input("\nDigite o número da transação que deseja editar: "))

        if 1 <= indice <= len(dados):

            transacao = dados[indice - 1]

            id_transacao = transacao[0]

            print("\nDeixe vazio para manter o valor atual.")

            novo_tipo = input(f"Tipo ({transacao[1]}): ").lower()
            novo_valor = input(f"Valor ({transacao[2]}): ")
            nova_categoria = input(f"Categoria ({transacao[3]}): ").title()
            nova_data = input(f"Data ({transacao[4]}): ")

            tipo = novo_tipo if novo_tipo else transacao[1]
            valor = float(novo_valor) if novo_valor else transacao[2]
            categoria = nova_categoria if nova_categoria else transacao[3]
            data = nova_data if nova_data else transacao[4]

            cursor.execute("""
                UPDATE transacoes
                SET tipo = ?,
                    valor = ?,
                    categoria = ?,
                    data = ?
                WHERE id = ?
            """, (tipo, valor, categoria, data, id_transacao))

            conexao.commit()

            print("\nTransação atualizada com sucesso!")

        else:
            print("Número inválido.")

    except ValueError:
        print("Digite um número válido.")

    conexao.close()
        
