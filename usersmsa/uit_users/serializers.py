from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import ValidationError

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'])

        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()

        return user


class UserLoginSerializer(serializers.ModelSerializer):

    password = serializers.CharField()
    username = serializers.CharField()

    class Meta:
        model = UserModel
        fields = ("id", "username", 'email', 'first_name', 'last_name', 'password')

    def check_user(self, validated_data):
        user = authenticate(username=validated_data['username'],
                            password=validated_data['password'])
        if not user:
            raise ValidationError({'detail': 'user not found'})

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id", "username", 'email', 'first_name', 'last_name')
