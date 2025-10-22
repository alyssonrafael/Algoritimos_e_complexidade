class AVLNode:
    """Nó de uma Árvore AVL. Inclui o fator 'height' (altura)."""
    def __init__(self, key, data=None):
        self.key = key
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    """
    Implementação de Árvore AVL (Adelson-Velsky e Landis).
    """
    def __init__(self):
        self.root = None

    # --- Funções de altura e balanceamento ---
    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _update_height(self, node):
        if not node:
            return 0
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    # --- Rotações ---
    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        self._update_height(z)
        self._update_height(y)
        return y

    def _left_rotate(self, y):
        z = y.right
        T2 = z.left
        z.left = y
        y.right = T2
        self._update_height(y)
        self._update_height(z)
        return z

    # --- Inserção com Balanceamento ---
    def insert(self, key, data=None):
        self.root = self._insert_recursive(self.root, key, data)

    def _insert_recursive(self, node, key, data):
        if not node:
            return AVLNode(key, data)
        
        if key < node.key:
            node.left = self._insert_recursive(node.left, key, data)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, data)
        else:
            node.data = data
            return node

        self._update_height(node)
        balance = self._get_balance(node)

        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    # --- Remoção com Balanceamento---
    def _find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def remove(self, key):
        self.root = self._remove_recursive(self.root, key)

    def _remove_recursive(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self._remove_recursive(node.left, key)
        elif key > node.key:
            node.right = self._remove_recursive(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                min_larger_node = self._find_min(node.right)
                node.key = min_larger_node.key
                node.data = min_larger_node.data
                node.right = self._remove_recursive(node.right, min_larger_node.key)

        if node is None:
            return node

        self._update_height(node)
        balance = self._get_balance(node)

        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    # --- Busca ---
    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    # --- Percursos ---
    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.key)
            self._inorder_recursive(node.right, result)

    def preorder_traversal(self):
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        if node:
            result.append(node.key)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder_traversal(self):
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.key)

    # Busca os dados 
    def get_all_nodes_data(self):
        """
        Retorna uma lista de todos os 'data' dos nós (ex: objetos City)
        em percurso in-ordem.
        """
        nodes_data = []
        self._collect_data_inorder(self.root, nodes_data)
        return nodes_data

    def _collect_data_inorder(self, node, nodes_data_list):
        """Método auxiliar recursivo para coletar os dados."""
        if node:
            self._collect_data_inorder(node.left, nodes_data_list)
            if node.data:
                nodes_data_list.append(node.data) # Adiciona o objeto City
            self._collect_data_inorder(node.right, nodes_data_list)
    