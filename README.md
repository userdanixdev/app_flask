# Flask API - Estudos com Flask, SQLAlchemy e Alembic

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![License](https://img.shields.io/badge/license-MIT-green)

## Sobre o projeto

Este projeto foi desenvolvido com o objetivo de estudar os principais conceitos do framework **Flask** para desenvolvimento de aplicações web e APIs REST utilizando Python.

Durante o desenvolvimento foram aplicadas diversas boas práticas utilizadas em projetos reais, como organização em módulos, utilização do padrão **Application Factory**, separação das rotas através de **Blueprints**, integração com banco de dados utilizando **Flask-SQLAlchemy** e controle de versões do banco com **Flask-Migrate (Alembic)**.

Embora seja um projeto de estudos, sua estrutura segue padrões próximos aos encontrados em aplicações profissionais.

---

# Tecnologias utilizadas

* Python
* Flask
* Flask-SQLAlchemy
* SQLAlchemy 2.x
* Flask-Migrate
* Alembic
* SQLite
* Click (CLI)
* Git
* GitHub

---

# Funcionalidades implementadas

## Estrutura da aplicação

* Application Factory Pattern
* Organização em módulos
* Blueprints
* Configuração centralizada da aplicação

## Banco de dados

* Integração com SQLite

* Modelagem utilizando SQLAlchemy ORM

* Criação das entidades:

* User

* Post

* Relacionamentos utilizando Foreign Keys

* Migrações com Alembic

---

# Recursos da API

## Usuários

* Criar usuário
* Listar usuários
* Buscar usuário por ID
* Atualizar usuário
* Remover usuário

Endpoints:

```text
GET     /users
POST    /users
GET     /users/<id>
PATCH   /users/<id>
DELETE  /users/<id>
```

---

# Recursos estudados

Durante a implementação foram praticados conceitos importantes do ecossistema Flask:

* Rotas
* Blueprints
* Request JSON
* Response JSON
* HTTP Status Code
* SQLAlchemy ORM
* Migrations
* CLI Commands
* SQLite
* Organização em camadas
* CRUD completo
* Tratamento de exceções (IntegrityError)

---

# Estrutura do projeto

```text
app_flask/

│
├── migrations/
│
├── src/
│   ├── controllers/
│   │     ├── user.py
│   │     └── post.py
│   │
│   ├── app.py
│   ├── db.py
│   └── schema.sql
│
├── instance/
│
├── pyproject.toml
├── poetry.lock
├── README.md
└── hello.py
```

---

# Modelo de dados

## User

| Campo    | Tipo    |
| -------- | ------- |
| id       | Integer |
| username | String  |
| email    | String  |
| active   | Boolean |

---

## Post

| Campo     | Tipo        |
| --------- | ----------- |
| id        | Integer     |
| title     | String      |
| body      | String      |
| created   | DateTime    |
| author_id | Foreign Key |

---

# Executando o projeto

Clone o repositório

```bash
git clone https://github.com/userdanixdev/app_flask.git
```

Entre na pasta

```bash
cd app_flask
```

Instale as dependências

```bash
poetry install
```

Ative o ambiente virtual

```bash
poetry shell
```

Execute a aplicação

```bash
flask --app src.app run
```

---

# Migrações

Criar uma migration

```bash
flask db migrate -m "Descrição da alteração"
```

Aplicar as alterações

```bash
flask db upgrade
```

---

# Exemplo de requisição

### Criar usuário

```http
POST /users
```

Body

```json
{
    "username": "daniel",
    "email": "daniel@email.com"
}
```

Resposta

```json
{
    "message": "User created"
}
```

---

# Conceitos praticados

* Flask
* APIs REST
* CRUD
* SQLAlchemy ORM
* Flask CLI
* Alembic
* Migrations
* SQLite
* Organização em módulos
* Application Factory Pattern
* Blueprints
* Tratamento de exceções
* HTTP Status

---

# Objetivo

Este projeto foi desenvolvido exclusivamente para fins de estudo e evolução prática em desenvolvimento backend com Python.

O foco principal foi compreender a arquitetura do Flask, o funcionamento do SQLAlchemy, a criação de APIs REST e a organização de aplicações escaláveis seguindo boas práticas do ecossistema Python.

---

## 🔐 Autenticação JWT

A autenticação da API foi implementada na versão **v0.1.0**.

📖 Consulte os detalhes da implementação na **Release v0.1.0**:
https://github.com/userdanixdev/app_flask/releases/tag/v0.1.0


# Próximos passos

* Hash de senhas com Werkzeug
* Validação de dados com Pydantic
* Testes automatizados com Pytest
* Docker
* Documentação da API com Swagger/OpenAPI
* Deploy da aplicação

---

## Autor

Desenvolvido por **Daniel** como projeto de estudos em Flask e desenvolvimento Backend com Python.
