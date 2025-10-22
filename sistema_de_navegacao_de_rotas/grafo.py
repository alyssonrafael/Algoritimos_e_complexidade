import collections
import heapq # Fila de prioridade para Dijkstra

class Graph:
    """
    Implementação de um Grafo direcionado e ponderado.
    """
    
    def __init__(self):
        self.adj = collections.defaultdict(dict)
        self.nodes = set()

    def add_node(self, node_name):
        self.nodes.add(node_name)
        _ = self.adj[node_name] 

    def add_edge(self, u, v, weight):
        """Adiciona uma aresta ponderada (rua) de u para v."""
        self.add_node(u) # Garante que nós existam
        self.add_node(v)
        
        
        # (Mão-dupla) nso dígrafo:
        self.adj[u][v] = weight
        self.adj[v][u] = weight

    def get_neighbors(self, u):
        return self.adj[u]

    def bfs(self, start_node):
        if start_node not in self.nodes:
            return []
        visited = set()
        queue = collections.deque([start_node])
        visited.add(start_node)
        traversal_order = []
        
        while queue:
            current_node = queue.popleft()
            traversal_order.append(current_node)
            for neighbor in self.adj[current_node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return traversal_order

    def dfs(self, start_node):
        if start_node not in self.nodes:
            return []
        visited = set()
        stack = [start_node]
        traversal_order = []
        
        while stack:
            current_node = stack.pop()
            if current_node not in visited:
                visited.add(current_node)
                traversal_order.append(current_node)
                for neighbor in reversed(list(self.adj[current_node].keys())):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return traversal_order

    def dijkstra(self, start_node):
        if start_node not in self.nodes:
            return {}, {}
        dist = {node: float('inf') for node in self.nodes}
        prev = {node: None for node in self.nodes}
        dist[start_node] = 0
        pq = [(0, start_node)]
        
        while pq:
            current_dist, current_node = heapq.heappop(pq)
            if current_dist > dist[current_node]:
                continue
            for neighbor, weight in self.adj[current_node].items():
                new_dist = current_dist + weight
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = current_node
                    heapq.heappush(pq, (new_dist, neighbor))
        return dist, prev

    def get_shortest_path(self, start_node, end_node):
        distances, previous_nodes = self.dijkstra(start_node)
        path = []
        current = end_node
        if distances[end_node] == float('inf'):
            return None
        while current is not None:
            path.append(current)
            current = previous_nodes.get(current)
        return path[::-1]
    
    def remove_node(self, node_to_remove):
        """
        Remove um nó (bairro) e todas as arestas (ruas) 
        conectadas a ele (entrada e saída).
        
        Complexidade: O(V) para esta implementação (dict de dicts),
        pois precisamos varrer todos os outros vértices para 
        remover as arestas de *entrada*.
        """
        if node_to_remove not in self.nodes:
            return

        # 1. Remove o nó da lista de nós
        self.nodes.remove(node_to_remove)

        # 2. Remove todas as arestas que 'saem' do nó
        if node_to_remove in self.adj:
            del self.adj[node_to_remove]

        # 3. Remove todas as arestas que 'entram' no nó
        # (Itera sobre uma cópia das chaves para poder modificar o dict)
        for node in list(self.adj.keys()):
            if node_to_remove in self.adj[node]:
                del self.adj[node][node_to_remove]