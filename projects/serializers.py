from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    # 모델 칸이 아니라 조회할 때 계산해서 붙이는 값이다.
    target_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'stack', 'target_count', 'created_at']
