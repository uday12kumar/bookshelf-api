import factory

from factory.django import DjangoModelFactory
from faker import Faker

from bookshelf.books.models import Genre, Book
from bookshelf.users.tests.factories import AuthorFactory

fake = Faker()


class BookFactory(DjangoModelFactory):
    name = fake.name()

    @factory.post_generation
    def author(self, create, extracted, **kwargs):
        if extracted:
            self.admin.add(extracted)
        else:
            user = AuthorFactory()
            self.author.add(user)

    @factory.post_generation
    def genre(self, create, extracted, **kwargs):
        if extracted:
            self.members.add(extracted)
        else:
            genre_ = GenreFactory()
            self.genre.add(genre_)

    class Meta:
        model = Book


class GenreFactory(DjangoModelFactory):
    name = fake.first_name()
    is_active = True

    class Meta:
        model = Genre
