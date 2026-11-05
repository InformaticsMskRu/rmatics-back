import pytest

from flask import Flask

from informatics_front.model import User, db
from informatics_front.utils.auth.make_jwt import generate_auth_token

VALID_TIME = 100500


@pytest.yield_fixture
def token(app: Flask, users: dict):
    user = db.session.query(User).get(users[0]['id'])

    previous_config_data = app.config.get('JWT_TOKEN_EXP')
    app.config['JWT_TOKEN_EXP'] = VALID_TIME

    token = generate_auth_token(user)
    yield token

    app.config['JWT_TOKEN_EXP'] = previous_config_data


@pytest.yield_fixture
def expired_token(app: Flask, users: dict):
    user = db.session.query(User).get(users[0]['id'])

    previous_config_data = app.config.get('JWT_TOKEN_EXP')
    app.config['JWT_TOKEN_EXP'] = -1

    token = generate_auth_token(user)
    yield token

    app.config['JWT_TOKEN_EXP'] = previous_config_data


@pytest.fixture(autouse=True)
def moodle_accepts_login(mocker):
    """The login view asks Moodle's token service; the tests must not need a live Moodle."""
    response = mocker.Mock()
    response.json.return_value = {'token': 'moodle-token'}
    return mocker.patch('informatics_front.view.auth.authorization.requests.post', return_value=response)
