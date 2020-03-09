from rest_framework import serializers

from bookshelf.books.models import Book, Genre
from bookshelf.users.models import Author
from bookshelf.users.serializers import AuthorSerializer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CreateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookSerializer(CreateBookSerializer):
    author = AuthorSerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)


class AuthorBookSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)

    class Meta:
        model = Author
        fields = ('name', 'books')
