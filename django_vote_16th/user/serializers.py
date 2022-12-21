from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class JoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['user_id', 'name', 'email', 'password', 'part', 'team', 'is_candidate']

    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        name = validated_data.get('name')
        email = validated_data.get('email')
        part = validated_data.get('part')
        team = validated_data.get('team')
        password = validated_data.get('password')
        is_candidate = validated_data.get('is_candidate')
        user = User(
            user_id=user_id,
            name=name,
            email=email,
            part=part,
            team=team,
            is_candidate=is_candidate,
        )
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(
        required=True,
        write_only=True,
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['user_id', 'password']

    def validate(self, data):
        user_id = data.get('user_id', None)
        password = data.get('password', None)

        if User.objects.filter(user_id=user_id).exists():
            user = User.objects.get(user_id=user_id)

            if not user.check_password(password):
                raise serializers.ValidationError("패스워드가 잘못되었습니다.")


        else:
            raise serializers.ValidationError("해당 유저는 존재하지 않습니다.")

        return user

class LogoutSerializer(serializers.ModelSerializer):

    user_id = serializers.CharField(
        required=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ['user_id']

    def validate(self, data):
        user_id = data.get('user_id', None)

        if User.objects.filter(user_id=user_id).exists():
            user = User.objects.get(user_id=user_id)
            refresh_token = user.refresh_token

            # refresh token이 null값
            if not refresh_token:
                raise serializers.ValidationError("이미 로그아웃 되었거나 현재 로그인 되어 있지 않습니다.")

        else:
            raise serializers.ValidationError("해당 유저는 존재하지 않습니다.")

        return user
