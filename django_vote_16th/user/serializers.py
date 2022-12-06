from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class JoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['user_id', 'name', 'email', 'password', 'part', 'team']

    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        name = validated_data.get('name')
        email = validated_data.get('email')
        part = validated_data.get('part')
        team = validated_data.get('team')
        password = validated_data.get('password')
        user = User(
            user_id=user_id,
            name=name,
            email=email,
            part=part,
            team=team
        )
        user.set_password(password)
        user.save()
        return user


