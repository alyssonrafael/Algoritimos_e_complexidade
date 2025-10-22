from arvore_avl import AVLTree
from grafo import Graph
import sys
import json          
import collections   
import os            

DB_FILE = "cities_db.json" # "banco de dados"

# Classe auxiliar
class City:
    def __init__(self, name, id_num, suppress_print=False):
        self.name = name
        self.id = id_num
        self.neighborhood_graph = Graph()
        if not suppress_print:
            print(f"-> Cidade '{self.name}' (ID: {self.id}) criada.")

#persistência

def save_data(avl_tree):
    """Salva todos os dados da árvore AVL em um arquivo JSON."""
    cities_list = avl_tree.get_all_nodes_data() # Lista de objetos City
    
    data_to_save = []
    for city in cities_list:
        data_to_save.append({
            "id": city.id,
            "name": city.name,
            "graph_nodes": list(city.neighborhood_graph.nodes),
            "graph_adj": city.neighborhood_graph.adj 
        })
    
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)
        print(f"\n[Sistema] Dados salvos com sucesso em {DB_FILE}")
    except Exception as e:
        print(f"\n[Sistema] Erro ao salvar dados: {e}")

def load_data():
    """Carrega os dados do JSON e reconstrói a árvore AVL."""
    new_tree = AVLTree()
    
    if not os.path.exists(DB_FILE):
        print(f"[Sistema] {DB_FILE} não encontrado. Começando com árvore vazia.")
        return new_tree

    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            data_loaded = json.load(f)
            
            if not isinstance(data_loaded, list):
                print(f"[Sistema] {DB_FILE} está corrompido. Começando com árvore vazia.")
                return new_tree

            for city_data in data_loaded:
                # 1. Recria a cidade (sem imprimir)
                city = City(city_data['name'], city_data['id'], suppress_print=True)
                
                # 2. Reconstrói o grafo
                city.neighborhood_graph.nodes = set(city_data.get('graph_nodes', []))
                # Recria o defaultdict a partir do dict salvo
                adj_data = city_data.get('graph_adj', {})
                # Correção para garantir que o defaultdict seja recriado corretamente
                rebuilt_adj = collections.defaultdict(dict)
                for node, neighbors in adj_data.items():
                    rebuilt_adj[node] = dict(neighbors)
                city.neighborhood_graph.adj = rebuilt_adj
                
                # 3. Insere na árvore
                new_tree.insert(city.id, city)
            
            print(f"\n[Sistema] {len(data_loaded)} cidades carregadas de {DB_FILE}.")
            return new_tree

    except json.JSONDecodeError:
        print(f"[Sistema] Erro ao decodificar {DB_FILE}. Começando com árvore vazia.")
        return new_tree
    except Exception as e:
        print(f"[Sistema] Erro ao carregar dados: {e}. Começando com árvore vazia.")
        return new_tree

# --- Funções de Complexidade ---
def show_complexity(operation, structure, complexity):
    print("\n--- Análise de Complexidade ---")
    print(f"Operação:   {operation}")
    print(f"Estrutura:  {structure}")
    print(f"Complexidade: {complexity}")
    print("---------------------------------")

# --- Sub-menu para Grafos ---
def explore_city_menu(city, avl_tree):
    """
    Gerencia o grafo de bairros.
    """
    g = city.neighborhood_graph
    
    while True:
        print(f"\n--- Gerenciando Bairros de '{city.name}' ---")
        print("1. Adicionar Bairro (Vértice)")
        print("2. Adicionar Rua (Aresta Ponderada)")
        print("3. Ver Bairros (BFS)")
        print("4. Ver Bairros (DFS)")
        print("5. Calcular Caminho Mínimo (Dijkstra)")
        print("6. Remover Bairro (Vértice)")  
        print("7. Voltar ao Menu Principal")
        
        choice = input("Escolha: ")
        
        if choice == '1':
            bairro = input("Nome do bairro: ")
            g.add_node(bairro)
            print(f"Bairro '{bairro}' adicionado.")
            show_complexity("Adicionar Vértice", "Grafo (Lista Adj.)", "O(1)")
            save_data(avl_tree)

        elif choice == '2':
            try:
                b1 = input("Bairro de origem: ")
                b2 = input("Bairro de destino: ")
                dist = int(input(f"Distância (peso) de {b1} para {b2}: "))
                g.add_edge(b1, b2, dist)
                g.add_edge(b2, b1, dist) 
                
                print(f"Rua adicionada: {b1} -> {b2} (Peso: {dist})")
                show_complexity("Adicionar Aresta", "Grafo (Lista Adj.)", "O(1)")
                save_data(avl_tree)
            except ValueError:
                print("Distância deve ser um número.")
                
        elif choice == '3':
            start = input("Bairro inicial para BFS: ")
            if start not in g.nodes:
                print(f"Erro: Bairro '{start}' não encontrado.")
                continue
            order = g.bfs(start)
            print(f"Ordem da visita (BFS): {order}")
            show_complexity("Busca em Largura", "Grafo", "O(V + E)")
            
        elif choice == '4':
            start = input("Bairro inicial para DFS: ")
            if start not in g.nodes:
                print(f"Erro: Bairro '{start}' não encontrado.")
                continue
            order = g.dfs(start)
            print(f"Ordem da visita (DFS): {order}")
            show_complexity("Busca em Profundidade", "Grafo", "O(V + E)")

        elif choice == '5':
            start = input("Bairro de origem: ")
            end = input("Bairro de destino: ")
            if start not in g.nodes or end not in g.nodes:
                print("Erro: Um ou ambos os bairros não existem.")
                continue
                
            dist, prev = g.dijkstra(start)
            path = g.get_shortest_path(start, end)
            
            if path:
                print(f"Caminho mais curto: {' -> '.join(path)}")
                print(f"Distância total: {dist[end]}")
            else:
                print(f"Não há caminho de '{start}' para '{end}'.")
            
            show_complexity("Caminho Mínimo", "Grafo (c/ Heap)", "O(E log V)")
            
        elif choice == '6':
            bairro = input("Nome do bairro a remover: ")
            if bairro not in g.nodes:
                print(f"Erro: Bairro '{bairro}' não encontrado.")
                continue
            
            g.remove_node(bairro)
            
            print(f"Bairro '{bairro}' e todas as suas conexões foram removidos.")
            show_complexity("Remover Vértice", "Grafo (Lista Adj.)", "O(V)")
            save_data(avl_tree)
            
        elif choice == '7':
            break
        else:
            print("Opção inválida.")

# --- Menu Principal ---
def main():
    # Carrega os dados do JSON ao invés de criar uma árvore vazia
    city_avl_tree = load_data() 
    
    while True:
        print("\n===== Sistema de Gestão de Cidades e Rotas =====")
        print("1. Cadastrar Cidade (Inserir na AVL)")
        print("2. Remover Cidade (Remover da AVL)")
        print("3. Buscar e Explorar Cidade (Buscar na AVL)")
        print("4. Listar Cidades (Percursos da AVL)")
        print("5. Sair")
        
        main_choice = input("Escolha uma opção: ")
        
        if main_choice == '1':
            try:
                name = input("Nome da cidade: ")
                city_id = int(input("ID da cidade (chave numérica): ")) 
                
                if city_avl_tree.search(city_id):
                    print(f"Erro: ID {city_id} já cadastrado.")
                else:
                    new_city = City(name, city_id) # Imprime "criada"
                    city_avl_tree.insert(city_id, new_city)
                    print(f"Cidade '{name}' inserida na árvore AVL.")
                    show_complexity("Inserção", "Árvore AVL", "O(log n)")
                    save_data(city_avl_tree) 
            except ValueError:
                print("Erro: ID deve ser um número.")

        elif main_choice == '2':
            try:
                city_id = int(input("ID da cidade a remover: "))
                node = city_avl_tree.search(city_id)
                if node:
                    city_avl_tree.remove(city_id)
                    print(f"Cidade (ID: {city_id}) removida.")
                    show_complexity("Remoção", "Árvore AVL", "O(log n)")
                    save_data(city_avl_tree) 
                else:
                    print(f"Erro: Cidade com ID {city_id} não encontrada.")
            except ValueError:
                print("Erro: ID deve ser um número.")

        elif main_choice == '3':
            try:
                city_id = int(input("ID da cidade para explorar: "))
                node = city_avl_tree.search(city_id)
                
                if node:
                    print(f"Cidade encontrada: {node.data.name}")
                    show_complexity("Busca", "Árvore AVL", "O(log n)")
                    # Passa a árvore para o sub-menu poder salvar
                    explore_city_menu(node.data, city_avl_tree)
                else:
                    print(f"Erro: Cidade com ID {city_id} não encontrada.")
                    show_complexity("Busca (Falha)", "Árvore AVL", "O(log n)")
            except ValueError:
                print("Erro: ID deve ser um número.")

        elif main_choice == '4':
            print("Escolha o percurso para listar os IDs das cidades:")
            print("  a. In-Ordem (Ordenado)")
            print("  b. Pré-Ordem")
            print("  c. Pós-Ordem")
            p_choice = input("Percurso: ").lower()
            
            result = []
            if p_choice == 'a':
                result = city_avl_tree.inorder_traversal()
            elif p_choice == 'b':
                result = city_avl_tree.preorder_traversal()
            elif p_choice == 'c':
                result = city_avl_tree.postorder_traversal()
            else:
                print("Opção de percurso inválida.")
                continue
                
            if not result:
                print("Nenhuma cidade cadastrada.")
            else:
                print(f"Resultado ({p_choice}): {result}")
            show_complexity("Percurso", "Árvore (AVL/BST)", "O(n)")

        elif main_choice == '5':
            # Salva uma última vez por garantia antes de sair
            save_data(city_avl_tree) 
            print("Saindo...")
            sys.exit()
            
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()