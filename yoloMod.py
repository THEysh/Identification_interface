import copy
import os
import time
import sys
import os
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt
from ultralytics import YOLO


def modifySuffix(orgPath: str, r=".jpg"):
    # 获取文件名和扩展名
    file_name, file_extension = os.path.splitext(os.path.basename(orgPath))
    # 修改扩展名为 .jpg
    new_file_name = f"{file_name}{r}"
    return new_file_name


import os
from ultralytics import YOLO


class YoloModel:
    def __init__(self):
        self.yolo = YOLO("./best.pt", task="detect")
        self.inf = {0: '11 ', 1: '02 ', 2: '07 ', 3: '03 ', 4: '2 ', 5: '13 ', 6: '25 ', 7: '28 ', 8: '04 '}
        self.saveMif = 3

    def run_inference(self, data: list):
        print("run_inference:", data)
        orgimgpath = data[0]
        if not isinstance(orgimgpath, str):
            raise TypeError("路径必须要是字符串")
        iou = data[1]
        conf = data[2]
        try:
            # tempYolo = copy.deepcopy(self.yolo)
            results = self.yolo.predict(source=orgimgpath, show=False, save=True, iou=iou, conf=conf)
        except Exception as e:
            print("Exception occurred ( tempYolo.predict ):", e)
            return [None, None, None, None, None, orgimgpath, None]
        imgshape = results[0].orig_shape
        runtime = results[0].speed['inference']
        save_dir = results[0].save_dir
        newimgName = modifySuffix(orgimgpath, r=".jpg")
        newimgpath = os.path.join(save_dir, newimgName)

        if len(results[0].boxes) <= 0:
            return [newimgpath, None, None, None, imgshape, orgimgpath, runtime]
        rectangle_pos = {
            "x": round(results[0].boxes.xyxy[0][0].item(), self.saveMif),
            "y": round(results[0].boxes.xyxy[0][1].item(), self.saveMif),
            "width": round((results[0].boxes.xyxy[0][2] - results[0].boxes.xyxy[0][0]).item(), self.saveMif),
            "height": round((results[0].boxes.xyxy[0][3] - results[0].boxes.xyxy[0][1]).item(), self.saveMif)
        }

        scores = results[0].boxes.conf  # 置信度分数
        classes = results[0].boxes.cls  # 类别索引

        return [newimgpath, rectangle_pos, round(float(scores[0]), self.saveMif), self.inf[int(classes[0])],
                imgshape, orgimgpath, round(runtime, self.saveMif)]


# 定义工作线程，用于执行推理任务
class InferenceThread(QThread):
    # 定义信号
    result_signal = pyqtSignal(list)  # 当推理完成时，将结果传递给主线程
    error_signal = pyqtSignal(str)  # 错误信号

    def __init__(self, model, data):
        super().__init__()
        self.model = model
        self.data = data

    def run(self):
        try:
            # 调用模型的推理方法
            result = self.model.run_inference(self.data)
            # 发出信号，传递结果
            self.result_signal.emit(result)
        except Exception as e:
            # 如果出现异常，发出错误信号
            self.error_signal.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YOLO 推理")
        self.setGeometry(100, 100, 600, 400)

        # 创建 UI 元素
        self.label = QLabel("推理结果将在这里显示", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.button = QPushButton("开始推理", self)
        self.button.clicked.connect(self.start_inference)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 创建 YoloModel 实例
        self.model = YoloModel()

    def start_inference(self):
        # 示例数据
        data = ['resource\\some_img\\wallhaven-jx25qw.jpg', 0.333, 0.583]

        # 创建并启动推理线程
        self.inference_thread = InferenceThread(self.model, data)
        self.inference_thread.result_signal.connect(self.on_inference_result)
        self.inference_thread.error_signal.connect(self.on_error)
        self.inference_thread.start()

    def on_inference_result(self, result):
        # 处理推理结果并更新 UI
        save_dir, rectangle_pos, scores, classes, imgshape, orgimgpath, runtime = result
        result_text = f"结果路径: {save_dir}\n" \
                      f"矩形位置: {rectangle_pos}\n" \
                      f"置信度: {scores}\n" \
                      f"类别: {classes}\n" \
                      f"原图路径: {orgimgpath}\n" \
                      f"运行时间: {runtime}秒"
        self.label.setText(result_text)

    def on_error(self, error_message):
        # 处理错误并更新 UI
        self.label.setText(f"错误: {error_message}")


if __name__ == "__main__":
    # ['resource\\some_img\\wallhaven-jx25qw.jpg', 0.333, 0.583]
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
