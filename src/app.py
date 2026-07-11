import os
from flask import Flask, current_app
import click
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from flask_migrate import Migrate
from sqlalchemy import Boolean

# A biblioteca: "os" ajuda a manipular pastas e caminhos para o projeto.
# "Flask" -> cria a aplicação web
# current_app -> refere-se ao app Flask atual dentro do contexto da aplicação
# click -> cria comandos CLI personalizados (flask init-db)


#Base = declarative_base() # ATENÇÃO! NÃO PRECISA REFERENCIAR Porque o Flask-SQLAlchemy já gerencia isso internamente.
#db = SQLAlchemy(model_class=Base)

db = SQLAlchemy()
migrate = Migrate()

from sqlalchemy import Integer, String, func, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
# Esse é o padrão moderno do SQLAlchemy 2.x.
# Dessa forma o 'mapped' declara e mapeia a tipagem de linguagem de programação Python
# O "mapped_column" declara a tipagem tipo SQL


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String)
    active: Mapped[bool] = mapped_column(Boolean, default = True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r},active={self.active!r})"
    

class Post(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    title: Mapped[str]= mapped_column(String, nullable=False)
    body: Mapped[str]=mapped_column(String, nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    author_id: Mapped[int]= mapped_column(ForeignKey('user.id'))

    
    def __repr__(self:str):
        return f"Post(id={self.id!r}, username={self.title!r}, author_id={self.author_id!r})"

@click.command("init-db")
def init_db_command():
    db.create_all()
    click.echo("Initialized the database.")

# Atenção importante: O "create_all()" é bom para estudo e ruim para produção. Em projetos reais usamos:
# Flask-Migrate e Alembic. Porque alterações de schema precisam de migrações controladas.    

def create_app(test_config=None):
    # Criação e configuração do app com Flask:
    # Application Factory Pattern.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = "dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///banco_2.sqlite",
    )
    if test_config is None:
        app.config.from_pyfile("config.py",silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

# Registrar CLI comandos:
    db.init_app(app)
    app.cli.add_command(init_db_command)
    migrate.init_app(app, db)
    
# Iniciar a extensão
    @app.route("/")
    def index():
        return "<h1>Aplicação Flask funcionando!</h1>"
    from src.controllers import user, post
    
    app.register_blueprint(user.app)
    return app                        

# Registrar o app:

