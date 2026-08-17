import time
import os
import joblib
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

숫자 = load_digits()
훈련X, 시험X, 훈련y, 시험y = train_test_split(
    숫자.data, 숫자.target, test_size=0.2, random_state=0)

for 이름, 모델 in [("로지스틱", LogisticRegression(max_iter=2000)),
                  ("랜덤포레스트", RandomForestClassifier(n_estimators=100, random_state=0))]:
    모델.fit(훈련X, 훈련y)
    joblib.dump(모델, "선수.pkl")
    크기 = os.path.getsize("선수.pkl")
    정확도 = round(모델.score(시험X, 시험y) * 100, 1)
    t = time.perf_counter()
    for _ in range(1000):
        모델.predict(시험X[:1])
    속도 = round((time.perf_counter() - t) * 1000)
    print(이름, "크기", 크기, "B / 정확도", 정확도, "% / 1000회", 속도, "ms")
os.remove("선수.pkl")