from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from ledger.views import 인사, 소개, 상세, 올해, 검색, 목록, 추가, 수정, 삭제, 통계, 가입, 로그인, 로그아웃
from ledger import views
from django.urls import include
from rest_framework.routers import DefaultRouter

라우터 = DefaultRouter()
라우터.register("내역", views.내역ViewSet)

urlpatterns = [
    path("hello/", 인사),
    path("about/", 소개),
    path("detail/2026/", 올해),
    path("detail/<int:번호>/", 상세),
    path("search/", 검색),
    path("list/", 목록),
    path("add/", 추가),
    path("edit/<int:번호>", 수정),
    path("delete/<int:번호>", 삭제),
    path("stats/", 통계),
    path("signup/", 가입),
    path("login/", 로그인),
    path("logout/", 로그아웃),
    path("api/내역/", views.내역목록api),
    path("api/v3/", include(라우터.urls)),
    path("api/token", TokenObtainPairView.as_view()),
    path("api/token/refresh", TokenRefreshView.as_view()),
    path("api/예측/", views.예측),
    path("api/그림/", views.그림예측),
    path("predict/", views.예측화면),
    path("api/시세/", views.시세),
    path("api/수집/", views.수집목록),
    path("chart/", views.시세화면),
]