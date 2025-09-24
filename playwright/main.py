import os
import sys

# Adiciona o diretório raiz ao path do Python para garantir que os módulos sejam encontrados
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# --- Importação segura dos scripts de cada exercício ---
# try/except para funcionar mesmo que eu apague algum 
try:
    from exercicio1.main import youtube_search_and_screenshot_v3
    EX1 = youtube_search_and_screenshot_v3
except ImportError:
    EX1 = None

try:
    from exercicio2.main import scrape_quotes
    EX2 = scrape_quotes
except ImportError:
    EX2 = None

try:
    from exercicio3.main import automate_login_and_save_result
    EX3 = automate_login_and_save_result
except ImportError:
    EX3 = None

try:
    from exercicio4.main import scrape_mercado_livre_challenge_v2
    EX4 = scrape_mercado_livre_challenge_v2
except ImportError:
    EX4 = None

# --- Dicionário para mapear opções do menu às funções ---
EXERCISES = {
    '1': {'func': EX1, 'desc': "Exercício 1: Pesquisa no YouTube e Screenshot"},
    '2': {'func': EX2, 'desc': "Exercício 2: Scraping de Citações (Quotes to Scrape)"},
    '3': {'func': EX3, 'desc': "Exercício 3: Login Automático e Validação"},
    '4': {'func': EX4, 'desc': "Exercício 4: Scraping do Mercado Livre (Desafio)"},
}

def show_menu():
    """Exibe o menu de opções formatado."""
    print("\n" + "="*50)
    print(" " * 15 + "MENU DE EXERCÍCIOS")
    print("="*50)
    
    for key, value in EXERCISES.items():
        # Mostra o exercício e um aviso se o script não for encontrado
        status = "" if value['func'] else " (Script não encontrado)"
        print(f"  [{key}] - {value['desc']}{status}")
        
    print("\n  [5] - Executar TODOS os exercícios em sequência")
    print("  [0] - Sair")
    print("="*50)


def run_all():
    """Executa todos os exercícios disponíveis em sequência."""
    print("\n--- INICIANDO EXECUÇÃO DE TODOS OS EXERCÍCIOS ---\n")
    all_found = True
    for key, value in EXERCISES.items():
        if value['func']:
            try:
                print(f"\n>>> Executando: {value['desc']} <<<\n")
                value['func']()
                print(f"\n>>> {value['desc']} finalizado. <<<\n")
            except Exception as e:
                print(f"\n!!! Ocorreu um erro ao executar o Exercício {key}: {e} !!!\n")
        else:
            all_found = False
            print(f"--- Pulando Exercício {key} (não encontrado) ---")
    
    if not all_found:
        print("\nAlguns scripts não foram encontrados e foram pulados.")
    print("\n--- EXECUÇÃO DE TODOS OS EXERCÍCIOS FINALIZADA ---\n")


def main():
    """Função principal que gerencia o loop do menu."""
    while True:
        show_menu()
        choice = input("Escolha uma opção e pressione Enter: ")

        if choice == '0':
            print("Saindo do programa. Até mais!")
            break
        
        elif choice == '5':
            run_all()
        
        elif choice in EXERCISES:
            exercise = EXERCISES[choice]
            if exercise['func']:
                try:
                    print(f"\n>>> Executando: {exercise['desc']} <<<\n")
                    exercise['func']()
                    print(f"\n>>> {exercise['desc']} finalizado. <<<\n")
                except Exception as e:
                    print(f"\n!!! Ocorreu um erro durante a execução: {e} !!!\n")
            else:
                print(f"\nErro: O script para o Exercício {choice} não foi encontrado.")
                print("Verifique se o arquivo 'exercicio{choice}/main.py' existe e não contém erros.")
        
        else:
            print("\nOpção inválida. Por favor, tente novamente.")
        
        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()