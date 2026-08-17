import joblib
from pathlib import Path

뿌리 = Path(__file__).resolve().parent.parent
모델 = joblib.load(뿌리 / "모델.pkl")
print("모델을 읽었습니다")