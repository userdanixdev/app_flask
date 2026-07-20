# Adidionar a entidade Post que permite usuários autenticados criarem publicações.
# Cada post pertence a um usuário e um usuário pode ter vários posts.
# Administradores possuem acesso total, enquanto usuários comuns podem modificar apenas seus próprios 
# 
# posts.

## Boas práticas:
## Criar branch feature post:
## Escopo:

# Model Post em app.py ( Versionado no alembic)
# Relacionamento User ↔ Post ( app.py)  ( Versionado no Alembic)
# Migration do banco ( Versionado com Alembic )
# Controller post.py
# CRUD completo
# Regras de autorização (autor ou admin)
# Testes via Postman
# Documentação da API

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from src.app import db, Post, User

app = Blueprint("post", __name__, url_prefix="/posts")

@app.route("/", methods=["POST"])
@jwt_required()
def create_post():
    # Receber JSON:
    data = request.get_json()
    if not data:
        return{
            "error":"JSON inválido."
        }, HTTPStatus.BAD_REQUEST
    if "title" not in data or "body" not in data:
        return {"error":"Os campos 'title' e 'body' são obrigatórios."}, HTTPStatus.BAD_REQUEST
    # Obter usuário logado:
    user_id = get_jwt_identity()
    # Buscar usuário:
    user = db.session.get(User, user_id)
    if not user:
        return {
            "error":"Usuário não encontrado."            
        }, HTTPStatus.NOT_FOUND
    post = Post(
        title=data["title"],
        body=data["body"],
        author_id=user.id
    )
# Salvar:
    try:
        db.session.add(post)
        db.session.commit()
# alguns bancos o valor só fica disponível após sincronizar o objeto com o banco        
        db.session.refresh(post)
    except IntegrityError:
        db.session.rollback()        
        return {
            "error":"Erro ao salvar o post."
        }, HTTPStatus.BAD_REQUEST
    return {
            "message":"Post criado com sucesso",
            "id":post.id,
            "title":post.title,
            "body":post.body,
            "author_id":post.author_id,
            "created": post.created.isoformat()
        }, HTTPStatus.CREATED

@app.route("/", methods=["GET"])
@jwt_required()
def list_posts():
    # Buscar os posts:
    query = db.select(Post)
    posts = db.session.execute(query).scalars().all()
    return {
        "identity":get_jwt_identity(),
        "posts":[
            {
                "id":post.id,
                "title":post.title,
                "body":post.body,
                "created":post.created.isoformat(),
                "author":{
                    "id":post.author.id,
                    "username":post.author.username,
                }
            }
            for post in posts
        ] 
    },HTTPStatus.OK
    
@app.route('/<int:post_id>')    
@jwt_required()
def get_post(post_id):
    post = db.get_or_404(Post,post_id)
    return {
        "identity":get_jwt_identity(),
        "post":{
            "id":post.id,
            "title":post.title,
            "body":post.body,
            "created":post.created.isoformat(),
            "author":{
                "id":post.author.id,
                "username":post.author.username,
            }
        }
    }, HTTPStatus.OK

@app.route('/<int:post_id>', methods=["PATCH"])   
@jwt_required()
def update_post(post_id):
    # Busca o post:
    post = db.get_or_404(Post, post_id)
    # Dados enviados:
    data = request.get_json()
    if not data:
        return{
            "error":"JSON inválido."
        }, HTTPStatus.BAD_REQUEST
    # Usuário autenticado:
    user_id = get_jwt_identity()
    user = db.get_or_404(User,user_id)
    # Verificar autorização
    if user.role.name != "admin" and post.author_id != user.id:
        return{
            "error":"Você não possui permissão para editar este post."
        }, HTTPStatus.FORBIDDEN
    # Atualização parcial:
    if "title" in data:
        post.title = data["title"]    
    if "body" in data:
        post.body = data["body"]
    try:         
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {
            "error": "Erro ao atualizar o post."
        }, HTTPStatus.BAD_REQUEST
    return {
        "message":"Post atualizado com sucesso.",
        "post":{
            "id":post.id,
            "title":post.title,
            "body":post.body,
            "created":post.created.isoformat(),
            "author":{
                "id":post.author.id,
                "username":post.author.username
            }
        }
    }, HTTPStatus.OK 

@app.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    # Buscar o post:
    post = db.get_or_404(Post,post_id)
    # Buscar o usário autenticado:
    user_id = get_jwt_identity()
    user = db.get_or_404(User,user_id)
    # Verificar autorização:
    if user.role.name != "admin" and post.author_id != user.id:
        return{
            "error":"Você não possui permissão para excluir este post."

        }, HTTPStatus.NO_CONTENT
    try:
        db.session.delete(post)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {
            "error":"Erro ao excluir o post."
        }, HTTPStatus.BAD_REQUEST
    return {
        "message":"Post excluído com sucesso."
    }, HTTPStatus.OK
            
