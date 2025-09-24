# Módulo: Bot de Automação do Instagram 🤖

## 📄 Descrição

Este módulo contém a lógica para automatizar interações com o Instagram. Ele é capaz de realizar login em uma conta, lidar com a verificação de duas etapas (2FA) e extrair dados públicos de um perfil especificado.

## ✨ Funcionalidades

- **Login Seguro**: Utiliza credenciais armazenadas em um arquivo `.env` na raiz do projeto.
- **Comportamento Humano**: Simula a digitação de um usuário real para evitar detecção.
- **Suporte a 2FA**: Pausa a execução e solicita que o usuário insira o código de verificação de 6 dígitos no terminal, garantindo a segurança.
- **Extração de Dados**: Coleta a biografia completa (incluindo quebras de linha) do perfil alvo.
- **Saída Estruturada**: Salva os dados coletados em um arquivo `dados_perfil_instagram.json` dentro deste diretório.

## ⚙️ Como Funciona

O bot utiliza o **Selenium** para controlar uma instância do Google Chrome. Ele navega até a página de login, preenche as credenciais, aguarda a possível tela de 2FA e, após o login bem-sucedido, navega para o perfil alvo para realizar a extração dos dados do DOM da página.

## 📦 Dependências

- `selenium`
- `webdriver-manager`
- `python-dotenv`

*(Estas dependências são instaladas através do `requirements.txt` na raiz do projeto.)*

## 🔧 Configuração

Este módulo requer que as seguintes variáveis de ambiente sejam definidas no arquivo `.env` na raiz do projeto:

- `INSTAGRAM_USER`: Seu nome de usuário do Instagram.
- `INSTAGRAM_PASS`: Sua senha do Instagram.

## 📄 Saída (Output)

O bot gera o arquivo `dados_perfil_instagram.json` com a seguinte estrutura:

```json
{
    "perfil": "@nome_do_perfil",
    "data_extracao": "2025-09-24 15:30:00",
    "bio": "Esta é a primeira linha da bio.\nEsta é a segunda linha.\n- Item da lista"
}
```

## 🧪 Como Testar de Forma Independente

Para testar apenas este módulo, navegue até esta pasta (`boot_login/`) pelo terminal e execute:

```bash
python main.py
```

> ### ⚠️ Atenção: Verificação de Duas Etapas (2FA)
>
> Se a sua conta do Instagram tiver a verificação de duas etapas ativada, o robô irá detectar a tela de verificação e fará uma pausa.
>
> **Fique atento ao terminal!** A seguinte mensagem aparecerá:
>
> ```text
> ATENÇÃO: Verificação de duas etapas detectada.
> Por favor, digite o código de 6 dígitos que você recebeu e pressione Enter:
> ```
>
> Nesse momento, verifique seu aplicativo autenticador ou SMS, digite o código de 6 dígitos no terminal e pressione `Enter` para que o bot possa continuar a execução.