from http import HTTPStatus
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash



auth_bp = Blueprint("auth",__name__, url_prefix="/auth")

# Criar o método de login na WEB:

@auth_bp.route("/login",methods=["POST"])
def login():
    from src.app import db,User
    username = request.json.get("username",None)
    password = request.json.get("password",None)
    user = db.session.execute(
    db.select(User).where(User.username == username)
).scalar_one_or_none()

    if user is None:
        return {"msg": "Usuário ou senha inválidos"}, HTTPStatus.UNAUTHORIZED

    if not check_password_hash(user.password, password):
        return {"msg": "Usuário ou senha inválidos"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))

    return {"access_token": access_token}
        