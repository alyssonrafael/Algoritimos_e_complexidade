# complexidade_on.py

def busca_linear(lista: list, alvo: any) -> int:
    """
    Procura por um elemento 'alvo' em uma lista e retorna seu índice.

    Esta função demonstra a complexidade de tempo O(n) - Linear.
    No pior caso, o algoritmo precisa percorrer todos os 'n' elementos da lista
    para encontrar o alvo ou determinar que ele não existe. O tempo de execução
    cresce linearmente com o tamanho da lista.

    Args:
        lista (list): A lista onde a busca será realizada.
        alvo (any): O elemento a ser encontrado.

    Returns:
        int: O índice do elemento 'alvo' se encontrado, caso contrário -1.
    """
    for indice, elemento in enumerate(lista):
        if elemento == alvo:
            return indice  # Retorna o índice assim que encontra o alvo
    return -1  # Retorna -1 se o loop terminar e o alvo não for encontrado

# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Testando Algoritmo de Complexidade O(n) ---")
    
    minha_lista = [45, 22, 14, 65, 87, 33, 91, 7]
    alvo_encontrado = 87
    alvo_nao_encontrado = 100

    print(f"Lista de entrada: {minha_lista}")
    
    # Teste 1: Alvo presente na lista
    print(f"Buscando pelo alvo: {alvo_encontrado}")
    indice = busca_linear(minha_lista, alvo_encontrado)
    if indice != -1:
        print(f"Elemento {alvo_encontrado} encontrado no índice: {indice}\n")
    else:
        print(f"Elemento {alvo_encontrado} não encontrado.\n")

    # Teste 2: Alvo não presente na lista
    print(f"Buscando pelo alvo: {alvo_nao_encontrado}")
    indice = busca_linear(minha_lista, alvo_nao_encontrado)
    if indice != -1:
        print(f"Elemento {alvo_nao_encontrado} encontrado no índice: {indice}")
    else:
        print(f"Elemento {alvo_nao_encontrado} não encontrado.")