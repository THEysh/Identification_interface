import requests
import json

class PredictionClient:
    def __init__(self, server_url):
        self.server_url = server_url

    def predict(self, input_path):
        data = {"input_image": input_path}
        response = requests.post(self.server_url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"请求失败，状态码: {response.status_code}, 响应体: {response.text}")

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
