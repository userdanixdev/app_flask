import pytest
from src.app import create_app, db, Role, User
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='function')
def app():
    app = create_app(
    {
        "SECRET_KEY" : "test",
        "SQLALCHEMY_DATABASE_URI":"sqlite://", ## Roda em memória
        ## Adiciona secret-key-jwt aqui (SETUP):
        "JWT_SECRET_KEY" : "test-super-secret",
    }
    )
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def access_token(client,admin_user):
        response = client.post(
            '/auth/login',
            json={
                'username':admin_user.username,
                'password':'test'
            }
        )
        return response.json["access_token"]           

@pytest.fixture()
def admin_user(app):
     role = Role(name='admin')                   
     db.session.add(role)
     db.session.commit()
     user = User(
          username = "John Lennon",
          email = 'john@example.com',
          password = generate_password_hash('test'),
          role_id=role.id
     )
     db.session.add(user)
     db.session.commit()
     return user

@pytest.fixture()
def normal_user(app):
    role = Role(name="normal")
    db.session.add(role)
    db.session.commit()
    user = User(
          username= "Paul McCartney",
          email= "paul@example.com",
          password=generate_password_hash("test"),
          role_id=role.id
     )        
    db.session.add(user)
    db.session.commit()
    return user        

@pytest.fixture()
def another_user(app):
     role = db.session.execute(
          db.select(Role).where(Role.name=="normal")
     ).scalar_one()
     user = User(
          username="George Harrison",
          email="george@example.com",
          password=generate_password_hash("test"),
          role_id=role.id
     )
     db.session.add(user)
     db.session.commit()
     return user

@pytest.fixture()
def normal_user_token(client,normal_user):
     response = client.post(
          "/auth/login",
          json={
               "username":normal_user.username,
               "password":"test"
          }
     )
     return response.json["access_token"]

@pytest.fixture()
def another_user_token(client,another_user):
     response=client.post(
          "/auth/login",
          json={
               "username":another_user.username,
               "password":"test"
          }
     )
     return response.json["access_token"]

# Obs: normal_user_token e another_user_token não são usuários. Eles são fixtures que geram o JWT de cada usuário

# As fixtures de usuários são responsáveis por criar os diferentes tipos de usuários que serão utilizados nos testes. A admin_user cria um usuário com a função admin, enquanto a normal_user cria um usuário comum que poderá ser autor de um post. A another_user cria um segundo usuário comum, permitindo testar situações em que um usuário tenta acessar ou modificar um post que pertence a outra pessoa.
# As fixtures de tokens têm outra finalidade. A access_token realiza o login do admin_user e retorna o JWT desse usuário. A normal_user_token faz o mesmo para o normal_user, retornando o JWT do usuário comum. Já a another_user_token retorna o JWT do segundo usuário comum.
# Esses tokens são necessários porque os endpoints do post.py utilizam @jwt_required(). Portanto, nos testes, precisamos enviar o token no cabeçalho Authorization para simular uma requisição autenticada.
# Dessa forma, conseguimos representar diferentes situações: o normal_user_token permite testar o autor autenticado alterando seu próprio post; o another_user_token permite testar outro usuário autenticado tentando alterar o post de alguém; e o access_token permite testar o administrador autenticado acessando ou modificando posts de outros usuários.
# Em resumo, as fixtures de usuário criam quem está no banco, enquanto as fixtures de token permitem que esses usuários façam requisições autenticadas durante os testes.

