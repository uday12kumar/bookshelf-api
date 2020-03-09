import logging

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, ListAPIView

from bookshelf.users.models import User, Author, UserToken
from bookshelf.users.serializers import UserRegisterSerializer, UserSerializer, UserLoginSerializer, \
    UserLoginRequestSerializer, AuthorSerializer

logger = logging.getLogger(__name__)


class Register(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer


class UserLogin(CreateAPIView):
    serializer_class = UserLoginRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        user = authenticate(email=request.data['email'].lower(), password=request.data['password'])
        if user:
            if user.is_active:
                return self.getAuthenticationResponseForUser(user)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def getAuthenticationResponseForUser(self, user):
        if user:
            token = UserToken.objects.create_token(user)
            serializer = UserLoginSerializer({"token": token, "user": user}, read_only=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class GetAuthors(ListAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class CreateAuthor(CreateAPIView):
    serializer_class = AuthorSerializer


class CreateAuthor(CreateAPIView):
    serializer_class = AuthorSerializer
