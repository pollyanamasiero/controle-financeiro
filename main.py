from funcoes.analise import analisar_dados
from funcoes.transacoes import ver_saldo, listar_transacoes, adicionar_transacao, remover_transacao, editar_transacao, filtrar_transacoes, resumo_mensal, resumo_anual
from funcoes.graficos import grafico_gastos_categoria, grafico_receitas_despesas
from funcoes.exportacao import exportar_excel
from funcoes.banco import criar_banco

     
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
        print("10 - Filtrar transações por mês/ano")
        print("11 - Resumo mensal")
        print("12 - Relatório anual")
        print("13 - Sair")
        
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
            filtrar_transacoes()
        elif opcao == "11":
            resumo_mensal()
        elif opcao == "12":
            resumo_anual()
        elif opcao == "13":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")
            
criar_banco()      
menu()