import requests
import json

from PyQt5.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition


class PredictionClient:
    def __init__(self, server_url):
        self.server_url = server_url

    def predict(self, input_path, iou=0.6, conf=0.6):
        data = {"input_image": input_path,
                "iou": iou,
                "conf": conf}
        try:
            response = requests.post(self.server_url, json=data)
        except Exception as e:
            print(f"\033[93m警告: 服务器未响应\033[0m")
        if response.status_code == 200:
            return response.json()


if __name__ == '__main__':
    # 实例化并使用该类
    url = 'http://127.0.0.1:8000/predict'
    input_path = r"F:\ysh_loc\projects\github_identification_interface\resource\some_img\1.jpg"
    client = PredictionClient(url)

    try:
        prediction_result = client.predict(input_path)
        print(json.dumps(prediction_result, indent=4))
    except Exception as e:
        print(e)
