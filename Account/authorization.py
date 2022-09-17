from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from jose import jwt, JWTError
from ninja.security import HttpBearer

TIME_DELTA = timedelta(days=120)

User = get_user_model()

class GlobalAuth(HttpBearer):
     def authenticate(self, request, token):
        try:
            user_email = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms='HS256')
        except JWTError:
            return {'token': 'unauthorized'}

        if user_email:
            return {'email': str(user_email['email'])}


def get_tokens_for_user(user):
    token = jwt.encode({'email': str(user.email)}, key=settings.SECRET_KEY, algorithm='HS256')
    return {
        'access': str(token)
    }