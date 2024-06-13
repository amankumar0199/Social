from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from rest_framework import serializers
from .models import FriendRequest, Friendship
from rest_framework.exceptions import ParseError
from users.utils import hash_password, verify_password
from users.utils import hash_password
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'password', 'email', 'name']
        extra_kwargs = {'password': {'write_only': True}}

    def create_user(self, validated_data):

        try:
            user = User()
            user.username = validated_data['name']
            user.email = validated_data['email']
            user.password = hash_password(validated_data['password'])
            user.save()
            return user
        except Exception as err:
            raise ParseError(err)

    def get_user_by_email(self, email):
        try:
            user = User.objects.get(email__exact=email)
            return user
        except Exception as err:
            raise serializers.ValidationError(err)

    def get_user_by_name(self, username):
        try:
            users = User.objects.filter(username__icontains=username)
            data = []
            for user in users:
                user_data = {}
                user_data["name"] = user.username
                user_data["email"] = user.email
                data.append(user_data)
            return data

        except Exception as err:
            raise serializers.ValidationError(err)

    def get_all_users(self, email):
        try:
            user = User.objects.all()
        except Exception as err:
            raise serializers.ValidationError(err)
        return user

    def check_user_login(self, email, password):
        if email and password:
            try:
                user = User.objects.get(email__exact=email)
                if user!=None:
                    saved_password = user.password
                    if verify_password(saved_password, password):
                        return True
                    else:
                        return False
                else:
                    return False
            except Exception as err:
                raise err
        else:
            return False

class FriendSerializer(serializers.ModelSerializer):
    class Meta:

        model = User
        fields = ['username', 'email']

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'timestamp']
        read_only_fields = ['id','sender', 'status', 'timestamp']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ['id', 'user1', 'user2', 'timestamp']

