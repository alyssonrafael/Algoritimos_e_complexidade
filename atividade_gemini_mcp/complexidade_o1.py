# complexidade_o1.py

def obter_primeiro_elemento(lista: list) -> any:
    """
    Retorna o primeiro elemento de uma lista.

    Esta função demonstra a complexidade de tempo O(1) - Constante.
    A operação de acesso a um índice específico de uma lista (`lista[0]`)
    é direta e não depende do número total de elementos na lista.
    O tempo de execução é o mesmo para uma lista de qualquer tamanho.

    Args:
        lista (list): A lista da qual o primeiro elemento será retornado.

    Returns:
        any: O primeiro elemento da lista, ou None se a lista estiver vazia.
    """
    if not lista:
        return None
    return lista[0]

# --- Bloco de Teste ---
# Este código só será executado se o arquivo for rodado diretamente.
# Permite testar a função de forma isolada.
if __name__ == "__main__":
    print("--- Testando Algoritmo de Complexidade O(1) ---")
    
    lista_pequena = [10, 20, 30]
    print(f"Lista de entrada (pequena): {lista_pequena}")
    primeiro = obter_primeiro_elemento(lista_pequena)
    print(f"Primeiro elemento retornado: {primeiro}\n")

    lista_grande = list(range(10000))
    print(f"Lista de entrada (grande): com {len(lista_grande)} elementos")
    primeiro = obter_primeiro_elemento(lista_grande)
    print(f"Primeiro elemento retornado: {primeiro}\n")
    
    lista_vazia = []
    print(f"Lista de entrada (vazia): {lista_vazia}")
    primeiro = obter_primeiro_elemento(lista_vazia)
    print(f"Primeiro elemento retornado: {primeiro}")