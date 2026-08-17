from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class 내역(models.Model):
    날짜 = models.DateField()
    분류 = models.CharField(max_length=10)
    항목 = models.CharField(max_length=50)
    금액 = models.IntegerField()
    이름 = models.CharField(max_length=20)
    계좌 = models.CharField(max_length=30)
    주인 = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.항목
    
class 예측기록(models.Model):
    항목 = models.CharField(max_length=50)
    분류 = models.CharField(max_length=10)
    확신 = models.FloatField()
    시각 = models.DateTimeField(auto_now_add=True)
    
class 수집(models.Model):
    날짜 = models.CharField(max_length=8)
    이름 = models.CharField(max_length=50)
    값 = models.FloatField()