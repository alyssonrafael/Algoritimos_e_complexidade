# Módulo: Coletor de Notícias G1 📰

## 📄 Descrição

Este módulo é um web scraper desenvolvido para coletar as manchetes mais recentes da página inicial do portal de notícias G1 (g1.globo.com).

A coleta é realizada utilizando **automação de navegador com Selenium**, o que garante a captura de todo o conteúdo da página, incluindo notícias carregadas dinamicamente via JavaScript.

## ✨ Funcionalidades

-   **Coleta Dinâmica**: Utiliza um navegador real para carregar a página completamente antes da coleta.
-   **Esperas Inteligentes**: Aguarda ativamente até que o feed de notícias esteja visível antes de extrair os dados, tornando o script mais robusto.
-   **Extração de Dados**: Captura o título, o link e um breve resumo de cada notícia.
-   **Saída Estruturada**: Salva os dados coletados em um arquivo `manchetes_g1_selenium.json` dentro deste diretório.

## ⚙️ Como Funciona

O script utiliza o **Selenium** para iniciar e controlar uma instância do navegador Google Chrome. Ele navega até a URL do G1 e, em vez de analisar o HTML imediatamente, usa um `WebDriverWait` para esperar que os elementos do feed de notícias sejam carregados e renderizados na página.

Após a confirmação de que o conteúdo está presente, o Selenium percorre os elementos, extrai as informações desejadas e, ao final do processo, fecha o navegador.

## 📦 Dependências

-   `selenium`
-   `webdriver-manager`

*(Estas dependências são instaladas através do `requirements.txt` na raiz do projeto.)*

## 🔧 Configuração

Este módulo não requer nenhuma configuração especial (como arquivos `.env`).

## 📄 Saída (Output)

O coletor gera o arquivo `manchetes_g1_selenium.json` com uma lista de notícias, seguindo a estrutura abaixo:

```json
[
    {
        "titulo": "Título da Primeira Notícia Importante",
        "link": "[https://g1.globo.com/link-para-a-noticia-1](https://g1.globo.com/link-para-a-noticia-1)",
        "resumo": "Um breve resumo sobre o acontecimento da notícia número 1.",
        "data_coleta": "2025-09-24 15:40:00"
    },
    {
        "titulo": "Título da Segunda Notícia",
        "link": "[https://g1.globo.com/link-para-a-noticia-2](https://g1.globo.com/link-para-a-noticia-2)",
        "resumo": "Resumo da notícia número 2.",
        "data_coleta": "2025-09-24 15:40:00"
    }
]
```

## 🧪 Como Testar de Forma Independente

Para testar apenas este módulo, navegue até esta pasta (`noticias/`) pelo terminal e execute:
```bash
python main.py
```
Isso irá iniciar uma janela do navegador que se fechará automaticamente ao final da coleta.