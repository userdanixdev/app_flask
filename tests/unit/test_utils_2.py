import pytest
from unittest.mock import Mock,patch
from src.utils.utils import eleva_quadrado
from src.controllers.decorator import requires_role
from http import HTTPStatus


@pytest.mark.parametrize("test_input, expected",[(2,4),(10,100),(3,9)])
def test_eleva_quadrado(test_input, expected):
    resultado = eleva_quadrado(test_input)
    assert resultado == expected

@pytest.mark.parametrize("test_input,exc_class,msg",[("a", TypeError, "unsupported operand type(s) for ** or pow(): 'str' and 'int'"),
                                                     (None,TypeError,"unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'")])
def test_eleva_quadrado_fail(test_input,exc_class,msg):
    with pytest.raises(exc_class) as exc:
        eleva_quadrado(test_input)
       
    assert str(exc.value) == msg

def test_requires_role(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"
    mock_get_jwt_identity = mocker.patch('src.controllers.decorator.get_jwt_identity')        
    mock_db_get_or_404 = mocker.patch('src.controllers.decorator.db.get_or_404', return_value = mock_user)
    mock_get_jwt_identity.start()
    mock_db_get_or_404.start()
    decorated_func = requires_role('admin')(lambda:"Sucess")      
    result = decorated_func()
    assert result == "Sucess"

    mock_get_jwt_identity.stop()
    mock_db_get_or_404.stop()

def test_requires_role_fail(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = "normal"

    mock_get_jwt_identity = mocker.patch(
        'src.controllers.decorator.get_jwt_identity',
        return_value=1
    )

    mock_db_get_or_404 = mocker.patch(
        'src.controllers.decorator.db.get_or_404',
        return_value=mock_user
    )

    mock_get_jwt_identity.start()
    mock_db_get_or_404.start()

    decorated_func = requires_role('admin')(lambda: "Sucess")

    result = decorated_func()

    assert result == (
        {"message": "User don't have access."},
        HTTPStatus.FORBIDDEN
    )

    mock_get_jwt_identity.stop()
    mock_db_get_or_404.stop()

    