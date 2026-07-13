from flask import Blueprint, request
from src.app import User, db
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
# localhost: 5000/users
app = Blueprint('user', __name__, url_prefix="/users")

@app.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data:
        return {"error":"JSON inválido"}, HTTPStatus.BAD_REQUEST
    # Isso evita erros quando o cliente envia um JSON inválido.
    user = User(username=data["username"],
                email=data["email"],
                password=generate_password_hash(data["password"]),
                role_id=data["role_id"],
                )
    
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {
            "error":"Usuário já existe"
        }, HTTPStatus.CONFLICT      
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role_id": user.role_id
    }, HTTPStatus.CREATED  

@app.route("/", methods=["GET"])
@jwt_required()
def list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return {
        "identity": get_jwt_identity(),
        "users":[
            {
                'id':user.id,
                'username':user.username,
                'role_id': user.role_id,
                'role': {
                    "id": user.role.id,
                    "name": user.role.name,
                } if user.role else {"id": None,"name":"sem_permissão"}
            }                                 
            for user in users
        ]            
    }, HTTPStatus.OK

#@app.route('/', methods=['GET','POST'])
#@jwt_required()
#def handle_user():
#    if request.method == 'POST':
#        result = _create_user()
#        if isinstance(result, tuple):
#        
#        return {
#            "id":result.id,
#            "username":result.username,
#            "email":result.email
#        }, HTTPStatus.CREATED
#    return {'identity':get_jwt_identity(),'users':_list_users()}

@app.route('/<int:user_id>')     
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
         'id':user.id,
         'username':user.username,
         "email": user.email
    }

@app.route('/<int:user_id>', methods=["PATCH"])     
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']        
    try:        
        db.session.commit()

    except IntegrityError:
        db.session.rollback
        return {
            'error':'username already exists'
        }, 409
    return {
        'id': user.id,
        'username': user.username,
        'email':user.email
    }

@app.route("/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)

    db.session.delete(user)
    db.session.commit()

    return {
        'message':'Usuário deletado com sucesso',
        'id': user_id,
        'username':user.username,
        'email':user.email
    },HTTPStatus.OK
    

    
