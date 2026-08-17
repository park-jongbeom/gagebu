import csv
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

한글 = {"POSITIVE": "긍정", "NEGATIVE": "부정", "NEUTRAL": "중립"}

제목들 = []
라벨들 = []
with open("korfin-asc_문장감성_정리본.csv", encoding="utf-8") as 파일:
    for 행 in csv.DictReader(파일):
        제목들.append(행["제목"])
        라벨들.append(한글[행["감성"]])
print("문장", len(제목들), "건")

훈련제목, 시험제목, 훈련라벨, 시험라벨 = train_test_split(
    제목들, 라벨들, test_size=0.2, random_state=0, stratify=라벨들)

변환기 = CountVectorizer()
훈련X = 변환기.fit_transform(훈련제목)
모델 = LogisticRegression(max_iter=2000).fit(훈련X, 훈련라벨)

정확도 = 모델.score(변환기.transform(시험제목), 시험라벨)
print("정확도", round(정확도 * 100, 1), "%")
joblib.dump((변환기, 모델), "감성모델.pkl")
print("저장 끝")