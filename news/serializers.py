from rest_framework import serializers
from .models import 뉴스


class 뉴스Serializer(serializers.ModelSerializer):
    class Meta:
        model = 뉴스
        fields = ["제목", "링크", "시각", "출처", "감성", "신뢰도"]