import time
import joblib
import numpy as np
import onnxruntime
from sklearn.datasets import load_digits

원본 = joblib.load("숫자모델.pkl")
세션 = onnxruntime.InferenceSession("숫자모델.onnx")
입력이름 = 세션.get_inputs()[0].name
한장 = load_digits().data[7:8].astype(np.float32)

print("원본 답:", int(원본.predict(한장)[0]))
print("그릇 답:", int(세션.run(None, {입력이름: 한장})[0][0]))

t = time.perf_counter()
for _ in range(1000):
    원본.predict(한장)
print("원본 1000회:", round((time.perf_counter() - t) * 1000), "ms")

t = time.perf_counter()
for _ in range(1000):
    세션.run(None, {입력이름: 한장})
print("그릇 1000회:", round((time.perf_counter() - t) * 1000), "ms")
