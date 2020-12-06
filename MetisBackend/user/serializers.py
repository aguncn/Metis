from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # 要序列的model
        fields = ('url', 'username', 'email', 'groups')  # 数据字段


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group  # 要序列的model
        fields = ('url', 'name')  # 数据字段
