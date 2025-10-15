# Importa as funções dos outros arquivos
from complexidade_o1 import obter_primeiro_elemento
from complexidade_on import busca_linear
from complexidade_on2 import bubble_sort

def exibir_menu():
    """Exibe as opções do menu para o usuário."""
    print("\n--- MENU DE ALGORITMOS DE COMPLEXIDADE ---")
    print("Escolha qual algoritmo você deseja executar:")
    print("1. Algoritmo O(1) - Obter Primeiro Elemento")
    print("2. Algoritmo O(n) - Busca Linear")
    print("3. Algoritmo O(n²) - Bubble Sort")
    print("4. Sair")
    print("------------------------------------------")

def main():
    """Função principal que gerencia a execução do menu."""
    lista_exemplo = [64, 34, 25, 12, 22, 11, 90, 5]

    while True:
        exibir_menu()
        escolha = input("Digite o número da sua opção: ")

        if escolha == '1':
            print("\nExecutando O(1): Obter Primeiro Elemento...")
            print(f"Lista de entrada: {lista_exemplo}")
            primeiro = obter_primeiro_elemento(lista_exemplo)
            print(f"Resultado: O primeiro elemento é {primeiro}.")
            
        elif escolha == '2':
            print("\nExecutando O(n): Busca Linear...")
            alvo = int(input("Digite o número que deseja buscar na lista " f"{lista_exemplo}" ": "))
            indice = busca_linear(lista_exemplo, alvo)
            if indice != -1:
                print(f"Resultado: O elemento {alvo} foi encontrado no índice {indice}.")
            else:
                print(f"Resultado: O elemento {alvo} não foi encontrado na lista.")

        elif escolha == '3':
            print("\nExecutando O(n²): Bubble Sort...")
            print(f"Lista de entrada (desordenada): {lista_exemplo}")
            ordenada = bubble_sort(lista_exemplo)
            print(f"Resultado: A lista ordenada é {ordenada}.")

        elif escolha == '4':
            print("Saindo do programa. Até logo!")
            break
            
        else:
            print("Opção inválida! Por favor, escolha um número de 1 a 4.")
        
        input("\nPressione Enter para continuar...")


# Garante que a função main() seja chamada quando o script for executado
if __name__ == "__main__":
    main()