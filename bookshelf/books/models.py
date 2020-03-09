from django.db import models
from bookshelf.models import TimestampedModel
from bookshelf.users.models import User, Author


class GenreManager(models.Manager):
    def list_active(self):
        return self.filter(is_active=True)


class Genre(TimestampedModel):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    objects = GenreManager()


class Book(TimestampedModel):
    name = models.CharField(max_length=100)
    author = models.ManyToManyField(Author, related_name='books')
    genre = models.ManyToManyField(Genre)
