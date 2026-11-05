import datetime
from typing import Optional

import jwt
from flask import current_app

from informatics_front.utils.functions import utcnow
from informatics_front.view.auth.serializers.auth import RoleAuthSerializer


def generate_auth_token(user: 'User') -> str:
    roles_serializer = RoleAuthSerializer(many=True)
    roles = roles_serializer.dumps(user.roles)

    expiration = utcnow() + datetime.timedelta(
        seconds=current_app.config.get('JWT_TOKEN_EXP'))

    d = {
        'id': user.id,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'roles': roles,
        'exp': expiration,
    }
    return jwt.encode(d, current_app.config['SECRET_KEY'], algorithm='HS256')


def generate_refresh_token(user: 'User') -> str:
    expiration = utcnow() + datetime.timedelta(
        seconds=current_app.config.get('JWT_REFRESH_TOKEN_EXP', ))
    d = {
        'user_id': user.id,
        'exp': expiration,
    }
    return jwt.encode(d, current_app.config['SECRET_KEY'], algorithm='HS256')


def decode_jwt_token(token: str) -> Optional[dict]:
    token_options = {'require': ['exp']}
    try:
        return jwt.decode(token, current_app.config['SECRET_KEY'],
                          options=token_options, algorithms=['HS256'])
    except jwt.PyJWTError:
        return None
