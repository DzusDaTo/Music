from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from . import models
from .models import AuthUser


from rest_framework import serializers
from .models import AuthUser
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.AuthUser
        fields = ('email', 'display_name', 'password', 'avatar', 'country', 'city', 'bio')

    def validate_password(self, value):
        """
        Дополнительная валидация пароля, например, можно добавить проверку сложности пароля
        """
        validate_password(value)
        return value

    def create(self, validated_data):
        # Создание нового пользователя
        user = models.AuthUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            display_name=validated_data.get('display_name', ''),
            country=validated_data.get('country', ''),
            city=validated_data.get('city', ''),
            bio=validated_data.get('bio', '')
        )

        # Сохраняем аватар, если он был передан
        avatar = validated_data.get('avatar')
        if avatar:
            user.avatar = avatar
            user.save()

        return user


class SocialLinkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.SocialLink
        fields = ('id', 'link')


class AuthorSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = models.AuthUser
        fields = ('id', 'avatar', 'country', 'city', 'bio', 'display_name', 'social_links')