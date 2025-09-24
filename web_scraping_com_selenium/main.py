# Importa as funções principais de cada sub-módulo
from boot_login.main import run_login_and_extraction
from noticias.main import run_news_scraper

def show_menu():
    """Mostra o menu de opções para o usuário."""
    print("\n--- MENU DE AUTOMAÇÕES ---")
    print("Escolha a tarefa que deseja executar:")
    print("1. Executar Bot do Instagram (Login + Extração de Perfil)")
    print("2. Executar Coletor de Notícias do G1")
    print("0. Sair")
    print("--------------------------")

def main():
    """Função principal que gerencia a execução dos bots."""
    while True:
        show_menu()
        choice = input("Digite sua escolha: ")

        if choice == '1':
            print("\n>>> Iniciando o Bot do Instagram...")
            run_login_and_extraction()
            print(">>> Tarefa 'Bot do Instagram' finalizada.")
        
        elif choice == '2':
            print("\n>>> Iniciando o Coletor de Notícias...")
            run_news_scraper()
            print(">>> Tarefa 'Coletor de Notícias' finalizada.")

        elif choice == '0':
            print("Encerrando o programa. Até mais!")
            break
        
        else:
            print("\nOpção inválida! Por favor, tente novamente.")

if __name__ == "__main__":
    main()