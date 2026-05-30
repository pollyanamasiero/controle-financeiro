import pandas as pd
from funcoes.transacoes import carregar_dados


def exportar_excel():
    dados = carregar_dados()
    
    if not dados:
        print("Sem dados para exportar.")
        return
    
    df = pd.DataFrame(dados)
    df.to_excel("transacoes.xlsx", index=False)
    
    print("Arquivo Excel gerado com sucesso!")    