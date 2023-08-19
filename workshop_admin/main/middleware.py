import hashlib

from django.contrib.auth import get_user_model

User = get_user_model()

import requests
from django.conf import settings

class MoodleAccountAuthorization:
    def authenticate(self, _, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')

        if not all([username, password]):
            return None

        r = requests.get(settings.MOODLE_URL, params={
             'username': username,
             'password': password,
             'service': 'moodle_mobile_app',
        })

        print(r.text)

        if "token" not in r.json():
            return None

        print(r.json())

        try:
            user = User.objects \
                .prefetch_related('roles') \
                .filter(username=username).get()
        except User.DoesNotExist:
            print("Not found")
            return None

        print(user.id)
        if not user.is_staff:
            return None
        return user

    def get_user(self, user_id):
        try:
            print("get_user")
            return User.objects.prefetch_related('roles').get(pk=user_id)
        except User.DoesNotExist:
            print("Not found 1")
            return None
