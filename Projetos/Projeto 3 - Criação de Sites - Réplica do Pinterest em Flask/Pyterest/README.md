# Pyterest

Pyterest é um clone do Pinterest desenvolvido com Flask e SQLAlchemy. Ele permite que os usuários criem contas, façam
login, postem e gerenciem fotos.

## Índice

- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Contato](#contato)

## Instalação

1. Clone este repositório:
   ```sh
   git clone https://github.com/Cr0wtl3r/pyterest.git

2. Navegue até o diretório do projeto:
    ```sh
   cd pyterest
   ```

3. Crie um ambiente virtual:
   ```sh
   python -m venv .venv
   ```

4. Ative o ambiente virtual:
    * Para Windows:
      ```sh
      .\.venv\Scripts\activate
      ```
    * Para MacOS/Linux:
       ```sh
      source .venv/bin/activate
      ```

5. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

## Configuração:

1. Crie um arquivo .env no diretório raiz e adicione suas variáveis de ambiente:
   ```env
   SECRET_KEY=sua_chave_secreta
   DATABASE_URI=sqlite:///comunidade.db
   ```

2. Inicialize o banco de dados através do arquivo criar_banco.py:
   ```sh
      python criar_banco.py
   ```

## Uso

1. Execute o servidor:
   ```sh
   python main.py
   ```

2. Acesse o aplicativo no navegador em http://127.0.0.1:5000

## Estrutura do Projeto

```plaintext
pyterest/
│
├── static/
│   ├── css/
│   ├── img/
│   └── posts_pictures/
│
├── templates/
│   ├── errors/
│   ├── posts/
│   └── users/
│
├── pyterest/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── forms.py
│
├── .env
├── config.py
├── run.py
├── requirements.txt
└── README.md
```


## Tecnologias Utilizadas

* Python 3.12
* Flask
* Flask-Bcrypt
* Flask-Login
* Flask-SQLAlchemy
* Flask-Migrate
* WTForms

## Contato
Linkedin - [Albino Marques](https://www.linkedin.com/in/albino-marques/) (Cr0wtl3r)
