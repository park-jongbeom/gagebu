from django.core.management.base import BaseCommand
from ledger.models import 수집
from ledger.시세 import 가져온다


class Command(BaseCommand):
    def handle(self, *args, **options):
        새로 = 0
        for 행 in 가져온다():
            기록, 만들었나 = 수집.objects.get_or_create(
                날짜 = 행["TIME"], 이름 = 행["ITEM_NAME1"],
                defaults={"값": float(행["DATA_VALUE"])})
            if 만들었나:
                새로 += 1
        print("새로 넣은 것", 새로, "건")