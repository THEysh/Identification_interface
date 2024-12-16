import time
import requests
import concurrent.futures
import json


def predictExpFun(serverUrl, predictData: list):
    """
    发送 POST 请求到服务器并处理响应
    input_path, iou, conf
    """
    # 请求体数据
    print("PredictionClient:里", predictData)
    data = {
        "input_image": predictData[0],
        "iou": predictData[1],
        "conf": predictData[2]
    }
    # 发送 POST 请求
    t = time.time()
    print(t)
    try:
        response = requests.post(serverUrl, json=data)
        # 检查请求是否成功
        if response.status_code == 200:
            prediction_result = response.json()
            print(f"Request time: {time.time() - t} seconds")
            return prediction_result
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"\033[93m警告: 服务器未响应 - {e}\033[0m")
        print(f"Request time: {time.time() - t} seconds")
        return None


class PredictionClient:
    def __init__(self, serverUrl):
        """
        初始化 PredictionClient 类
        :param serverUrl: 服务器的 URL
        """
        self.serverUrl = serverUrl

    def predict(self, predictData:list):
        """
        发送 POST 请求到服务器并处理响应
        input_path, iou, conf
        """
        # 请求体数据
        print("PredictionClient:里", predictData)
        data = {
            "input_image": predictData[0],
            "iou": predictData[1],
            "conf": predictData[2]
        }
        # 发送 POST 请求
        t = time.time()
        print(t)
        try:
            response = requests.post(self.serverUrl, json=data)
            # 检查请求是否成功
            if response.status_code == 200:
                prediction_result = response.json()
                print(f"Request time: {time.time() - t} seconds")
                return prediction_result
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"\033[93m警告: 服务器未响应 - {e}\033[0m")
            print(f"Request time: {time.time() - t} seconds")
            return None


# 使用类
if __name__ == '__main__':
    # 服务器的 URL
    server_url = 'http://localhost:8000/predict'
    # 图像文件路径
    input_image_path = 'F:\\ysh_loc\\projects\\github_identification_interface\\resource\\Snipaste_2024-12-15_15-12-05.png'
    # 创建 PredictionClient 实例
    client = PredictionClient(server_url)

    # 定义并发请求数量
    num_requests = 10

    # 使用线程池并发发送请求
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        # 创建一个列表来存储所有的请求任务
        futures = [executor.submit(client.predict, input_image_path, 0.3, 0.2) for _ in range(num_requests)]

        # 收集所有请求的结果
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)

    # 打印所有结果
    for result in results:
        print(result)
