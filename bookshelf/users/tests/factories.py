import uuid

from factory.django import DjangoModelFactory
from faker import Faker

from bookshelf.users.models import User, UserToken, Author

fake = Faker()


class UserFactory(DjangoModelFactory):
    first_name = fake.first_name()
    last_name = fake.last_name()

    class Meta:
        model = User


class TokenFactory(DjangoModelFactory):
    key = str(uuid.uuid4())

    class Meta:
        model = UserToken


class AuthorFactory(DjangoModelFactory):
    name = fake.first_name()

    class Meta:
        model = Author
