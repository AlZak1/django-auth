from datetime import datetime, timedelta

import datetime as date

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

import jwt


class User(AbstractUser):

    name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    password = models.CharField(max_length=255)
    username = None

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    @property
    def refresh_token(self):
        return self._generate_refresh_jwt_token()

    def _generate_jwt_token(self):

        payload = {
            'id': self.id,
            'exp': date.datetime.utcnow() + date.timedelta(minutes=60),
            'iat': date.datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return token

    def _generate_refresh_jwt_token(self):

        payload = {
            'id': self.id,
            'exp': date.datetime.utcnow() + date.timedelta(hours=24),
            'iat': date.datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return token

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
