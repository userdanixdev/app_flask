from flask import Blueprint, request
from src.app import User, db
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
# localhost: 5000/users
app = Blueprint('user', __name__, url_prefix="/users")

def _create_user():
    data = request.json
    user = User(username=data["username"],
                email=data["email"])
    db.session.add(user)
    db.session.commit()

def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            'id':user.id,
            'username':user.username,
        }
        for user in users
    ]            


@app.route('/', methods=['GET','POST'])
def handle_user():
    if request.method == 'POST':
        _create_user()
        return {'message': 'User created'}, HTTPStatus.CREATED
    else:
        return {'users':_list_users()}

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
    

    
