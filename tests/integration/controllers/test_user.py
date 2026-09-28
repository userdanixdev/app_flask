from http import HTTPStatus
from src.app import User, db, Role
from werkzeug.security import generate_password_hash


def test_get_user_sucess(client):
    role = Role(name = 'admin')
    db.session.add(role)
    db.session.commit()
    user = User(username='John Lennon',email='john@example.com', password=generate_password_hash('test'),role_id=role.id)
    db.session.add(user)
    db.session.commit()
    # Login:
    response = client.post(
        '/auth/login',
        json={
            'username':user.username,
            'password':'test'
        }
    )
                           
    assert response.status_code == HTTPStatus.OK
    access_token = response.json['access_token']

    # Busca usuário autenticado:
    response = client.get(
        f'/users/{user.id}',
        headers={
            'Authorization':f'Bearer {access_token}'
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        'id': user.id,
        'username': user.username,
        'email':user.email
    }

def test_get_user_not_found(client):
    role = Role(name = 'admin')
    db.session.add(role)
    db.session.commit()
    user = User(
        username='John Lennon',
        email='john@example.com',
        password=generate_password_hash('test'),
        role_id=role.id
    )
    db.session.add(user)
    db.session.commit()
    # Login:
    response = client.post(
        '/auth/login',
        json={
            'username': user.username,
            'password': 'test'
        }
    )

    assert response.status_code == HTTPStatus.OK

    access_token = response.json['access_token']
    ## Usuário inexistente:
    response = client.get(
        '/users/999',
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    
def test_list_users(client):
    role = Role(name = 'admin')
    db.session.add(role)
    db.session.commit()
    user = User(
        username='John Lennon',
        email='john@example.com',
        password=generate_password_hash('test'),
        role_id=role.id
        )
    db.session.add(user)
    db.session.commit()
    # Login:
    response = client.post(
        '/auth/login',
        json={
            'username': user.username,
            'password':'test'
            })
    assert response.status_code == HTTPStatus.OK
    access_token = response.json["access_token"]
    # Lista de usuários:
    response = client.get(
        '/users/',
        headers={
            'Authorization': f'Bearer {access_token}'})
    
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "identity":str(user.id),
        "users":[
            {
                "id":user.id,
                "username":user.username,
                "role_id":user.role_id,
                "role":{
                    "id":user.role.id,
                    "name":user.role.name,
                }
            }
        ]
    }

def test_create_user(client, access_token):
    role = db.session.execute(
        db.select(Role).where(Role.name == 'admin')
    ).scalar_one()
    response = client.post(
        '/users/',
        json={
            'username': 'Paul McCartney',
            'email': 'paul@example.com',
            'password': 'test',
            'role_id': role.id
        },
        headers={"Authorization":f"Bearer {access_token}"}
    )
        
    assert response.status_code == HTTPStatus.CREATED
    user = db.session.execute(db.select(User).where(
        User.username == 'Paul McCartney')).scalar_one()
    
    assert response.json == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role_id': role.id
    }

    assert user is not None
    assert user.username == 'Paul McCartney'
    assert user.email == 'paul@example.com'
    assert user.role_id == role.id
    