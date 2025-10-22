import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Listbox, Text, END, Frame, Label, Entry, Button
from tkinter.ttk import Combobox, Notebook, Separator 

import json
import collections
import os
import sys

import networkx as nx
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk 

from arvore_avl import AVLTree
from grafo import Graph

# --- Lógica de Dados ---
DB_FILE = "cities_db.json"
class City:
    def __init__(self, name, id_num, suppress_print=False):
        self.name = name
        self.id = id_num
        self.neighborhood_graph = Graph()
def save_data(avl_tree):
    cities_list = avl_tree.get_all_nodes_data()
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
    except Exception as e:
        messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar os dados em {DB_FILE}:\n{e}")
def load_data():
    new_tree = AVLTree()
    if not os.path.exists(DB_FILE):
        return new_tree
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            data_loaded = json.load(f)
            if not isinstance(data_loaded, list): return new_tree
            for city_data in data_loaded:
                city = City(city_data['name'], city_data['id'], suppress_print=True)
                city.neighborhood_graph.nodes = set(city_data.get('graph_nodes', []))
                adj_data = city_data.get('graph_adj', {})
                rebuilt_adj = collections.defaultdict(dict)
                for node, neighbors in adj_data.items():
                    rebuilt_adj[node] = dict(neighbors)
                city.neighborhood_graph.adj = rebuilt_adj
                new_tree.insert(city.id, city)
            return new_tree
    except Exception as e:
        messagebox.showwarning("Erro ao Carregar", f"Não foi possível carregar {DB_FILE}:\n{e}\nIniciando com árvore vazia.")
        return new_tree


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tip)  
        widget.bind("<Leave>", self.hide_tip)  

    def show_tip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert") 
        x += self.widget.winfo_rootx() + 25     
        y += self.widget.winfo_rooty() + 25     

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True) 
        self.tooltip_window.wm_geometry(f"+{x}+{y}") 

        label = tk.Label(self.tooltip_window, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None

class CustomToolbar(NavigationToolbar2Tk):
    """Uma barra de ferramentas Matplotlib personalizada com tooltips customizados."""
    
    toolitems_keep = ('Home', 'Pan') 
    
    def __init__(self, canvas, window):
        super().__init__(canvas, window, pack_toolbar=False) 

        if 'Home' in self._buttons:
            ToolTip(self._buttons['Home'], "Resetar Visão")
        if 'Pan' in self._buttons:
            ToolTip(self._buttons['Pan'], "Mover Gráfico")

        buttons_to_hide = []
        for text, tooltip_text, image_file, callback_name in self.toolitems:
            if text not in self.toolitems_keep and text is not None:
                buttons_to_hide.append(text)
        
        for text in buttons_to_hide:
            if text in self._buttons:
                self._buttons[text].pack_forget()

        self.add_zoom_buttons()
        self.pack(side=tk.BOTTOM, fill=tk.X)

    def add_zoom_buttons(self):
        zoom_frame = tk.Frame(self) 
        zoom_frame.pack(side=tk.LEFT, padx=5)

        button_plus = tk.Button(master=zoom_frame, text='+', width=2, command=self.zoom_in)
        button_plus.pack(side=tk.LEFT, padx=2)
        ToolTip(button_plus, "Aumentar Zoom") 

        button_minus = tk.Button(master=zoom_frame, text='-', width=2, command=self.zoom_out)
        button_minus.pack(side=tk.LEFT, padx=2)
        ToolTip(button_minus, "Diminuir Zoom") 


    def zoom_in(self):
        self._zoom_factor(0.8)

    def zoom_out(self):
        self._zoom_factor(1.2)

    def _zoom_factor(self, factor):
        ax = self.canvas.figure.axes[0]
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        x_center = (cur_xlim[1] + cur_xlim[0]) / 2
        y_center = (cur_ylim[1] + cur_ylim[0]) / 2
        new_width = (cur_xlim[1] - cur_xlim[0]) * factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * factor
        ax.set_xlim([x_center - new_width / 2, x_center + new_width / 2])
        ax.set_ylim([y_center - new_height / 2, y_center + new_height / 2])
        self.canvas.draw_idle() 

# --- Janela do Explorador de Cidades (Grafo) ---

class CityExplorerWindow:
    
    def __init__(self, parent, city_obj, avl_tree):
        self.root = Toplevel(parent)
        self.root.title(f"Explorador: {city_obj.name} (ID: {city_obj.id})")
        self.root.geometry("800x700") 
        
        self.city = city_obj
        self.graph = city_obj.neighborhood_graph
        self.avl_tree = avl_tree
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5,10), pady=10)

        self.figure = plt.Figure(figsize=(5, 5), dpi=100, facecolor='#f0f0f0')
        self.ax = self.figure.add_subplot(111, facecolor='#f0f0f0')
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=right_frame)
        self.canvas.draw()
        
      
        self.toolbar = CustomToolbar(self.canvas, right_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.nx_graph = nx.Graph()

        left_frame = ttk.Frame(main_frame, width=300)
        left_frame.pack(side='left', fill='y', padx=(10,5), pady=10)
        left_frame.pack_propagate(False)

        self.notebook = Notebook(left_frame)
        self.notebook.pack(fill='x', expand=False, pady=(0, 10))

        self.tab_analise = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_analise, text='Analisar Rotas')

        percurso_frame = ttk.LabelFrame(self.tab_analise, text="Percursos (BFS/DFS)", padding=10)
        percurso_frame.pack(fill='x')

        ttk.Label(percurso_frame, text="Ponto de Partida:").pack(anchor='w')
        self.analise_partida_combo = Combobox(percurso_frame, width=25, state='readonly')
        self.analise_partida_combo.pack(fill='x', pady=(0, 10))
        
        bfs_btn = ttk.Button(percurso_frame, text="Rodar BFS", command=self.run_bfs)
        bfs_btn.pack(side='left', expand=True, padx=2)
        dfs_btn = ttk.Button(percurso_frame, text="Rodar DFS", command=self.run_dfs)
        dfs_btn.pack(side='left', expand=True, padx=2)

        dijkstra_frame = ttk.LabelFrame(self.tab_analise, text="Caminho Mínimo (Dijkstra)", padding=10)
        dijkstra_frame.pack(fill='x', pady=10)
        
        ttk.Label(dijkstra_frame, text="Origem:").pack(anchor='w')
        self.dijkstra_origem_combo = Combobox(dijkstra_frame, width=25, state='readonly')
        self.dijkstra_origem_combo.pack(fill='x', pady=(0, 5))
        
        ttk.Label(dijkstra_frame, text="Destino:").pack(anchor='w')
        self.dijkstra_destino_combo = Combobox(dijkstra_frame, width=25, state='readonly')
        self.dijkstra_destino_combo.pack(fill='x', pady=(0, 10))
        
        dijkstra_btn = ttk.Button(dijkstra_frame, text="Calcular Caminho Mínimo", command=self.run_dijkstra)
        dijkstra_btn.pack(fill='x')

        self.tab_editar = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_editar, text='Editar Mapa')

        rua_frame = ttk.LabelFrame(self.tab_editar, text="Adicionar / Atualizar Rua", padding=10)
        rua_frame.pack(fill='x')

        ttk.Label(rua_frame, text="Bairro A:").pack(anchor='w')
        self.edit_bairro_a_combo = Combobox(rua_frame, width=25)
        self.edit_bairro_a_combo.pack(fill='x', pady=(0, 5))
        
        ttk.Label(rua_frame, text="Bairro B:").pack(anchor='w')
        self.edit_bairro_b_combo = Combobox(rua_frame, width=25)
        self.edit_bairro_b_combo.pack(fill='x', pady=(0, 5))

        ttk.Label(rua_frame, text="Distância:").pack(anchor='w')
        self.edit_distancia_entry = ttk.Entry(rua_frame, width=10)
        self.edit_distancia_entry.pack(anchor='w', pady=(0, 10))
        
        add_route_btn = ttk.Button(rua_frame, text="Salvar Rua (Mão-Dupla)", command=self.add_route)
        add_route_btn.pack(fill='x')

        bairro_frame = ttk.LabelFrame(self.tab_editar, text="Remover Bairro (Ação Destrutiva)", padding=10)
        bairro_frame.pack(fill='x', pady=10)
        
        ttk.Label(bairro_frame, text="Selecione o Bairro:").pack(anchor='w')
        self.remove_bairro_combo = Combobox(bairro_frame, width=25, state='readonly')
        self.remove_bairro_combo.pack(fill='x', pady=(0, 10))
        
        remove_bairro_btn = ttk.Button(bairro_frame, text="Remover Bairro e suas Ruas", command=self.remove_bairro, style='Danger.TButton')
        remove_bairro_btn.pack(fill='x')
        style = ttk.Style()
        style.configure('Danger.TButton', foreground='red', font=('TkDefaultFont', 9, 'bold'))

        output_frame = ttk.Frame(left_frame)
        output_frame.pack(fill='both', expand=True)

        ttk.Label(output_frame, text="Resultado da Operação:").pack(anchor='w', pady=(5,2))
        self.output_text = Text(output_frame, height=10, wrap='word', font=("Arial", 9))
        self.output_text.pack(fill='both', expand=True)

        self.update_bairro_list()
        self.draw_graph()

        self.root.transient(parent)
        self.root.grab_set()

    def update_bairro_list(self):
        bairros = sorted(list(self.graph.nodes))
        self.analise_partida_combo['values'] = bairros
        self.dijkstra_origem_combo['values'] = bairros
        self.dijkstra_destino_combo['values'] = bairros
        self.edit_bairro_a_combo['values'] = bairros
        self.edit_bairro_b_combo['values'] = bairros
        self.remove_bairro_combo['values'] = bairros

    def log_output(self, message, complexity_msg=None):
        self.output_text.delete("1.0", END)
        self.output_text.insert(END, message)
        if complexity_msg:
            formatted_comp = f"\n\n--- Análise de Complexidade ---\n{complexity_msg}"
            self.output_text.insert(END, formatted_comp)

    def draw_graph(self, highlight_path=None):
        NODE_COLOR = '#42a5f5'         
        NODE_HIGHLIGHT_COLOR = '#ef5350' 
        EDGE_COLOR = '#9e9e9e'         
        EDGE_HIGHLIGHT_COLOR = '#ef5350' 
        
        self.ax.clear()
        self.nx_graph.clear()

        added_edges = set()
        for u, neighbors in self.graph.adj.items():
            self.nx_graph.add_node(u) 
            for v, weight in neighbors.items():
                if (v, u) not in added_edges:
                    self.nx_graph.add_edge(u, v, weight=weight)
                    added_edges.add((u, v))
        
        if not self.nx_graph.nodes:
            self.ax.text(0.5, 0.5, "Sem bairros para desenhar.", 
                         horizontalalignment='center', verticalalignment='center', 
                         transform=self.ax.transAxes)
            self.canvas.draw()
            return
            
        try:
            k_value = 0.9 if len(self.nx_graph.nodes) < 30 else 1.2
            pos = nx.spring_layout(self.nx_graph, k=k_value, iterations=50, seed=42) 
        except nx.NetworkXException:
            pos = nx.circular_layout(self.nx_graph)

        highlight_set = set(highlight_path) if highlight_path else set()
        
        node_color_map = []
        for node in self.nx_graph.nodes():
            if node in highlight_set:
                node_color_map.append(NODE_HIGHLIGHT_COLOR)
            else:
                node_color_map.append(NODE_COLOR)
        
        path_edges = []
        edge_color_map = []
        edge_width_map = []
        
        if highlight_path:
            path_edges = list(zip(highlight_path[:-1], highlight_path[1:]))
            
        for edge in self.nx_graph.edges():
            if edge in path_edges or (edge[1], edge[0]) in path_edges:
                edge_color_map.append(EDGE_HIGHLIGHT_COLOR)
                edge_width_map.append(2.5)
            else:
                edge_color_map.append(EDGE_COLOR)
                edge_width_map.append(1.0)
        
        nx.draw_networkx_nodes(
            self.nx_graph, pos, ax=self.ax, 
            node_size=700, 
            node_color=node_color_map,
            edgecolors='black',
            linewidths=0.5
        )
        
        nx.draw_networkx_edges(
            self.nx_graph, pos, ax=self.ax, 
            edgelist=self.nx_graph.edges(), 
            edge_color=edge_color_map, 
            width=edge_width_map,
            alpha=0.8
        )
        
        nx.draw_networkx_labels(
            self.nx_graph, pos, ax=self.ax, 
            font_size=9, font_weight='bold',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.5, pad=0)
        )
        
        edge_labels = nx.get_edge_attributes(self.nx_graph, 'weight')
        nx.draw_networkx_edge_labels(
            self.nx_graph, pos, 
            edge_labels=edge_labels, 
            ax=self.ax, 
            font_size=8, 
            font_color='#333333',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=0)
        )

        self.ax.set_title(f"Mapa de Bairros: {self.city.name}", weight='bold')
        self.ax.axis('off')
        
        try:
           self.figure.tight_layout(pad=1.5)
        except ValueError:
            pass 
            
        self.canvas.draw()

    def add_route(self):
        b1 = self.edit_bairro_a_combo.get()
        b2 = self.edit_bairro_b_combo.get()
        dist_str = self.edit_distancia_entry.get()
        if not all([b1, b2, dist_str]):
            messagebox.showerror("Erro", "Preencha Bairro A, Bairro B e Distância.", parent=self.root)
            return
        try:
            dist = int(dist_str)
            self.graph.add_edge(b1, b2, dist)
            self.graph.add_edge(b2, b1, dist)
            save_data(self.avl_tree) 
            self.update_bairro_list() 
            self.draw_graph()
            msg = f"Rua adicionada: {b1} <-> {b2} (Distância: {dist})"
            comp = ("Operação: Adicionar Aresta (Mão-Dupla)\n"
                    "Estrutura: Grafo (Lista Adj.)\n"
                    "Complexidade: O(1)")
            self.log_output(msg, comp)
            self.edit_bairro_a_combo.set('')
            self.edit_bairro_b_combo.set('')
            self.edit_distancia_entry.delete(0, END)
        except ValueError:
            messagebox.showerror("Erro", "A distância deve ser um número inteiro.", parent=self.root)

    def remove_bairro(self):
        bairro = self.remove_bairro_combo.get()
        if not bairro:
            messagebox.showerror("Erro", "Selecione o bairro para remover.", parent=self.root)
            return
        if messagebox.askyesno("Confirmar Remoção", 
                               f"Tem certeza que deseja remover o bairro '{bairro}'?\n"
                               "TODAS as ruas conectadas a ele serão apagadas.", 
                               parent=self.root):
            self.graph.remove_node(bairro)
            save_data(self.avl_tree)
            self.update_bairro_list()
            self.draw_graph()
            self.remove_bairro_combo.set('')
            msg = f"Bairro '{bairro}' e suas conexões foram removidos."
            comp = ("Operação: Remover Vértice (Bairro)\n"
                    "Estrutura: Grafo (Lista Adj.)\n"
                    "Complexidade: O(V) - (V é o nº de bairros)")
            self.log_output(msg, comp)

    def run_bfs(self):
        start_node = self.analise_partida_combo.get()
        if not start_node:
            messagebox.showerror("Erro", "Informe o 'Ponto de Partida' para o BFS.", parent=self.root)
            return
        self.draw_graph() 
        order = self.graph.bfs(start_node)
        msg = f"Busca em Largura (BFS) a partir de '{start_node}':\n\n" + " -> ".join(order)
        comp = ("Operação: Busca em Largura (BFS)\n"
                "Estrutura: Grafo\n"
                "Complexidade: O(V + E)")
        self.log_output(msg, comp)

    def run_dfs(self):
        start_node = self.analise_partida_combo.get()
        if not start_node:
            messagebox.showerror("Erro", "Informe o 'Ponto de Partida' para o DFS.", parent=self.root)
            return
        self.draw_graph()
        order = self.graph.dfs(start_node)
        msg = f"Busca em Profundidade (DFS) a partir de '{start_node}':\n\n" + " -> ".join(order)
        comp = ("Operação: Busca em Profundidade (DFS)\n"
                "Estrutura: Grafo\n"
                "Complexidade: O(V + E)")
        self.log_output(msg, comp)

    def run_dijkstra(self):
        start_node = self.dijkstra_origem_combo.get()
        end_node = self.dijkstra_destino_combo.get()
        if not all([start_node, end_node]):
            messagebox.showerror("Erro", "Informe 'Origem' e 'Destino'.", parent=self.root)
            return
        distances, _ = self.graph.dijkstra(start_node)
        path = self.graph.get_shortest_path(start_node, end_node)
        comp = ("Operação: Caminho Mínimo (Dijkstra)\n"
                "Estrutura: Grafo (c/ Heap)\n"
                "Complexidade: O(E log V)")
        if path:
            dist = distances.get(end_node, 'N/A')
            self.draw_graph(highlight_path=path) 
            msg = (f"Caminho Mínimo (Dijkstra) de '{start_node}' para '{end_node}':\n\n"
                   f"{' -> '.join(path)}\n\n"
                   f"Distância Total: {dist}")
            self.log_output(msg, comp)
        else:
            self.draw_graph() 
            msg = f"Não foi encontrado caminho de '{start_node}' para '{end_node}'."
            self.log_output(msg, comp)


# --- Janela Principal (AVL) ---

class CityNavigatorApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Cidades (AVL + Grafos)")
        self.root.geometry("600x450")
        
        self.avl_tree = load_data()
        self.selected_city_id = None
        
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill='both', expand=True, pady=(0,10))
        
        ttk.Label(list_frame, text="Cidades Cadastradas (Árvore AVL)", font=("Arial", 12, "bold")).pack(pady=5)
        
        percurso_frame = ttk.Frame(list_frame)
        percurso_frame.pack(fill='x', pady=5)
        
        self.inorder_btn = ttk.Button(percurso_frame, text="In-Ordem", command=lambda: self.populate_listbox("inorder"))
        self.inorder_btn.pack(side='left', expand=True)
        self.preorder_btn = ttk.Button(percurso_frame, text="Pré-Ordem", command=lambda: self.populate_listbox("preorder"))
        self.preorder_btn.pack(side='left', expand=True)
        self.postorder_btn = ttk.Button(percurso_frame, text="Pós-Ordem", command=lambda: self.populate_listbox("postorder"))
        self.postorder_btn.pack(side='left', expand=True)
        
        self.city_listbox = Listbox(list_frame, height=10)
        self.city_listbox.pack(fill='both', expand=True)
        
        self.city_listbox.bind("<ButtonRelease-1>", self.on_city_select)
        self.city_listbox.bind("<Double-Button-1>", self.on_city_double_click)
        
        form_frame = ttk.LabelFrame(main_frame, text="Formulário da Cidade", padding="10")
        form_frame.pack(fill='x', expand=False)
        
        entry_frame = ttk.Frame(form_frame)
        entry_frame.pack(fill='x', expand=True, pady=(0, 5))
        
        ttk.Label(entry_frame, text="ID da Cidade:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.city_id_entry = ttk.Entry(entry_frame, width=15)
        self.city_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.clear_btn = ttk.Button(entry_frame, text="Limpar / Novo", command=self.clear_form, width=15)
        self.clear_btn.grid(row=0, column=2, padx=(20, 5), pady=5, sticky='e')
        
        ttk.Label(entry_frame, text="Nome da Cidade:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.city_name_entry = ttk.Entry(entry_frame, width=45)
        self.city_name_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky='w')
        
        entry_frame.grid_columnconfigure(2, weight=1)

        separator = ttk.Separator(form_frame, orient='horizontal')
        separator.pack(fill='x', expand=True, pady=5)

        action_frame = ttk.Frame(form_frame)
        action_frame.pack(fill='x', expand=True, pady=(5,0))
        
        self.save_btn = ttk.Button(action_frame, text="Adicionar Nova Cidade", command=self.on_save_click)
        self.save_btn.pack(side='left', expand=True, fill='x', padx=2)
        
        self.remove_btn = ttk.Button(action_frame, text="Remover Selecionada", command=self.on_remove_click, style='Danger.TButton')
        self.remove_btn.pack(side='left', expand=True, fill='x', padx=2)
        
        self.explore_btn = ttk.Button(action_frame, text="Explorar Selecionada", command=self.on_explore_click)
        self.explore_btn.pack(side='left', expand=True, fill='x', padx=2)
        
        self.populate_listbox("inorder")
        self.clear_form()

    def clear_form(self, event=None):
        self.selected_city_id = None
        self.city_id_entry.config(state='normal')
        self.city_id_entry.delete(0, END)
        self.city_name_entry.delete(0, END)
        self.save_btn.config(text="Adicionar Nova Cidade", state='normal')
        self.remove_btn.config(state='disabled')
        self.explore_btn.config(state='disabled')
        self.clear_btn.config(state='disabled')
        self.city_listbox.selection_clear(0, END)

    def on_city_select(self, event):
        try:
            selection_index = self.city_listbox.curselection()
            if not selection_index: return
            selected_string = self.city_listbox.get(selection_index[0])
            if not selected_string.strip().startswith("ID:"):
                self.clear_form()
                return 
            city_id = int(selected_string.split()[1])
            node = self.avl_tree.search(city_id)
            if node:
                self.selected_city_id = city_id
                self.city_id_entry.config(state='normal')
                self.city_id_entry.delete(0, END)
                self.city_id_entry.insert(0, node.data.id)
                self.city_id_entry.config(state='disabled')
                self.city_name_entry.delete(0, END)
                self.city_name_entry.insert(0, node.data.name)
                self.save_btn.config(text="Atualizar Nome", state='normal')
                self.remove_btn.config(state='normal')
                self.explore_btn.config(state='normal')
                self.clear_btn.config(state='normal')
        except (ValueError, IndexError):
            self.clear_form()

    def on_city_double_click(self, event):
        self.on_city_select(event)
        if self.selected_city_id:
            self.on_explore_click()

    def on_save_click(self):
        if self.selected_city_id:
            new_name = self.city_name_entry.get().strip()
            if not new_name:
                messagebox.showerror("Erro", "O nome não pode ficar em branco.")
                return
            node = self.avl_tree.search(self.selected_city_id)
            if node:
                node.data.name = new_name
                save_data(self.avl_tree)
                messagebox.showinfo("Sucesso", f"Nome da cidade ID {self.selected_city_id} atualizado para '{new_name}'.")
                self.populate_listbox()
                self.clear_form()
        else:
            id_str = self.city_id_entry.get()
            name = self.city_name_entry.get().strip()
            if not id_str or not name:
                messagebox.showerror("Erro", "ID e Nome são obrigatórios para adicionar.")
                return
            try:
                city_id = int(id_str)
                if self.avl_tree.search(city_id):
                    messagebox.showerror("Erro", f"O ID {city_id} já está em uso.")
                else:
                    new_city = City(name, city_id, suppress_print=True)
                    self.avl_tree.insert(city_id, new_city)
                    save_data(self.avl_tree)
                    messagebox.showinfo("Sucesso", f"Cidade '{name}' (ID: {city_id}) adicionada.")
                    self.populate_listbox()
                    self.clear_form()
            except ValueError:
                messagebox.showerror("Erro", "O ID deve ser um número inteiro.")

    def on_remove_click(self):
        if not self.selected_city_id: return
        node = self.avl_tree.search(self.selected_city_id)
        if not node:
            messagebox.showerror("Erro", f"Cidade com ID {self.selected_city_id} não encontrada (erro de sincronia).")
            return
        if messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover '{node.data.name}' (ID: {self.selected_city_id})?"):
            self.avl_tree.remove(self.selected_city_id)
            save_data(self.avl_tree)
            messagebox.showinfo("Sucesso", f"Cidade (ID: {self.selected_city_id}) removida.")
            self.populate_listbox()
            self.clear_form()

    def on_explore_click(self):
        if not self.selected_city_id: return
        node = self.avl_tree.search(self.selected_city_id)
        if node:
            CityExplorerWindow(self.root, node.data, self.avl_tree)
        else:
            messagebox.showerror("Erro", f"Cidade com ID {self.selected_city_id} não encontrada (erro de sincronia).")
    
    def populate_listbox(self, order_type="inorder"):
        self.city_listbox.delete(0, END)
        city_keys = []
        if order_type == "inorder":
            city_keys = self.avl_tree.inorder_traversal()
            self.city_listbox.insert(END, "--- Percurso In-Ordem (Ordenado por ID) ---")
        elif order_type == "preorder":
            city_keys = self.avl_tree.preorder_traversal()
            self.city_listbox.insert(END, "--- Percurso Pré-Ordem ---")
        elif order_type == "postorder":
            city_keys = self.avl_tree.postorder_traversal()
            self.city_listbox.insert(END, "--- Percurso Pós-Ordem ---")
        if not city_keys:
            self.city_listbox.insert(END, "Nenhuma cidade cadastrada.")
            return
        for key in city_keys:
            node = self.avl_tree.search(key)
            if node and node.data:
                self.city_listbox.insert(END, f"  ID: {node.key} - Nome: {node.data.name}")
        self.clear_form()

# --- Inicialização da Aplicação ---
if __name__ == "__main__":
    try:
        import networkx
        import matplotlib
    except ImportError:
        messagebox.showerror("Dependências Faltando",
            "Este modo gráfico requer as bibliotecas 'networkx' e 'matplotlib'.\n"
            "Por favor, instale-as executando:\n\n"
            "pip install networkx matplotlib")
        sys.exit(1)
        
    root = tk.Tk()
    app = CityNavigatorApp(root)
    root.mainloop()