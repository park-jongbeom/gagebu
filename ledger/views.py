from django.views.decorators.cache import cache_page
from django.shortcuts import render, get_object_or_404, redirect
from ledger.models import 내역, 예측기록, 수집
from ledger.forms import 내역폼
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncMonth
from django.contrib.auth import login as 로그인시킨다, logout as 로그아웃시킨다
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, authentication_classes, throttle_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from .serializers import 내역Serializer, 예측요청Serializer, 예측기록Serializer, 수집Serializer
from rest_framework import viewsets
from .ai import 모델
from .그림 import 알아본다
from .시세 import 가져온다

# Create your views here.
from django.http import HttpResponse


def 인사(request):
    return HttpResponse("안녕하세요, 첫 화면입니다")


def 소개(request):
    return HttpResponse("가계부를 만들 예정입니다")


@login_required
def 상세(request, 번호):
    건 = get_object_or_404(내역, id=번호, 주인=request.user)
    return render(
        request,
        "ledger/상세.html",
        {"건": 건, "이름": 이름가리기(건.이름), "계좌": 계좌가리기(건.계좌)},
    )


def 올해(request):
    return HttpResponse("2026년 내역입니다")


def 검색(request):
    if request.method == "POST":
        return HttpResponse("POST 로 왔습니다")
    return render(request, "ledger/검색.html")


def 이름가리기(이름):
    return 이름[0] + "**"


def 계좌가리기(계좌):
    return "****-" + 계좌[-4:]


@login_required
def 목록(request):
    검색어 = request.GET.get("검색어", "")
    내역들 = 내역.objects.select_related("주인").filter(주인=request.user).order_by("-날짜")
    if 검색어:
        내역들 = 내역들.filter(Q(항목__icontains=검색어) | Q(이름__icontains=검색어))
    분류 = request.GET.get("분류", "")
    if 분류:
        내역들 = 내역들.filter(분류=분류)
    쪽나눔 = Paginator(내역들, 5)
    쪽 = 쪽나눔.get_page(request.GET.get("page"))
    합계 = 내역들.aggregate(합계=Sum("금액"))["합계"]
    return render(
        request, "ledger/목록.html", {"쪽": 쪽, "검색어": 검색어, "합계": 합계}
    )


@login_required
def 추가(request):
    if request.method == "POST":
        폼 = 내역폼(request.POST)
        if 폼.is_valid():
            건 = 폼.save(commit=False)
            건.주인 = request.user
            폼.save()
            return redirect("/list/")
    else:
        폼 = 내역폼()
    return render(request, "ledger/추가.html", {"폼": 폼})


@login_required
def 수정(request, 번호):
    건 = get_object_or_404(내역, id=번호, 주인=request.user)
    if request.method == "POST":
        폼 = 내역폼(request.POST, instance=건)
        if 폼.is_valid():
            폼.save()
            return redirect("/list/")
    else:
        폼 = 내역폼(instance=건)
    return render(request, "ledger/추가.html", {"폼": 폼})


@login_required
def 삭제(request, 번호):
    건 = get_object_or_404(내역, id=번호, 주인=request.user)
    if request.method == "POST":
        건.delete()
        return redirect("/list/")
    return render(request, "ledger/삭제.html", {"건": 건})


@login_required
def 통계(request):
    내것 = 내역.objects.filter(주인=request.user)
    분류별 = 내것.values("분류").annotate(합계=Sum("금액"), 건수=Count("id"))
    월별 = (
        내것.annotate(달=TruncMonth("날짜"))
        .values("달")
        .annotate(합계=Sum("금액"))
        .order_by("달")
    )
    전체 = 내것.aggregate(합계=Sum("금액"))["합계"]
    return render(
        request, "ledger/통계.html", {"분류별": 분류별, "월별": 월별, "전체": 전체}
    )


def 가입(request):
    if request.method == "POST":
        폼 = UserCreationForm(request.POST)
        if 폼.is_valid():
            사용자 = 폼.save()
            로그인시킨다(request, 사용자)
            return redirect("/list/")
    else:
        폼 = UserCreationForm()
    return render(request, "ledger/가입.html", {"폼": 폼})


def 로그인(request):
    if request.method == "POST":
        폼 = AuthenticationForm(request, request.POST)
        if 폼.is_valid():
            로그인시킨다(request, 폼.get_user())
            return redirect("/list/")
    else:
        폼 = AuthenticationForm()
    return render(request, "ledger/로그인.html", {"폼": 폼})


def 로그아웃(request):
    로그아웃시킨다(request)
    return redirect("/list/")


@api_view(["GET", "POST"])
def 내역목록api(request):
    if request.method == "GET":
        자료 = 내역.objects.all()
        직렬 = 내역Serializer(자료, many=True)
        return Response(직렬.data)
    직렬 = 내역Serializer(data=request.data)
    직렬.is_valid(raise_exception=True)
    직렬.save()
    return Response(직렬.data, status=201)


class 내역ViewSet(viewsets.ModelViewSet):
    queryset = 내역.objects.all()
    serializer_class = 내역Serializer

class 예측제한(UserRateThrottle):
    rate = "5/min"

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([예측제한])
def 예측(request):
    print("토큰:", request.headers.get("X-Token"))
    요청 = 예측요청Serializer(data=request.data)
    요청.is_valid(raise_exception=True)
    항목 = 요청.validated_data["항목"]
    분류 = 모델.predict([항목])[0]
    확신 = round(float(max(모델.predict_proba([항목])[0])), 3)
    if 확신 < 0.8:
        분류 = "모르겠음"
    기록 = 예측기록.objects.create(항목=항목, 분류=분류, 확신=확신)
    return Response(예측기록Serializer(기록).data, status=201)

def 예측화면(request):
    return render(request, "ledger/예측.html")

@api_view(["POST"])
@authentication_classes([])
def 그림예측(request):
    올린 = request.FILES.get("그림")
    if 올린 is None:
        return Response({"오류": "그림 칸이 비어 있습니다"}, status=400)
    try:
        숫자 = 알아본다(올린)
    except Exception:
        return Response({"오류": "그림 파일이 아닙니다"}, status=400)
    return Response({"파일": 올린.name, "숫자": 알아본다(올린)}, status=200)



@api_view(["GET"])
def 시세(request):
    return Response(가져온다())

@cache_page(60)
@api_view(["GET"])
def 수집목록(request):
    자료 = 수집.objects.all().order_by("날짜")
    return Response(수집Serializer(자료, many=True).data)

def 시세화면(request):
    return render(request, "ledger/시세.html")

# 상자 시험