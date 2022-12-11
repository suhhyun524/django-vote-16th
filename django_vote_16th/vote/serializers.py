from rest_framework import serializers
from user.models import User
from .models import Demo_Vote, PartLeader_Vote


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['team']


class DemoVoteSerializer(serializers.ModelSerializer):
    total = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Demo_Vote
        fields = ['team', 'total']


class PartVoteSerializer(serializers.ModelSerializer):
    total = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = PartLeader_Vote
        fields = ['votee', 'total']

