from django.urls import path

from bookshelf.books.apis import CreateBook, GetUpdateBook, GetGenere, ListBooks, GetAuthorsBooks

app_name = "books"

urlpatterns = [
    path("", CreateBook.as_view(), name="create_book"),
    path("list/", ListBooks.as_view(), name="list_book"),
    path("<int:pk>/", GetUpdateBook.as_view(), name="update_book"),
    path("author/<int:has_books>/", GetAuthorsBooks.as_view(), name="author"),
    path("genres/", GetGenere.as_view(), name="genres"),
]
