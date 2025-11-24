from src.services.auth import AuthService


def test_decode_and_decode_access_token():

    data = {"user_id":1}
    jwt_token = AuthService().create_access_token(data=data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    access_token = AuthService().decode_token(jwt_token)

    assert access_token
    assert isinstance(access_token, dict)
    assert list(access_token.keys()) == ['user_id','exp']