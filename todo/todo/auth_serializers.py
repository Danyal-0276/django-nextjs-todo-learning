from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    password_confirm = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "password_confirm",
        ]
        read_only_fields = ["id"]

    def validate_email(self, value):
        normalized_email = value.strip().lower()

        if User.objects.filter(email__iexact=normalized_email).exists():
            raise serializers.ValidationError("An account already uses this email.")

        return normalized_email

    def validate(self, attrs):
        password = attrs["password"]

        password_confirm = attrs["password_confirm"]

        if password != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": ["Password do not match"]}
            )

        candidate_user = User(
            username=attrs["username"],
            email=attrs["email"],
        )

        try:
            validate_password(
                password,
                user=candidate_user,
            )
        except DjangoValidationError as error:
            raise serializers.ValidationError(
                {"password": list(error.messages)}
            ) from error

        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        return User.objects.create_user(**validated_data)
