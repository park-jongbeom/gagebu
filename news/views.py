from django.shortcuts import render
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import 뉴스
from .serializers import 뉴스Serializer


@api_view(["GET"])
def 감성통계(request):
    통계 = 뉴스.objects.exclude(감성="").values("감성").annotate(건수=Count("id"))
    return Response(통계)

@api_view(["GET"])
def 뉴스목록(request):
    최근 = 뉴스.objects.order_by("-시각")[:20]
    return Response(뉴스Serializer(최근, many=True).data)


def 대시보드(request):
    return render(request, "news/대시보드.html")
