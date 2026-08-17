import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from django.core.management.base import BaseCommand
from news.models import 뉴스
from news.ai import 판정한다

주소들 = {
    "경제": "https://www.hankyung.com/feed/economy",
    "금융": "https://www.hankyung.com/feed/finance",
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        새로 = 0
        for 출처, 주소 in 주소들.items():
            요청 = urllib.request.Request(주소, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(요청) as 응답:
                뿌리 = ET.fromstring(응답.read())
            for 항목 in 뿌리.findall(".//item"):
                제목 = 항목.findtext("title")
                감성, 신뢰도 = 판정한다(제목)
                건, 만들어짐 = 뉴스.objects.get_or_create(
                    링크=항목.findtext("link"),
                    defaults={
                        "제목": 제목,
                        "시각": parsedate_to_datetime(항목.findtext("pubDate")),
                        "출처": 출처,
                        "감성": 감성,
                        "신뢰도": 신뢰도,
                    },
                )
                if 만들어짐:
                    새로 += 1
        채움 = 0
        for 건 in 뉴스.objects.filter(감성=""):
            건.감성, 건.신뢰도 = 판정한다(건.제목)
            건.save()
            채움 += 1
        print("새로 넣은 것", 새로, "건 / 감성을 채운 것", 채움, "건")