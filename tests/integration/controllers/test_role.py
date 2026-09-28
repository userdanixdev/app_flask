from http import HTTPStatus
from src.app import db,Role,User

def test_create_role(client,access_token):
    response = client.post(
        '/roles/',
        json={
            'name':'normal'
        },
        headers={
            'Authorization':f'Bearer {access_token}'
        }
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {
        'message':'Role created'
    }
    role = db.session.execute(
        db.select(Role).where(Role.name == 'normal')
    ).scalar_one()
    assert role.name == 'normal'

# Teste para JSON inválidos:
def test_create_role_invalid_json(client,access_token):
    response = client.post(
        '/roles/',
        json={},
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {
        'error': 'JSON inválido'
    }
## Teste para ROLES DUPLICATAS:
def test_create_role_duplicate(client, access_token):
    role = Role(name = 'normal')
    db.session.add(role)
    db.session.commit()    
    response = client.post(
        '/roles/',
        json={
            'name':'normal'
        },
        headers={
            'Authorization':f'Bearer {access_token}'
        }
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == {
        'error':'Usuário já existe'
    }
# Teste para listar roles:
def test_list_roles(client, access_token):
    role_normal = Role(name='normal')

    db.session.add(role_normal)
    db.session.commit()        
    response = client.get(
        '/roles/',
        headers={
            'Authorization':f'Bearer {access_token}'
        }
    )
    assert response.status_code == HTTPStatus.OK
    roles = {
        role['name']: role
        for role in response.json
    }
    assert roles['admin']['name'] == 'admin'
    assert roles['admin']['users'] == [{
        'id':1,
        'username':'John Lennon'
    }]
    assert roles['normal']['name']=='normal'
    assert roles['normal']['users']==[]