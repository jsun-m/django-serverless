from rest_framework import serializers

from django.utils import timezone

from database.identity.models import create_authtoken, expire_authtokens
from database.identity.models import Identity


class AuthTokenSerializer(serializers.Serializer):
    id = serializers.CharField(source="external_id")
    expires = serializers.DateTimeField()
    created = serializers.DateTimeField()


class OneTimeAuthTokenSerializer(serializers.Serializer):
    key = serializers.CharField()
    id = serializers.CharField(source="external_id", read_only=True)
    expires = serializers.DateTimeField()
    created = serializers.DateTimeField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    token = OneTimeAuthTokenSerializer(read_only=True)

    def validate(self, data):
        try:
            identity = Identity.objects.get(email=data.get("email", "").lower())
            self.context["identity"] = identity
        except Identity.DoesNotExist:
            raise serializers.ValidationError("invalid_login")

        if identity.check_password(data["password"]):
            return data

        raise serializers.ValidationError("invalid_login")

    def create(self, validated_data):
        identity = self.context["identity"]

        expire_authtokens(identity=identity)  # expire any existing authtokens
        authtoken = create_authtoken(identity)

        identity.last_login = timezone.now()
        identity.save()

        return {"token": authtoken}


class CreateIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Identity
        fields = ("email", "password")

    def create(self, validated_data):
        identity = Identity(**validated_data)
        identity.set_password(validated_data["password"])
        identity.save()

        return identity

    def to_representation(self, value):
        return {"identity": value}

