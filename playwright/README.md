# Projeto de Automação com Playwright em Python 🚀

Este projeto é uma coletânea de exercícios práticos de automação web desenvolvidos em Python, utilizando a biblioteca Playwright. O objetivo é explorar diferentes cenários de interação com navegadores, desde buscas simples até web scraping e automação de login.

---

## 📂 Estrutura do Projeto

O projeto é organizado de forma modular, onde cada exercício reside em sua própria pasta, facilitando a execução e o entendimento individual de cada automação.

```
playwright/
├── main.py              # Script principal com um menu interativo para executar os exercícios.
├── requirements.txt     # Arquivo para listar as dependências do projeto.
├── README.md            # Este arquivo de documentação.
├── exercicio1/
│   ├── main.py          # Automação: Pesquisa no YouTube e Screenshot.
│   └── init.py      # Torna 'exercicio1' um pacote Python.
├── exercicio2/
│   ├── main.py          # Automação: Scraping de Citações do Quotes to Scrape.
│   └── init.py      # Torna 'exercicio2' um pacote Python.
├── exercicio3/
│   ├── main.py          # Automação: Login em formulário de teste e validação.
│   └── init.py      # Torna 'exercicio3' um pacote Python.
└── exercicio4/
├── main.py          # Automação: Scraping de produtos no Mercado Livre (Desafio).
└── init.py      # Torna 'exercicio4' um pacote Python.
```

## 🚀 Como Executar

Siga os passos abaixo para configurar e rodar o projeto.

### 1. Pré-requisitos

- Python 3.8 ou superior.
- Google Chrome instalado.

### 2. Configuração do Ambiente

**Clone o repositório:**

```bash
git clone https://github.com/alyssonrafael/Algoritimos_e_complexidade
cd playwright
```

**Crie e ative um ambiente virtual:**

```bash
# Criar o ambiente
python -m venv venv

# Ativar no Windows
.\venv\Scripts\activate

# Ativar no macOS/Linux
source venv/bin/activate
```

### 3. Instalação das Dependências

Instale todas as bibliotecas listadas no `requirements.txt` com um único comando:

```bash
pip install -r requirements.txt
```

### 5. Execução

Execute o orquestrador principal para iniciar o menu:

```bash
python main.py
```

Escolha a opção desejada no menu e siga as instruções no terminal.

---

## 👨‍💻 Autor

Alysson Rafael

202212048944

ciencias da computação

24/09/2025

link do funcionamento do programa [Clique aqui](https://youtu.be/KVbrBNVG9sw "youtube")

---

## ⚠️ Observações e Ética

- Este projeto foi desenvolvido exclusivamente para **fins educacionais** e como demonstração de habilidades em automação e web scraping.
- A automação de plataformas e redes sociais pode violar os **Termos de Serviço** dos sites. Utilize este código por sua conta e risco.
- **Não utilize** web scraping ou automação em sites que não permitem a prática ou para coletar dados pessoais sensíveis, respeitando a privacidade e a Lei Geral de Proteção de Dados (LGPD).
- Para testes de login, dê preferência ao uso de **contas de teste** ou sites de demonstração criados para este fim.
