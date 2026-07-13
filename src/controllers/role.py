from flask import Blueprint, request
from src.app import User, db, Role
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

# localhost: 5000/roles
app = Blueprint('role', __name__, url_prefix="/roles")

@app.route("/", methods=["POST"])
@jwt_required()
def create_role():
    data = request.get_json()
    if not data:
        return {"error":"JSON inválido"}, HTTPStatus.BAD_REQUEST
    # Isso evita erros quando o cliente envia um JSON inválido.
    role = Role(name=data['name'])
    try:
        db.session.add(role)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {
            "error":"Usuário já existe"
        }, HTTPStatus.CONFLICT      
    return {"message":"Role created"}, HTTPStatus.CREATED  

@app.route("/", methods=["GET"])
@jwt_required()
def list_roles():
    query = db.select(Role)
    roles = db.session.execute(query).scalars()

    return [
        {
            "id": role.id,
            "name": role.name,
            "users": [
                {
                    "id": user.id,
                    "username": user.username,
                }
                for user in role.user
            ],
        }
        for role in roles
    ], HTTPStatus.OK    