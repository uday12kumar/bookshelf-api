from rest_framework import serializers

from bookshelf.users.models import User, Author


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class UserRegisterSerializer(UserSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'password2')

    def save(self):
        user = User(first_name=self.validated_data['first_name'],
                    last_name=self.validated_data['last_name'],
                    email=self.validated_data['email'],
                    )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': "password didn't match."})
        user.set_password(password)
        user.save()
        return user


class UserLoginRequestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')


class UserLoginSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=130)
    user = UserSerializer()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
