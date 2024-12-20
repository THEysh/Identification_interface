import os
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

from time import sleep

from ultralytics import YOLO

from yoloMod import modifySuffix


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

        scores = results[0].boxes.conf
        classes = results[0].boxes.cls

        return [newimgpath, rectangle_pos, round(float(scores[0]), self.saveMif), self.inf[int(classes[0])],
                imgshape, orgimgpath, round(runtime, self.saveMif)]


class YoloThread(QThread):
    result_signal = pyqtSignal(list)  # 定义信号，用于传输结果

    def __init__(self, model, data):
        super().__init__()
        self.model = model
        self.data = data

    def run(self):
        result = self.model.run_inference(self.data)
        self.result_signal.emit(result)  # 传递结果到主线程


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('YOLO Parallel Prediction')
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.label = QLabel('Click to start prediction', self)
        self.layout.addWidget(self.label)

        self.button = QPushButton('Start Prediction', self)
        self.button.clicked.connect(self.start_prediction)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def start_prediction(self):
        # 假设你有两个图片路径和一些配置数据
        data1 = ["resource/cut_RGB_20240719084737.png", 0.5, 0.4]
        data2 = ["resource/logo.png", 0.5, 0.4]

        # 初始化 YOLO 模型
        model1 = YoloModel()
        model2 = YoloModel()

        # 创建并启动两个线程
        self.thread1 = YoloThread(model1, data1)
        self.thread2 = YoloThread(model2, data2)

        self.thread1.result_signal.connect(self.update_label)
        self.thread2.result_signal.connect(self.update_label)

        self.thread1.start()
        self.thread2.start()

    def update_label(self, result):
        print("Prediction result:", result)
        self.label.setText(f'Prediction result: {result[0]}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
