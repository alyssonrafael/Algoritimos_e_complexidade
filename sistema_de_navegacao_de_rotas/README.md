# 🗺️ Sistema de Navegação de Rotas e Dados Hierárquicos

Um projeto educacional de **Algorítimos e complexidade** que integra **Árvores AVL** e **Grafos** para simular um sistema de gerenciamento de **cidades, bairros e rotas** — com interface gráfica interativa e persistência de dados.

---

## 🎯 Objetivo

O projeto tem como foco a **implementação, análise e visualização** de estruturas de dados clássicas — **Árvores Binárias de Busca Balanceadas (AVL)** e **Grafos** — aplicadas a um contexto realista de **navegação urbana**.

Principais metas:

- Implementar e operar **Árvores AVL** com balanceamento automático.
- Construir e explorar **Grafos ponderados e não direcionados**.
- Executar **algoritmos clássicos** (BFS, DFS, Dijkstra).
- Persistir e visualizar dados de forma interativa.

---

## ✨ Funcionalidades

### 🌆 Gerenciamento de Cidades (Árvore AVL)

- **Adicionar** novas cidades (ID numérico único e nome).
- **Atualizar** nomes de cidades existentes.
- **Remover** cidades.
- **Listar** cidades em diferentes percursos:
  - In-ordem
  - Pré-ordem
  - Pós-ordem

### 🏘️ Gerenciamento de Bairros e Ruas (Grafo)

- **Adicionar ou remover bairros** (vértices).
- **Adicionar ou atualizar ruas** (arestas ponderadas).
- Todas as ruas são **mão dupla** (arestas bidirecionais) na interface gráfica.

### 🧭 Análise de Rotas

- **Busca em Largura (BFS):** Explora bairros por camadas.
- **Busca em Profundidade (DFS):** Explora caminhos recursivamente.
- **Caminho Mínimo (Dijkstra):** Calcula e exibe o trajeto mais curto entre dois bairros.

### 🎨 Visualização Interativa

- **Interface Gráfica (GUI)** com visualização dinâmica do grafo.
- **Destaque visual** do caminho encontrado pelo Dijkstra.
- **Controles de zoom e movimento (pan)** para explorar o mapa.

### 💾 Persistência de Dados

- Salvamento **automático** em `cities_db.json`.
- Carregamento automático dos dados ao iniciar a aplicação.
- Sistema de fallback para recriar o arquivo em caso de erro ou corrupção.

### 📊 Análise de Complexidade

- Exibição da **complexidade teórica** das operações diretamente na interface (GUI e CLI).

---

## 🧰 Tecnologias Utilizadas

| Categoria                          | Ferramentas                                                                |
| ---------------------------------- | -------------------------------------------------------------------------- |
| **Linguagem**                | Python 3.x                                                                 |
| **Estruturas de Dados**      | Implementações próprias de Árvores AVL e Grafos (Lista de Adjacência) |
| **Interface Gráfica (GUI)** | `tkinter`, `matplotlib`, `networkx`                                  |
| **Persistência**            | `json`                                                                   |
| **Outros Módulos**          | `collections`, `heapq`, `os`, `sys`, `math`                      |

---

## 📁 Estrutura do Projeto

```bash
├── arvore_avl.py        # Implementação da classe AVLTree e AVLNode
├── arvore_binaria.py    # Versão inicial da árvore AVL 
├── grafo.py             # Implementação da classe Graph (BFS, DFS, Dijkstra, etc.)
├── gui.py               # Interface Gráfica (Tkinter + Matplotlib + NetworkX)
├── main.py              # Interface de Linha de Comando (CLI)
├── cities_db.json       # Banco de dados persistente (gerado automaticamente)
└── README.md            # Este arquivo
```

> 💡 **Nota:** A aplicação principal (`gui.py` e `main.py`) utiliza a implementação de `arvore_avl.py`. O arquivo `arvore_binaria.py` contém uma versão inicial ou base.

---

## ⚙️ Instalação e Configuração

1. **Clone o repositório** ou baixe os arquivos:

   ```bash
   git clone https://github.com/alyssonrafael/Algoritimos_e_complexidade
   cd sistema_de_navegacao_de_rotas
   ```
2. Certifique-se de ter o Python 3 instalado.
3. Instale as dependências necessárias:

   ```bash
   pip install networkx matplotlib
   ```

   (As bibliotecas tkinter e json já vêm com o Python por padrão.)

## ▶️ Como Executar

Você pode usar a aplicação de duas formas:

---

### 🖥️ 1. Interface Gráfica (Recomendada)

A interface mais completa e visual, ideal para explorar o sistema de forma intuitiva.

**Recursos disponíveis:**

- Gerenciamento completo de cidades e bairros.
- Visualização interativa do grafo (zoom, pan, destaque de caminhos).
- Execução dos algoritmos **BFS**, **DFS** e **Dijkstra**.

**Para iniciar:**

```bash
python gui.py
```

## 💻 2. Interface de Linha de Comando (CLI)

Uma versão baseada em menus de texto, útil para testes rápidos ou ambientes sem suporte gráfico.

**Recursos disponíveis:**

- Gerenciamento básico de cidades e bairros.
- Execução dos algoritmos via texto.

**Para iniciar:**

```bash
python main.py
```

---

## 💾 Persistência de Dados

- O estado da aplicação é **salvo automaticamente** em `cities_db.json`.
- O sistema **recupera os dados automaticamente** na inicialização.
- Caso o arquivo não exista, uma nova estrutura vazia é criada.

---

## 📈 Complexidade das Operações

| Estrutura                 | Operação                     | Complexidade     |
| ------------------------- | ------------------------------ | ---------------- |
| **Árvore AVL**     | Inserção / Remoção / Busca | O(log n)         |
| **Grafo (BFS/DFS)** | Travessia completa             | O(V + E)         |
| **Dijkstra**        | Caminho mínimo                | O((V + E) log V) |

---

## 🧩 Conceitos Envolvidos

- **Árvores AVL:** rotação simples e dupla, balanceamento dinâmico.
- **Grafos:** representação via lista de adjacência, pesos e conectividade.
- **Algoritmos clássicos:** busca e otimização.
- **Persistência:** serialização de dados com JSON.
- **Visualização:** uso de Matplotlib e NetworkX para visualização interativa.

---

## 👨‍💻 Autores

Desenvolvido como parte de um projeto de **Algorítimos e complexidade**, com foco em aplicar conceitos teóricos em um contexto prático e visual. E indo alem do que foi proposto colocando uma interface visual para visualizar e diminuir a abstração do terminal e persistência com um simples json.
