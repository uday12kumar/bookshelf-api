import os
from unittest import mock

import boto3
from django.test import TestCase
from moto import mock_sns
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from bookshelf.users.models import User, UserToken, Author
from bookshelf.users.tests.factories import UserFactory, TokenFactory, AuthorFactory


class UserTestCase(TestCase):
    """ Test module for User model """

    def setUp(self):
        self.user = UserFactory()

    def test_user_object(self):
        users = User.objects.all()
        self.assertEqual(users.count(), 1)


class TokenTestCase(TestCase):
    """ Test module for UserToken model """

    def setUp(self):
        self.user = UserFactory()
        self.user_token = TokenFactory(user=self.user)

    def test_user_object(self):
        tokens = UserToken.objects.all()
        self.assertEqual(tokens.count(), 1)


class AuthorTestCase(TestCase):
    """ Test module for Author model """

    def setUp(self):
        self.author = AuthorFactory()

    def test_user_object(self):
        author = Author.objects.all()
        self.assertEqual(author.count(), 1)
        self.assertEqual(author.first().name, self.author.name)


class UserLogin(APITestCase):
    """ Test module for login api """

    def setUp(self):
        self.email = "uday12kumar@gmail.com"
        self.password = "testpassword"
        self.client = APIClient()
        self.request_login = "users:login"
        self.user = UserFactory(email=self.email)
        self.user.set_password(self.password)
        self.user.save()
        self.request_payload = {'email': self.email, 'password': self.password}

    def test_user_login(self):
        response = self.client.post(reverse(self.request_login), data=self.request_payload, format='json')
        self.assertEqual(response.status_code, 200)


class UserRegister(APITestCase):
    """ Test module for register api """

    def setUp(self):
        self.email = "uday12kumar@gmail.com"
        self.password = "testpassword"
        self.first_name = "uday"
        self.last_name = "guntu"
        self.client = APIClient()
        self.request_register = "users:register"
        self.request_payload = {'email': self.email, 'password': self.password, 'password2': self.password,
                                'first_name': self.first_name, 'last_name': self.last_name}

    def test_user_register(self):
        response = self.client.post(reverse(self.request_register), data=self.request_payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['first_name'], self.first_name)
        self.assertEqual(response.data['last_name'], self.last_name)