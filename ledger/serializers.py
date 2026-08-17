from rest_framework import serializers
from .models import 내역, 예측기록, 수집


class 내역Serializer(serializers.ModelSerializer):
    class Meta:
        model = 내역
        fields = ["id", "날짜", "분류", "항목", "금액"]

class 예측요청Serializer(serializers.Serializer):
    항목 = serializers.CharField(max_length=50)
    
class 예측기록Serializer(serializers.ModelSerializer):
    class Meta:
        model = 예측기록
        fields = ["id", "항목", "분류", "확신", "시각"]
        
class 수집Serializer(serializers.ModelSerializer):
    class Meta:
        model = 수집
        fields = ["id", "날짜", "이름", "값"]