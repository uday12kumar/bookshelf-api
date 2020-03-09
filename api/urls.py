from django.urls import include, path
from django.contrib import admin

from bookshelf.users import urls as user_urls
from bookshelf.books import urls as book_urs
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Bookshelf API')

app_name = "bookshelf"

urlpatterns = [
    path('api/v1/', include([
        path('users/', include(user_urls)),
        path('books/', include(book_urs)),
    ])),
]

urlpatterns += [
    path('', schema_view),
    path('_admin/', admin.site.urls),
]

# try:
#     urlpatterns += [
#         path('silk/', include('silk.urls', namespace='silk')),
#     ]
# except Exception as error:
#     print(error)
#     pass
