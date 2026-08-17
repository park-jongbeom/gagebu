from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
import joblib

숫자 = load_digits()
모델 = LogisticRegression(max_iter=2000).fit(숫자.data, 숫자.target)
joblib.dump(모델, "숫자모델.pkl")
print("학습 끝", 숫자.images.shape)