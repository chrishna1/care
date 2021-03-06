from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from care.users.models import GENDER_CHOICES, State
from config.serializers import ChoiceField

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    user_type = ChoiceField(choices=User.TYPE_CHOICES)
    gender = ChoiceField(choices=GENDER_CHOICES)
    password = serializers.CharField(write_only=True)
    # until we start supporting other states
    state = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "user_type",
            "local_body",
            "district",
            "state",
            "phone_number",
            "gender",
            "age",
        )

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        # until we start supporting other states
        validated_data["state"] = State.objects.get(name="Kerala")
        return super().create(validated_data)


class UserSerializer(SignUpSerializer):
    user_type = ChoiceField(choices=User.TYPE_CHOICES, read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "user_type",
            "local_body",
            "district",
            "state",
            "phone_number",
            "gender",
            "age",
            "is_superuser",
        )

    extra_kwargs = {"url": {"lookup_field": "username"}}


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")
