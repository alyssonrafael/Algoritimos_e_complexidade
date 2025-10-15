# complexidade_on2.py

def bubble_sort(lista: list) -> list:
    """
    Ordena uma lista de números em ordem crescente usando o algoritmo Bubble Sort.

    Esta função demonstra a complexidade de tempo O(n²) - Quadrática.
    O algoritmo possui dois laços aninhados. O laço externo executa 'n' vezes
    e o laço interno também executa, em média, 'n' vezes. Isso resulta em
    n * n = n² operações de comparação no pior caso.

    Args:
        lista (list): A lista de números a ser ordenada.

    Returns:
        list: A lista ordenada.
    """
    n = len(lista)
    # Copia a lista para não modificar a original
    lista_ordenada = lista[:]
    
    # Percorre toda a lista
    for i in range(n):
        # O último i elementos já estão no lugar certo
        for j in range(0, n-i-1):
            # Percorre a lista de 0 a n-i-1
            # Troca se o elemento encontrado for maior que o próximo
            if lista_ordenada[j] > lista_ordenada[j+1]:
                lista_ordenada[j], lista_ordenada[j+1] = lista_ordenada[j+1], lista_ordenada[j]
                
    return lista_ordenada

# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Testando Algoritmo de Complexidade O(n²) ---")
    
    lista_desordenada = [64, 34, 25, 12, 22, 11, 90]
    print(f"Lista original (desordenada): {lista_desordenada}")
    
    lista_ordenada = bubble_sort(lista_desordenada)
    print(f"Lista ordenada: {lista_ordenada}")