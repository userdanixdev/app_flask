# Flask API - Estudos com Flask, SQLAlchemy, Alembic, Autenticação, Autorização e Testes

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-red?logo=sqlalchemy)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-orange)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![JWT](https://img.shields.io/badge/JWT-Authentication-purple?logo=jsonwebtokens)
![Pytest](https://img.shields.io/badge/Pytest-Tests-0A9EDC?logo=pytest)
![REST%20API](https://img.shields.io/badge/API-REST-02569B)
![Poetry](https://img.shields.io/badge/Poetry-Dependency%20Management-60A5FA?logo=poetry)
![Git](https://img.shields.io/badge/Git-Version%20Control-F05032?logo=git)

## Sobre o projeto

Este projeto foi desenvolvido com o objetivo de aprofundar os principais conceitos do Flask para o desenvolvimento de aplicações web e APIs REST utilizando Python.

Durante sua construção, foram aplicadas práticas e padrões comuns no desenvolvimento de aplicações reais, incluindo organização modular, Application Factory, separação de rotas utilizando Blueprints, integração com banco de dados por meio do Flask-SQLAlchemy e gerenciamento da evolução do schema através do Flask-Migrate (Alembic).

O projeto também contempla recursos de autenticação e autorização com JWT, controle de acesso baseado em roles, operações CRUD e uma suíte de testes de integração utilizando Pytest, permitindo validar a interação entre endpoints, regras de autorização, ORM e banco de dados.

Embora tenha sido desenvolvido como um projeto de aprendizado e experimentação, sua estrutura busca seguir princípios de organização e desenvolvimento encontrados em aplicações profissionais, servindo também como laboratório prático para conceitos de Backend, APIs REST, persistência de dados, segurança e testes automatizados.

## Tecnologias utilizadas:

* Python
* Flask
* Flask-SQLAlchemy
* SQLAlchemy 2.x
* Flask-Migrate
* Alembic
* SQLite
* Click (CLI)
* Flask-JWT-Extended
* Pytest
* pytest-mock
* Poetry

## Estrutura da aplicação

* Application Factory Pattern
* Organização em módulos
* Blueprints
* Configuração centralizada da aplicação
* separação entre controllers e modelos
* ORM para acesso ao banco;
* migrations para controle da estrutura do banco;
* autenticação e autorização;
* testes de integração.

## Banco de dados

A aplicação utiliza SQLite durante o desenvolvimento.
O SQLAlchemy é utilizado como ORM para modelagem e persistência das entidades.

## Entidades

Atualmente a aplicação trabalha principalmente com:

* User
* Role
* Post

### Relacionamentos:
```
Role
 │
 └── 1:N ── User
              │
              └── 1:N ── Post
```

**Um usuário pertence a uma Role e pode possuir vários Posts.**
***Os Posts possuem uma relação com o usuário responsável pela publicação.***

## Autenticação JWT

**A autenticação da API foi implementada utilizando JWT (JSON Web Token).**

A autenticação permite:

- login de usuários;
- geração de access token;
- proteção de endpoints;
- identificação do usuário autenticado;
- utilização do token através do header Authorization.

Formato utilizado:

**Authorization**: Bearer <access_token>

A implementação inicial da autenticação está documentada na:

[Release v0.1.0 - Autenticação JWT](https://github.com/userdanixdev/app_flask/releases#release-v0.1.0)

## Autorização baseada em Roles

Foi implementada uma estrutura de autorização baseada em Roles.

*Atualmente a aplicação trabalha com diferentes níveis de acesso, permitindo diferenciar usuários administradores e usuários comuns.*

A estrutura foi introduzida na:

[Release v0.2.0 - Estrutura de Roles](https://github.com/userdanixdev/app_flask/releases#release-v0.2.0)

## Decorator de permissões:

A aplicação utiliza o decorator:

> @requires_role('admin')

para restringir determinados endpoints a usuários que possuem uma Role específica.

*O decorator realiza a verificação da Role do usuário autenticado antes da execução da função protegida.*

Exemplo:

```
@requires_role('admin')
def update_user():
    ...
```

A implementação foi adicionada na [Release v0.3.0 - Controle de permissões](https://github.com/userdanixdev/app_flask/releases#release-v0.3.0)

## Posts:

A aplicação possui um recurso de publicação de Posts.

Funcionalidades:

- criação de Posts;
- listagem de Posts;
- busca por ID;
- atualização;
- exclusão;
- associação automática ao usuário autenticado;
- autenticação JWT;
- autorização baseada no proprietário do Post;
- administradores possuem acesso aos Posts;
- usuários comuns podem modificar apenas os próprios Posts.

## Endpoints:

Método | Endpoint |	Descrição 
|--|--|--|
POST|	/posts|	Criar um Post
GET	|/posts|	Listar Posts
GET	|/posts/<id>|	Buscar Post por ID
PUT	|/posts/<id>|	Atualizar Post
DELETE|	/posts/|<id>	Excluir Post

A implementação dos Posts foi documentada na:

[Release v0.4.0 - Posts e Controle de Acesso](https://github.com/userdanixdev/app_flask/releases#release-v0.4.0)

## Usuários:

A API disponibiliza operações para gerenciamento de usuários.

Método	|Endpoint|	Descrição
|--|--|--|
GET|	/users|	Listar usuários
POST|	/users|	Criar usuário
GET	|/users/<id>|	Buscar usuário
PATCH|	/users/<id>|	Atualizar usuário
DELETE|	/users/<id>	|Remover usuário

*O acesso aos endpoints é controlado de acordo com a autenticação e as permissões do usuário.*

## Testes automatizados:

O projeto possui uma estrutura de testes utilizando Pytest.

Os testes de integração validam o comportamento da API através das rotas reais da aplicação, utilizando um banco SQLite em memória.

### Estrutura das fixtures

O arquivo conftest.py centraliza fixtures utilizadas pelos testes, incluindo:

- criação da aplicação de teste;
- banco SQLite em memória;
- cliente HTTP;
- usuário administrador;
- usuário comum;
- segundo usuário comum;
- tokens JWT.

A implementação dos Testes foi documentada na:

[Release v0.5.0 - Testes de Integração e Qualidade](https://github.com/userdanixdev/app_flask/releases/tag/v0.5.0)

Exemplo:
```
tests/
│
├── conftest.py
│
└── integration/
    └── controllers/
        ├── test_post.py
        ├── test_role.py
        └── test_user.py
```        

## Execução dos testes

Para executar todos os testes de integração:

```pytest tests/integration```

Os testes verificam diferentes cenários, incluindo:

- autenticação;
- autorização;
- criação de usuários;
- busca de usuários;
- criação de Posts;
- atualização de Posts;
- exclusão de Posts;
- acesso sem autenticação;
- acesso sem permissão;
- recursos inexistentes;
- criação de Roles;
- duplicidade de Roles.

## Recursos estudados:

Durante o desenvolvimento foram praticados conceitos importantes do ecossistema Flask:

* Flask;
* Application Factory;
* Blueprints;
* rotas;
* Request JSON;
* Response JSON;
* HTTP Status Codes;
* SQLAlchemy ORM;
* Foreign Keys;
* relacionamentos;
* Flask-Migrate;
* Alembic;
* SQLite;
* JWT;
* Roles;
* autorização;
* decorators;
* CRUD;
* tratamento de exceções;
* IntegrityError;
* Pytest;
* fixtures;
* testes de integração;
* banco de dados em memória.

## Estrutura do projeto:
```
app_flask/
│
├── migrations/
│
├── src/
│   ├── controllers/
│   │   ├── user.py
│   │   ├── post.py
│   │   └── ...
│   │
│   ├── app.py
│   ├── db.py
│   └── schema.sql
│
├── tests/
│   ├── conftest.py
│   │
│   └── integration/
│       └── controllers/
│           ├── test_post.py
│           ├── test_role.py
│           └── test_user.py
│
│
├── pyproject.toml
├── poetry.lock
├── README.md

```
## Migrações:

O controle da estrutura do banco é realizado utilizando ```Flask-Migrate/Alembic.```

- Criar uma migration
```flask db migrate -m "Descrição da alteração"``` 
- Aplicar migrations
```flask db upgrade```
- Reverter uma migration
```flask db downgrade```

## Executando o projeto

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

## Criar usuário:

POST /users/
```
Body:

{
    "username": "Paul McCartney",
    "email": "paul@example.com",
    "password": "test",
    "role_id": 1
}
```
## Criar Post:
```
POST /posts/
```
> O usuário autenticado é associado automaticamente ao Post.

---

# SQLite vs PostgreSQL

## SQLite

O **SQLite** é um banco de dados relacional embarcado (embedded), armazenando todas as informações em um único arquivo local (`.sqlite`).

### Quando utilizar

- estudos;
- desenvolvimento local;
- protótipos;
- aplicações pequenas;
- testes automatizados;
- ambientes com baixa concorrência.

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
- Aplicações com muitos usuários 
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
class Use r(db.Model):
    id =  mapped_column(Integer, primary_key=True)
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

## Histórico de Releases:

[- v0.1.0 - Autenticação JWT](https://github.com/userdanixdev/app_flask/releases#release-v0.1.0)

> Implementação da autenticação utilizando JWT.

[- v0.2.0 - Estrutura de Roles](https://github.com/userdanixdev/app_flask/releases#release-v0.2.0)

> Implementação da estrutura inicial de Roles para autorização.

[- v0.3.0 - Controle de permissões](https://github.com/userdanixdev/app_flask/releases#release-v0.3.0)

> Implementação do decorator para controle de acesso baseado em Roles.

[- v0.4.0 - Posts](https://github.com/userdanixdev/app_flask/releases#release-v0.4.0)

> Implementação da entidade Post, CRUD completo, relacionamento User ↔ Post e regras de autorização.

[- v0.5.0 - Testes de integração](https://github.com/userdanixdev/app_flask/releases/tag/v0.5.0)

> Implementação e organização da estrutura de testes de integração utilizando Pytest, fixtures e banco SQLite em memória.

# Objetivo

Este projeto foi desenvolvido exclusivamente para fins de estudo e evolução prática em desenvolvimento backend com Python.

*O foco principal foi compreender a arquitetura do Flask, o funcionamento do SQLAlchemy, a criação de APIs REST e a organização de aplicações escaláveis seguindo boas práticas do ecossistema Python.*


## Autor:

*Desenvolvido por Daniel M. França como projeto de estudos em Flask, desenvolvimento Backend com Python, SQLAlchemy, autenticação, autorização e testes automatizados.*

