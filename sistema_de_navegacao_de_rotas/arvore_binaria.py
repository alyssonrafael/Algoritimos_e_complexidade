class Node:
    """Nó básico de uma árvore."""
    def __init__(self, key, data=None):
        self.key = key
        self.data = data  # Dados associados (ex: objeto 'Cidade')
        self.left = None
        self.right = None

class BinarySearchTree:
    """
    Implementação de uma Árvore Binária de Busca (BST).
    
    Complexidade das Operações (Médio / Pior Caso):
    - Inserção: O(log n) / O(n)
    - Busca:    O(log n) / O(n)
    - Remoção:  O(log n) / O(n)
    - Percursos: O(n)
    Onde 'n' é o número de nós e 'h' (altura) é O(log n) no caso médio 
    e O(n) no pior caso (árvore degenerada).
    """
    def __init__(self):
        self.root = None

    def insert(self, key, data=None):
        """Insere novo nó na árvore. Complexidade: O(h)"""
        self.root = self._insert_recursive(self.root, key, data)

    def _insert_recursive(self, node, key, data):
        if node is None:
            return Node(key, data)
        
        if key < node.key:
            node.left = self._insert_recursive(node.left, key, data)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, data)
        else:
            # Chave já existe, atualiza os dados
            node.data = data
        return node

    def search(self, key):
        """Busca um nó pela chave. Complexidade: O(h)"""
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node
        
        if key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    def remove(self, key):
        """Remove um nó pela chave. Complexidade: O(h)"""
        self.root = self._remove_recursive(self.root, key)

    def _remove_recursive(self, node, key):
        if node is None:
            return node

        if key < node.key:
            node.left = self._remove_recursive(node.left, key)
        elif key > node.key:
            node.right = self._remove_recursive(node.right, key)
        else:
            # Nó encontrado Casos de remoção:
            # 1. Nó sem filhos (folha)
            if node.left is None and node.right is None:
                return None
            # 2. Nó com um filho
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # 3. Nó com dois filhos
            else:
                # Encontra o sucessor in-ordem (menor da subárvore direita)
                min_larger_node = self._find_min(node.right)
                node.key = min_larger_node.key
                node.data = min_larger_node.data
                # Remove o sucessor in-ordem da subárvore direita
                node.right = self._remove_recursive(node.right, min_larger_node.key)
        
        return node

    def _find_min(self, node):
        """Encontra o nó com a menor chave na subárvore dada."""
        current = node
        while current.left is not None:
            current = current.left
        return current

    # --- Percursos ---
    
    def inorder_traversal(self):
        """Retorna lista da travessia In-Ordem. Complexidade: O(n)"""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.key)
            self._inorder_recursive(node.right, result)

    def preorder_traversal(self):
        """Retorna lista da travessia Pré-Ordem. Complexidade: O(n)"""
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        if node:
            result.append(node.key)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder_traversal(self):
        """Retorna lista da travessia Pós-Ordem. Complexidade: O(n)"""
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.key)