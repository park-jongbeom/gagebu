from django.db import models

# Create your models here.
class 뉴스(models.Model):
    제목 = models.CharField(max_length=200)
    링크 = models.URLField(unique=True)
    시각 = models.DateTimeField()
    출처 = models.CharField(max_length=20)    
    감성 = models.CharField(max_length=10, blank=True)
    신뢰도 = models.FloatField(null=True, blank=True)