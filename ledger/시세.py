import json
import urllib.request
import os 
from dotenv import load_dotenv

load_dotenv()

열쇠 = os.getenv("ECOS_KEY")
주소 = "https://ecos.bok.or.kr/api/StatisticSearch/"+ 열쇠 + "/json/kr/1/10/722Y001/D/20260101/20260110/0101000"

def 가져온다():
    답 = urllib.request.urlopen(주소)
    자료 = json.loads(답.read().decode("utf-8"))
    return 자료["StatisticSearch"]["row"]