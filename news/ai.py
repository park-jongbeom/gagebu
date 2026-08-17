import joblib
from pathlib import Path

뿌리 = Path(__file__).resolve().parent.parent
변환기, 모델 = joblib.load(뿌리 / "감성모델.pkl")
print("감성 모델을 읽었습니다")


def 판정한다(문장):
    X = 변환기.transform([문장])
    감성 = str(모델.predict(X)[0])
    신뢰도 = round(float(max(모델.predict_proba(X)[0])), 2)
    return 감성, 신뢰도