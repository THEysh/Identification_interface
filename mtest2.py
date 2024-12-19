import sys
import time
import asyncio
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from fastapi import FastAPI
from pydantic import BaseModel
import time
from ultralytics_main.predict import run_inference  # 导入 predict.py 中的 run_inference 函数
import asyncio
from concurrent.futures import ThreadPoolExecutor
import uvicorn

app = FastAPI()


class ImageRequest(BaseModel):
    input_images: list  # 修改为接收多个图像路径
    iou: float = 0.7  # 添加 iou 参数，默认值为 0.7
    conf: float = 0.25  # 添加 conf 参数，默认值为 0.25


class ImageResponse(BaseModel):
    save_dir: str  # 添加保存路径
    rectangle_pos: list  # 修改为接收多个矩形位置
    scores: float  # 置信度分数
    classes: int  # 类别索引
    inference_time: float


async def run_inference_async(image_paths, iou, conf):  # 修改为接收 iou 和 conf
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, run_inference, image_paths, iou, conf)  # 传入 iou 和 conf


@app.post("/predict", response_model=list[ImageResponse])  # 修改为返回多个响应
async def predict(request: ImageRequest):
    start_time = time.time()
    responses = []
    # 将输入图像分成每批最多 50 张
    batch_size = 1
    input_batches = [request.input_images[i:i + batch_size] for i in range(0, len(request.input_images), batch_size)]

    for batch in input_batches:
        # 对每个批次创建任务列表
        result = await run_inference_async(batch, request.iou, request.conf)  # 传入 iou 和 conf
        if result is not None and all(result):  # 检查结果是否为 None 且所有值都有效
            save_dir, rectangle_pos, scores, classes = result

            for i in range(len(scores)):
                responses.append(ImageResponse(
                    save_dir=save_dir,
                    rectangle_pos=rectangle_pos[i:i + 1],  # 每个矩形位置
                    scores=scores[i],  # 每个分数
                    classes=classes[i],  # 每个类别索引
                    inference_time=time.time() - start_time
                ))
        else:
            print("One of the images failed to process.")

    return responses  # 返回所有响应


# 异步耗时函数
async def long_running_task():
    uvicorn.run(app, host="0.0.0.0", port=8000)


# 将异步函数封装到 QThread 中
class AsyncThread(QThread):
    result_signal = pyqtSignal(str)  # 用于传递结果信号

    def __init__(self, loop, parent=None):
        super().__init__(parent)
        self.loop = loop

    def run(self):
        # 运行异步任务
        result = asyncio.run(long_running_task())  # 使用 asyncio 运行异步任务
        self.result_signal.emit(result)  # 发射信号将结果传递回主线程


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 异步操作示例")
        self.setGeometry(100, 100, 400, 200)

        # 标签和按钮
        self.label = QLabel(self)
        self.label.setGeometry(100, 50, 200, 50)
        self.label.setText("点击按钮开始任务")

        self.button = QPushButton('开始任务', self)
        self.button.setGeometry(100, 120, 200, 50)
        self.button.clicked.connect(self.start_task)

    def start_task(self):
        self.label.setText("任务进行中...")
        self.button.setEnabled(False)  # 禁用按钮，防止重复点击

        # 创建一个事件循环并启动线程
        loop = asyncio.get_event_loop()
        self.thread = AsyncThread(loop)
        self.thread.result_signal.connect(self.on_task_done)  # 连接信号
        self.thread.start()

    def on_task_done(self, result):
        self.label.setText(result)  # 更新标签显示结果
        self.button.setEnabled(True)  # 重新启用按钮


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
