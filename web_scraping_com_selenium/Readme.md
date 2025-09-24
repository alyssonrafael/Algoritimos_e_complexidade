# Projeto de Automação em Python 🤖

Este projeto é uma suíte de automação desenvolvida em Python, contendo robôs para interagir com redes sociais e coletar dados da web. Atualmente, o projeto inclui dois módulos principais:

1. **Bot do Instagram**: Um robô robusto que realiza login, lida com verificação de duas etapas (2FA) e extrai informações de perfis.
2. **Coletor de Notícias**: Um scraper que coleta as últimas manchetes do portal de notícias G1.

---

## 📂 Estrutura do Projeto

O projeto é organizado de forma modular para facilitar a manutenção e a adição de novas automações.

```
web_scraping_com_selenium/
├── .env                  # Arquivo para credenciais (deve ser criado localmente)
├── requirements.txt      # Lista de dependências do projeto
├── main.py               # Orquestrador principal que executa os robôs
├── boot_login/
│   ├── __init__.py       # Torna este diretório um pacote Python.
│   ├── main.py           # Lógica do bot do Instagram
│   └── README.md         # Documentação específica do bot
└── noticias/
    ├── __init__.py       # Torna este diretório um pacote Python.
    ├── main.py           # Lógica do coletor de notícias
    └── README.md         # Documentação específica do coletor
```

---

## ✨ Funcionalidades

- **Interface de Menu**: Orquestrador central para escolher qual robô executar.
- **Gerenciamento de Dependências**: Arquivo `requirements.txt` para fácil instalação.
- **Segurança**: Uso de variáveis de ambiente (`.env`) para proteger credenciais.
- **Automação do Instagram**:
  - Login automatizado com comportamento "humano".
  - Suporte para intervenção manual na verificação de duas etapas (2FA).
  - Extração de dados de perfil (Bio).
  - Saída de dados em formato JSON.
- **Coleta de Notícias**:
  - Scraping de manchetes do G1.
  - Extração de título, link e resumo.
  - Saída de dados em formato JSON.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Selenium**: Para automação de navegador.
- **python-dotenv**: Para gerenciamento de variáveis de ambiente.
- **webdriver-manager**: Para gerenciamento automático do ChromeDriver.

---

## 🚀 Como Executar

Siga os passos abaixo para configurar e rodar o projeto.

### 1. Pré-requisitos

- Python 3.8 ou superior.
- Google Chrome instalado.

### 2. Configuração do Ambiente

**Clone o repositório:**

```bash
git clone https://github.com/alyssonrafael/Algoritimos_e_complexidade
cd web_scraping_com_selenium
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

### 4. Configuração das Credenciais

Crie um arquivo chamado `.env` ou renomeie o `.env.example` na raiz da pasta e adicione suas credenciais do Instagram:

```ini
INSTAGRAM_USER="seu_usuario_aqui"
INSTAGRAM_PASS="sua_senha_aqui"
```

### 5. Execução

Execute o orquestrador principal para iniciar o menu:

```bash
python main.py
```

Escolha a opção desejada no menu e siga as instruções no terminal.

---

## 📚 Módulos

- **🤖 Bot do Instagram**: Focado em automação de login e extração de dados do Instagram.
  - [Clique aqui para a documentação detalhada do bot.](./boot_login/README.md)
- **📰 Coletor de Notícias**: Focado em web scraping de portais de notícias.
  - [Clique aqui para a documentação detalhada do coletor.](./noticias/README.md)

---

## 👨‍💻 Autor

Alysson Rafael

202212048944

ciencias da computação

24/09/2025

link do funcionamento do programa [Clique aqui](https://youtu.be/-P5q24GUq4U)

---

## ⚠️ Observações e Ética

- Este projeto foi desenvolvido exclusivamente para **fins educacionais** e como demonstração de habilidades em automação e web scraping.
- A automação de plataformas e redes sociais pode violar os **Termos de Serviço** dos sites. Utilize este código por sua conta e risco.
- **Não utilize** web scraping ou automação em sites que não permitem a prática ou para coletar dados pessoais sensíveis, respeitando a privacidade e a Lei Geral de Proteção de Dados (LGPD).
- Para testes de login, dê preferência ao uso de **contas de teste** ou sites de demonstração criados para este fim.
