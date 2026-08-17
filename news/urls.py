from django.urls import path
from . import views

urlpatterns = [
    path("api/감성통계/", views.감성통계),
    path("api/뉴스/", views.뉴스목록),
    path("news/", views.대시보드),
]