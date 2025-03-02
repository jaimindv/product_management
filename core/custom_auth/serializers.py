from rest_framework import serializers

from core.custom_auth.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {"password": {"required": True, "write_only": True}}

    def create(self, validated_data):
        password = validated_data.get("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.get("password")
        user_instance = super().update(instance, validated_data)
        if password:
            user_instance.set_password(password)
            user_instance.save()
        return user_instance


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        if old_password == new_password:
            raise serializers.ValidationError(
                {"message": "New password cannot be same as old password."}
            )

        request = self.context.get("request")
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError({"message": "Incorrect old password."})
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
