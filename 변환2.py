import joblib
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import StringTensorType

모델 = joblib.load("모델.pkl")
그릇 = convert_sklearn(모델, initial_types=[("입력", StringTensorType([None, 1]))])