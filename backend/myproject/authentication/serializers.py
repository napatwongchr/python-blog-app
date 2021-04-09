from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class UserLoginSerializer(serializers.Serializer):
  email = serializers.CharField(max_length=255)
  password = serializers.CharField(max_length=128, write_only=True)
  token = serializers.CharField(max_length=128, read_only=True)
  refresh_token = serializers.CharField(max_length=128, read_only=True)

  def validate(self, data):
    email = data.get("email", None)
    password = data.get("password", None)

    try:
      user = User.objects.get(email=email)
      is_password_valid = user.check_password(password)

      if user is None or not is_password_valid:
        raise serializers.ValidationError(
          'A user with this email and password is not matched.'
        )

      refresh = RefreshToken.for_user(user)
      update_last_login(None, user=user)
      
    except User.DoesNotExist:
      raise serializers.ValidationError(
          'User with given email and password does not exists'
      )

    return {
      "email": user.email,
      "token": str(refresh.access_token),
      "refresh_token": str(refresh)
    }
