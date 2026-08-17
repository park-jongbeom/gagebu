import joblib
import numpy as np
from skl2onnx import to_onnx

모델 = joblib.load("숫자모델.pkl")
견본 = np.zeros((1, 64), dtype=np.float32)

그릇 = to_onnx(모델, 견본)
open("숫자모델.onnx", "wb").write(그릇.SerializeToString())
print("담았습니다", len(그릇.SerializeToString()), "바이트")