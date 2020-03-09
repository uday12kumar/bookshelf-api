from django.urls import path

from bookshelf.users.api import Register, UserLogin, GetAuthors, CreateAuthor

app_name = "users"
urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("login/", UserLogin.as_view(), name="login"),
    path("authors/", GetAuthors.as_view(), name="list_authors"),
    path("author/create", CreateAuthor.as_view(), name="authors"),
]
