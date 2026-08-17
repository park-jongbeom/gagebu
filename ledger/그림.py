
import numpy as np
import onnxruntime
from pathlib import Path
from PIL import Image

뿌리 = Path(__file__).resolve().parent.parent
세션 = onnxruntime.InferenceSession(뿌리 / "숫자모델.onnx",
                                  providers=["CPUExecutionProvider"])
입력이름 = 세션.get_inputs()[0].name

def 알아본다(올린파일):
    그림 = Image.open(올린파일).convert("L").resize((8,8))
    칸 = (255 - np.asarray(그림, dtype=np.float32)) / 255 * 16
    return int(세션.run(None, {입력이름: 칸.reshape(1, -1)})[0][0])