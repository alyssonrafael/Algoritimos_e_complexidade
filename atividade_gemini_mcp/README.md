# Projeto de Estudo: Complexidade de Algoritmos em Python

Este repositório contém três exemplos de algoritmos em Python, cada um demonstrando uma complexidade de tempo diferente (Notação Big O). O objetivo é fornecer uma visualização prática de como a eficiência de um algoritmo pode variar drasticamente com base em sua implementação.

O projeto inclui um menu interativo para facilitar a execução e o teste de cada algoritmo separadamente.

> **Nota:** Este projeto, incluindo a estrutura dos códigos, a documentação e este arquivo README, foi gerado com o auxílio da IA **Gemini** do Google, como parte de um exercício prático. utilizando o MCP (cli) do google

---

## 📚 Algoritmos Incluídos

O projeto está dividido nos seguintes exemplos de complexidade:

### 1. Complexidade Constante - `O(1)`

- **Arquivo:** `complexidade_o1.py`
- **Função:** `obter_primeiro_elemento()`
- **Descrição:** Não importa o tamanho da lista (seja com 10 ou 1 milhão de elementos), a operação de acessar o primeiro índice leva sempre o mesmo tempo. É a forma mais eficiente de complexidade.

### 2. Complexidade Linear - `O(n)`

- **Arquivo:** `complexidade_on.py`
- **Função:** `busca_linear()`
- **Descrição:** O tempo de execução cresce em proporção direta ao número de elementos (`n`) na lista. Para encontrar um item no pior cenário, o algoritmo precisa percorrer a lista inteira uma vez.

### 3. Complexidade Quadrática - `O(n²)`

- **Arquivo:** `complexidade_on2.py`
- **Função:** `bubble_sort()`
- **Descrição:** O tempo de execução cresce de forma quadrática em relação ao número de elementos. Isso geralmente ocorre devido a laços de repetição aninhados, onde para cada elemento, percorremos a lista novamente. É consideravelmente menos eficiente para grandes conjuntos de dados.

---

## 🚀 Como Executar

Para rodar este projeto, você precisará ter o [Python 3](https://www.python.org/downloads/) instalado.

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/alyssonrafael/Algoritimos_e_complexidade
   ```
2. **Navegue até a pasta do projeto:**

   ```bash
   cd atividade_gemini_mcp
   ```
3. **Execute o menu principal:**

   ```bash
   python menu.py
   ```
4. Siga as instruções exibidas no terminal para escolher qual dos três algoritmos você deseja testar.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3
- google gemini cli
