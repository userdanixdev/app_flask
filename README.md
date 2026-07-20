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

# SQLite vs PostgreSQL

## SQLite

O **SQLite** é um banco de dados relacional embarcado (embedded), armazenando todas as informações em um único arquivo local (`.sqlite`).

### Quando utilizar

- Estudos e aprendizado
- Desenvolvimento local
- Protótipos
- Aplicações pequenas
- Testes automatizados
- Sistemas com poucos acessos simultâneos

### Vantagens

- Não requer instalação de servidor
- Configuração simples
- Leve e rápido para pequenos projetos
- Fácil de transportar (apenas um arquivo)
- Integração simples com Flask e SQLAlchemy

### Desvantagens

- Baixa concorrência para escrita
- Escalabilidade limitada
- Recursos avançados reduzidos
- Não recomendado para aplicações com muitos usuários

---

## PostgreSQL

O **PostgreSQL** é um Sistema Gerenciador de Banco de Dados (SGBD) cliente-servidor, projetado para aplicações de médio e grande porte.

### Quando utilizar

- APIs REST em produção
- Sistemas corporativos
- Aplicações com muitos usuários simultâneos
- Projetos escaláveis
- Ambientes em nuvem (AWS, Azure, GCP)

### Vantagens

- Alta performance
- Excelente concorrência
- Grande escalabilidade
- Controle de usuários e permissões
- Transações robustas (ACID)
- Backup e recuperação
- Suporte a JSON, Arrays, UUID e outros tipos avançados

### Desvantagens

- Requer instalação e configuração
- Administração mais complexa
- Maior consumo de recursos

---

# Comparação

| Característica | SQLite | PostgreSQL |
|----------------|--------|------------|
| Instalação | Não necessita servidor | Necessita servidor |
| Armazenamento | Arquivo local (.sqlite) | Banco em servidor |
| Configuração | Muito simples | Mais complexa |
| Performance | Boa para projetos pequenos | Excelente para projetos médios e grandes |
| Concorrência | Limitada | Alta |
| Escalabilidade | Baixa | Alta |
| Recursos avançados | Básicos | Avançados |
| Produção | Apenas aplicações simples | Recomendado |

---

# SQLAlchemy facilita a migração

Uma das principais vantagens do **SQLAlchemy ORM** é abstrair a comunicação com o banco de dados.

Os modelos permanecem praticamente iguais:

```python
class User(db.Model):
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String)
```

Na maioria dos casos, a principal alteração ocorre apenas na string de conexão.

SQLite:

```python
SQLALCHEMY_DATABASE_URI = "sqlite:///app.sqlite"
```

PostgreSQL:

```python
SQLALCHEMY_DATABASE_URI = (
    "postgresql://usuario:senha@localhost:5432/app_flask"
)
```

---

# Resumo

- **SQLite** é ideal para estudos, desenvolvimento local e pequenos projetos.
- **PostgreSQL** é recomendado para aplicações em produção, com maior volume de dados, múltiplos usuários e necessidade de escalabilidade.
- Utilizando **SQLAlchemy ORM**, é possível migrar entre os dois bancos com poucas alterações no código da aplicação.

## 🔐 Autenticação JWT

A autenticação da API foi implementada na versão **v0.1.0**.

📖 Consulte os detalhes da implementação na **Release v0.1.0**:
https://github.com/userdanixdev/app_flask/releases/tag/v0.1.0

### 🔐 Autorização: Estrutura de Autorização e Gerenciamento de Roles

Nesta versão foi implementada a estrutura inicial de autorização baseada em roles, preparando a aplicação para controle de acesso por nível de permissão.

📖 Consulte os detalhes da implementação na **Release v0.2.0**:
https://github.com/userdanixdev/app_flask/releases/tag/v0.2.0

### 🔐 Autorização: Decoradores ( Permissões )

Nessa feature temos a implementação do decorator `@requires_role()`. e controle de acesso baseado em Roles.

📖 Consulte os detalhes da implementação na **Release v0.3.0**:
https://github.com/userdanixdev/app_flask/releases/tag/v0.3.0

---

## 🚀 Nova Funcionalidade - Posts

### ✨ O que foi adicionado

Implementação da entidade **Post**, permitindo que usuários autenticados criem e gerenciem publicações na API.

### Funcionalidades

* Implementação do modelo `Post`.
* Relacionamento **User ↔ Post** (1:N).
* CRUD de Posts.
* Associação automática do post ao usuário autenticado.
* Controle de autorização para edição e exclusão de posts.
* Administradores possuem acesso total.
* Usuários comuns podem modificar apenas os próprios posts.
* Integração com autenticação JWT.

### Endpoints

| Método   | Endpoint      | Descrição             |
| -------- | ------------- | --------------------- |
| `POST`   | `/posts`      | Criar um novo post    |
| `GET`    | `/posts`      | Listar todos os posts |
| `GET`    | `/posts/<id>` | Buscar um post por ID |
| `PUT`    | `/posts/<id>` | Atualizar um post     |
| `DELETE` | `/posts/<id>` | Excluir um post       |

📖 Consulte os detalhes da implementação na **Release v0.4.0**:

https://github.com/userdanixdev/app_flask/releases/tag/v0.4.0

## Autor

Desenvolvido por **Daniel** como projeto de estudos em Flask e desenvolvimento Backend com Python.
