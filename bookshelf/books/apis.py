from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from bookshelf.books.models import Book, Genre
from bookshelf.books.serializers import BookSerializer, GenreSerializer, CreateBookSerializer, AuthorBookSerializer
from bookshelf.users.models import Author


class GetUpdateBook(RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CreateBookSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


class CreateBook(CreateAPIView):
    serializer_class = CreateBookSerializer


class ListBooks(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filterset_fields = ('genre__id', 'author__id')


class GetGenere(ListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.list_active()


class GetAuthorsBooks(ListAPIView):
    serializer_class = AuthorBookSerializer

    def get_queryset(self):
        if self.kwargs['has_books'] == 1:
            return Author.objects.with_books()
        else:
            return Author.objects.with_out_books()
