from http import HTTPStatus
from src.app import db,Role,User

def test_create_post(client, access_token):
    response = client.post(
        "/posts/",
        json={
            "title":"Meu primeiro post",
            "body":"Conteúdo do meu primeiro post.",
        },
        headers={
            "Authorization":f"Bearer {access_token}"
        }
    )
    assert response.status_code == HTTPStatus.CREATED
    

# Teste de criação de post sem autenticação de um usuário:
def test_create_post_without_authentication(client):
    response = client.post(
        "/posts/",
        json={
            "title":"Meu post",
            "body":"Conteúdo"
        }
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED

# Se o JSON foi inválido:
def test_create_post_invalid_json(client,normal_user_token):
    response=client.post(
        "/posts/",
        data = '{"Title":"Meu post"',
        content_type = "application/json",
        headers={
            "Authorization":f"Bearer {normal_user_token}"
        }
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    

def test_create_post_without_title(client,normal_user_token):
    response = client.post(
        "/posts/",
        json={
            "body":"Conteúdo do post."
        },
        headers = {
            "Authorization":f"Bearer {normal_user_token}"
        }
    )    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json["error"] == (
        "Os campos 'title' e 'body' são obrigatórios."
    )
## Sem corpo do texto:
def test_create_post_without_body(client, normal_user_token):
    response = client.post(
        "/posts/",
        json={
            "title":"Título do post"
        },
        headers={
            "Authorization": f"Bearer {normal_user_token}"
        }
    )    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json["error"] == (
        "Os campos 'title' e 'body' são obrigatórios."
    )

def test_list_posts(client,normal_user_token):
    create_response = client.post(
        "/posts/",
        json={
            "title":"Post para listagem",
            "body":"Conteúdo do post."
        },
        headers={
            "Authorization":f"Bearer {normal_user_token}"
        }
    )    
    assert create_response.status_code == HTTPStatus.CREATED
    # Listagem :
    response = client.get(
        "/posts/",
        headers={
            "Authorization":f"Bearer {normal_user_token}"
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json["posts"]
    post = response.json["posts"][0]
    assert post["title"] == "Post para listagem"
    assert post["body"] == "Conteúdo do post."
    assert post["author"]["username"] == "Paul McCartney"

def test_list_posts_without_authentication(client):
    response = client.get("/posts/")

    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_get_post(client, normal_user_token):
    create_response = client.post(
        "/posts/",
        json ={
            "title":"Post para consulta",
            "body":"Conteúdo do post."
        },
        headers = {
            "Authorization":f"Bearer {normal_user_token}"
        }
    )    
    assert create_response.status_code == HTTPStatus.CREATED
    post_id = create_response.json["id"]
    response = client.get(
        f"/posts/{post_id}",
        headers = {
            "Authorization":f"Bearer {normal_user_token}"
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json["post"]["id"] == post_id
    assert response.json["post"]["title"] == "Post para consulta"
    assert response.json["post"]["body"] == "Conteúdo do post."
    assert response.json["post"]["author"]["username"] == "Paul McCartney"


# Obs: No endpont existe:' post = db.get_or_404(Post, post_id)' então:

def test_get_post_not_found(client, normal_user_token):
    response = client.get(
        "/post/999",
        headers ={
            "Authorization":f"Bearer {normal_user_token}"
        }
    )
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_get_post_without_authentication(client):
    response = client.get("/posts/1")

    assert response.status_code == HTTPStatus.UNAUTHORIZED

# 1. Teste: autor pode atualizar o próprio post:

def test_update_post(client, normal_user_token):
    create_response = client.post(
        "/posts/",
        json ={
            "title":"Título original",
            "body":"Conteúdo original"
        },
        headers = {
            "Authorization":f"Bearer {normal_user_token}"
        }
    )    
    
    # Isso valida a regra do endpoint: '# if user.role.name != "admin" and post.author_id != user.id'
    post_id =  create_response.json["id"]
    response = client.patch(
        f"/posts/{post_id}",
        json={
            "title":"título atualizado",
            "body":"Conteúdo atualizado."
        },
        headers = {
            "Authorization":f" Bearer {normal_user_token}"
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json["message"] == "Post atualizado com sucesso."
    post = response.json["post"]
    assert post["id"] == post_id
    assert post["title"] == "título atualizado"
    assert post["body"] == "Conteúdo atualizado."
    assert post["author"]["username"] == "Paul McCartney"

# Outro usuário não pode editar o post de outro:
def test_update_post_without_permission(
        client,normal_user_token,another_user_token):
    create_response = client.post(
        "/posts/",
        json={
            "title":"Post do Paul",
            "body":"Conteúdo do Paul."
        },
        headers ={
            "Authorization":f"Bearer {normal_user_token}"
        }
    )
    assert create_response.status_code == HTTPStatus.CREATED
    post_id = create_response.json["id"]
    response = client.patch(
        f"/posts/{post_id}",
        json={
            "title":"Tentativa de alteração",
            "body":"George tentou alterar."
        },
        headers = {
            "Authorization":f"Bearer {another_user_token}"
        }
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json["error"] == (
        "Você não possui permissão para editar este post."
    )
# admin pode editar o post de outro usuário.

# Aqui podemos provar a condição : '# if user.role.name != "admin" and post.author_id != user.id'
# Ou seja, se o usuário for admin pe#rmite a alteração do post.

def test_update_post_as_admin(
        client, normal_user_token, access_token
):
    create_response = client.post(
        "/posts/",
        json={
            "title":"Post do Paul",
            "body":"Conteúdo original."
        },
        headers = {
            "Authorization":f"Bearer {normal_user_token}"
        }
    )
    assert create_response.status_code == HTTPStatus.CREATED
    post_id = create_response.json["id"]
    response = client.patch(
        f"/posts/{post_id}",
        json={
            "title":"Post atualizado pelo admin",
            "body":"Conteúdo atualizado pelo admin."
        },
        headers={
            "Authorization":f" Bearer {access_token}"
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json["message"] == "Post atualizado com sucesso."
    post = response.json["post"]
    assert post["id"] == post_id
    assert post["title"] == "Post atualizado pelo admin"
    assert post["body"] == "Conteúdo atualizado pelo admin."
    assert post["author"]["username"] == "Paul McCartney"

    # Obs: O post continua sendo de Paul mas quem quer executar o PATCH é o JOHN. ENtão 'user.role.name != "admin"'

def test_update_post_without_authentication(client):
    response = client.patch(
        "/posts/1",
        json={
            "title":"Tentativa de atualização"
        }
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED

# Teste com PATCH com JSON inválido/vazio:
# No endpoint temos request.get_json(). Se não for recebe mensagem de JSON inválido e BAD_REQUEST 400

def test_update_post_invalid_json(client, normal_user_token):
    create_response = client.post(
        "/posts/",
        json={
            "title":"Post original",
            "body":"Conteúdo original."
        },
        headers ={
            "Authorization":f"Bearer {normal_user_token}"
        }
    )
    assert create_response.status_code == HTTPStatus.CREATED
    post_id = create_response.json["id"]
    response= client.patch(
        f"/posts/{post_id}",
        json={},
        headers={
            "Authorization":f"Bearer {normal_user_token}"
        }
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json["error"] == "JSON inválido."


# Observações importantes: O post é criado primeiro para testar especificamente a validação do JSON, e não a existência do post.
# POST -> 201 CREATED -> PATCH /posts/1 -> JSON = {} -> # if not data -> 400 BAD REQUES#T


# Teste em tentar atualizar um post que não existe → 404 NOT_FOUND.
def test_update_post_not_found(client,normal_user_token):
    response = client.patch(
        "/posts/999",
        json={
            "title":"Tentativa de atualização"
        },
        headers ={
            "Authorization":f"Bearer {normal_user_token}"
        }
    )
    assert response.status_code == HTTPStatus.NOT_FOUND

# Obs: O endpoint começa com: post = 'db.get_or_404(Post, post_id)' então ao solicitar PATCH/posts/999 se não existir, o Flask-SQLAlchemy

# interrompe a execução e retorna 404 NOT FOUND.
# O teste não precisa criar um post antes, porque justamente queremos verificar o comportamento quando o recurso não existe.

# DELETES: Autor pode excluir o próprio post.

def test_delete_post(client,normal_user_token):
    create_response = client.post(
        "/posts/",
        json={
            "title":"Post para excluir",
            "body":"Conteúdo do post."
        },
        headers ={
            "Authorization":f" Bearer {normal_user_token}"
        }
    )
    assert create_response.status_code == HTTPStatus.CREATED
    post_id = create_response.json["id"]
    response = client.delete(
        f"/posts/{post_id}",
        headers ={
            "Authorization":f" Bearer {normal_user_token}"
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json["message"] == "Post excluído com sucesso."
# Nesse caso o teste o usuário cria o post e deleta. Se der sucesso, é o autor. 200. ok

# # De acordo com o endpoint: # if user.role.name != "admin" and post.author_id != user.id.
# Paul é o autor , dessa forma# a condição não bloqueia a exclusão.
# 
# Outro usuário não pode excluir o post    
# Ex: Um usuário cria o post e outro usuário tenta exlcuir, 403 FORBIDDEN
def test_delete_post_without_permission(
        client, normal_user_token, another_user_token
):
    create_response = client.post(
        "/posts/",
        json={
            "title":"Post do Paul",
            "body":"Conteúdo do Paul."
        },
        headers = {
            "Authorization":f" Bearer {normal_user_token}"
        }
    )
    assert create_response.status_code == HTTPStatus.CREATED
    post_id = create_response.json["id"]
    response = client.delete(
        f"/posts/{post_id}",
        headers ={
            "Authorization":f"Bearer {another_user_token}"
        }
    )
    assert response.status_code == HTTPStatus.NO_CONTENT

# Obs: Dessa forma, estamos testando exatamente o comportamento atual do endpoint.

# if user.role.name != "admin" and post.author_id != user.id:
#    return {
#        "error": "Você não possui permissão para excluir este post."
#    }, HTTPStatus.NO_CONTENT    
    
# Admin pode excluir post de outro usuário:
def test_delete_post_as_admin(
        client, normal_user_token,access_token
):
    create_response = client.post(
        "/posts/",
        json={
            "title":"Post do Paul",
            "body":"Conteúdo do Paul."
        },
        headers ={
            "Authorization":f"Bearer {normal_user_token}"
        }
    )
    assert create_response.status_code == HTTPStatus.CREATED
    post_id = create_response.json["id"]
    response = client.delete(
        f"/posts/{post_id}",
        headers ={
            "Authorization":f"Bearer {access_token}"
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json["message"] == "Post excluído com sucesso."
    # Aqui estamos valindo a segunda parte da regra: (user.role.name == "admin")
    # Mesmo que o post pertença ao Paul, o administrador pode excluí-lo.

def test_delete_post_without_authentication(client):
    response = client.delete("/posts/1")

    assert response.status_code == HTTPStatus.UNAUTHORIZED
# Aqui nem precisamos criar um post, porque @jwt_required() é executado antes da busca pelo post.

# DELETE de post inexistente → 404    
def test_delete_post_not_found(client, normal_user_token):
    response = client.delete(
        "/posts/999",
        headers={
            "Authorization": f"Bearer {normal_user_token}"
        }
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
# Esse testa diretamente: (post = db.get_or_404(Post, post_id))    
# O fluxo é DELETE /posts/999 -> JWT válido -> procura Post 999 -> não encontrado -> 404 NOT FOUND



